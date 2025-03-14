# DTU

## tm2t

安装环境：

```bash
conda env create -f environment.yaml
conda activate tm2t
python -m spacy download en_core_web_sm

# environment.yaml 里面 - nlg-eval==2.3 换成 - git+https://github.com/Maluuba/nlg-eval.git@master
conda env update --file environment.yaml --prune

gdown 1OXy2FBhXrswT6zE4SBSPpVfQhxmI8Zzy
unzip t2m.zip
mkdir -p ./checkpoints
mv t2m ./checkpoints/
python app.py

curl -X POST "http://127.0.0.1:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"text": "一个人走路然后跳起来", "num_samples": 1}'
```

app.py

```python
import os
import tempfile
import torch
import numpy as np
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from os.path import join as pjoin
import logging
import spacy

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import utils.paramUtil as paramUtil
from utils.plot_script import *
from networks.quantizer import *
from networks.modules import *
from utils.word_vectorizer import WordVectorizerV2
from utils.utils import *
from scripts.motion_process import *

app = FastAPI(title="文本到动作生成API", description="将文本描述转换为3D人体动作")

# 模型和配置变量
vq_decoder = None
quantizer = None
t2m_model = None
w_vectorizer = None
mean = None
std = None
device = None
opt = None

class TextInput(BaseModel):
    text: str
    num_samples: Optional[int] = 1

class GenerationResult(BaseModel):
    motion_data: List[List[float]]

@app.on_event("startup")
async def load_models():
    """启动时加载预训练模型和配置"""
    global vq_decoder, quantizer, t2m_model, w_vectorizer, mean, std, device, opt

    logger.info("开始加载模型和配置...")

    # 配置参数
    class Options:
        def __init__(self):
            self.dataset_name = 't2m'
            self.gpu_id = 0 if torch.cuda.is_available() else -1
            self.checkpoints_dir = './checkpoints'
            self.tokenizer_name = 'VQVAEV3_CB1024_CMT_H1024_NRES3'
            self.name = 'T2M_Seq2Seq_NML1_Ear_SME0_N'
            self.joints_num = 22
            self.max_motion_token = 55
            self.max_motion_frame = 196
            self.codebook_size = 1024
            self.dim_vq_latent = 1024
            self.lambda_beta = 0.25
            self.n_resblk = 3
            self.n_down = 2
            self.q_mode = 'cmt'
            self.dim_txt_hid = 512
            self.dim_mot_hid = 1024
            self.n_mot_layers = 1
            self.early_or_late = 'early'
            self.sample = True
            self.top_k = 3
            self.device = torch.device("cpu" if self.gpu_id == -1 else f"cuda:{self.gpu_id}")

    opt = Options()
    device = opt.device
    logger.info(f"使用设备: {device}")

    if opt.dataset_name == 't2m':
        opt.joints_num = 22
        dim_pose = 263
        kinematic_chain = paramUtil.t2m_kinematic_chain
        logger.info("使用t2m数据集配置")
    elif opt.dataset_name == 'kit':
        opt.joints_num = 21
        dim_pose = 251
        kinematic_chain = paramUtil.kit_kinematic_chain
        logger.info("使用kit数据集配置")

    # 加载均值和标准差
    logger.info(f"正在加载均值和标准差文件从: {pjoin(opt.checkpoints_dir, opt.dataset_name, opt.tokenizer_name, 'meta')}")
    try:
        mean = np.load(pjoin(opt.checkpoints_dir, opt.dataset_name, opt.tokenizer_name, 'meta', 'mean.npy'))
        std = np.load(pjoin(opt.checkpoints_dir, opt.dataset_name, opt.tokenizer_name, 'meta', 'std.npy'))
        logger.info("均值和标准差加载成功")
    except Exception as e:
        logger.error(f"加载均值和标准差失败: {str(e)}")
        raise

    # 词汇配置
    n_mot_vocab = opt.codebook_size + 3
    opt.mot_start_idx = opt.codebook_size
    opt.mot_end_idx = opt.codebook_size + 1
    opt.mot_pad_idx = opt.codebook_size + 2

    enc_channels = [1024, opt.dim_vq_latent]
    dec_channels = [opt.dim_vq_latent, 1024, dim_pose]

    # 初始化词向量器
    logger.info("正在初始化词向量器...")
    try:
        w_vectorizer = WordVectorizerV2('./glove', 'our_vab')
        n_txt_vocab = len(w_vectorizer) + 1
        _, _, opt.txt_start_idx = w_vectorizer['sos/OTHER']
        _, _, opt.txt_end_idx = w_vectorizer['eos/OTHER']
        opt.txt_pad_idx = len(w_vectorizer)
        logger.info("词向量器初始化成功")
    except Exception as e:
        logger.error(f"初始化词向量器失败: {str(e)}")
        raise

    # 加载模型
    logger.info("正在创建VQ解码器...")
    try:
        vq_decoder = VQDecoderV3(opt.dim_vq_latent, dec_channels, opt.n_resblk, opt.n_down).to(device)
        logger.info("VQ解码器创建成功")
    except Exception as e:
        logger.error(f"创建VQ解码器失败: {str(e)}")
        raise

    logger.info(f"正在创建Quantizer (模式: {opt.q_mode})...")
    try:
        if opt.q_mode == 'ema':
            quantizer = EMAVectorQuantizer(opt.codebook_size, opt.dim_vq_latent, opt.lambda_beta).to(device)
        elif opt.q_mode == 'cmt':
            quantizer = Quantizer(opt.codebook_size, opt.dim_vq_latent, opt.lambda_beta).to(device)
        logger.info("Quantizer创建成功")
    except Exception as e:
        logger.error(f"创建Quantizer失败: {str(e)}")
        raise

    tokenizer_path = pjoin(opt.checkpoints_dir, opt.dataset_name, opt.tokenizer_name, 'model', 'finest.tar')
    logger.info(f"正在加载tokenizer模型从: {tokenizer_path}")
    try:
        checkpoint = torch.load(tokenizer_path, map_location=device)
        vq_decoder.load_state_dict(checkpoint['vq_decoder'])
        quantizer.load_state_dict(checkpoint['quantizer'])
        logger.info("tokenizer模型加载成功")
    except Exception as e:
        logger.error(f"加载tokenizer模型失败: {str(e)}")
        raise

    logger.info("正在创建文本到动作模型...")
    try:
        t2m_model = Seq2SeqText2MotModel(300, n_mot_vocab, opt.dim_txt_hid, opt.dim_mot_hid,
                                        opt.n_mot_layers, device, opt.early_or_late).to(device)
        logger.info("文本到动作模型创建成功")
    except Exception as e:
        logger.error(f"创建文本到动作模型失败: {str(e)}")
        raise

    model_path = pjoin(opt.checkpoints_dir, opt.dataset_name, opt.name, 'model', 'finest.tar')
    logger.info(f"正在加载文本到动作模型参数从: {model_path}")
    try:
        checkpoint = torch.load(model_path, map_location=device)
        t2m_model.load_state_dict(checkpoint['t2m_model'])
        logger.info("文本到动作模型参数加载成功")
    except Exception as e:
        logger.error(f"加载文本到动作模型参数失败: {str(e)}")
        raise

    # 设置为评估模式
    logger.info("将模型设置为评估模式...")
    vq_decoder.eval()
    quantizer.eval()
    t2m_model.eval()

    logger.info("所有模型已加载完成")

@app.post("/generate", response_model=GenerationResult)
async def generate_motion(text_input: TextInput = Body(...)):
    """
    从文本生成动作数据

    - **text**: 输入的文本描述
    - **num_samples**: 要生成的样本数量（默认为1）

    返回生成的动作数据
    """
    logger.info(f"收到生成请求: {text_input.text}")

    if vq_decoder is None or quantizer is None or t2m_model is None:
        logger.error("模型尚未加载，请稍后再试")
        raise HTTPException(status_code=500, detail="模型尚未加载，请稍后再试")

    # 限制生成的样本数量，避免服务器过载
    num_samples = min(text_input.num_samples, 5)
    logger.info(f"生成样本数量: {num_samples}")

    # 处理输入文本
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(text_input.text)
        temp_file_path = temp_file.name
        logger.info(f"已创建临时文件: {temp_file_path}")

    # 创建数据集和加载器
    import torch.utils.data as data

    class SimpleTextDataset(data.Dataset):
        def __init__(self, text, w_vectorizer, mean, std):
            self.text = [text]
            self.w_vectorizer = w_vectorizer
            self.mean = mean
            self.std = std
            self.nlp = spacy.load('en_core_web_sm')
            self.max_text_len = 20

        def __len__(self):
            return 1

        def process_text(self, sentence):
            """处理文本并返回词和词性标签"""
            # 如果是中文，简单分词
            if any('\u4e00' <= ch <= '\u9fff' for ch in sentence):
                # 简单中文分词处理 (实际应用中可能需要更好的中文处理)
                words = list(sentence)
                pos_tags = ['NOUN'] * len(words)  # 简化处理，将所有词视为名词
                return words, pos_tags

            # 英文处理
            sentence = sentence.replace('-', '')
            doc = self.nlp(sentence)
            word_list = []
            pos_list = []
            for token in doc:
                word = token.text
                if not word.isalpha():
                    continue
                if (token.pos_ == 'NOUN' or token.pos_ == 'VERB') and (word != 'left'):
                    word_list.append(token.lemma_)
                else:
                    word_list.append(word)
                pos_list.append(token.pos_)
            return word_list, pos_list

        def __getitem__(self, idx):
            caption = self.text[0]

            # 处理文本获取词和词性
            word_list, pos_list = self.process_text(caption)

            # 创建tokens
            tokens = ['%s/%s' % (word_list[i], pos_list[i]) for i in range(len(word_list))]

            # 处理token长度
            if len(tokens) < self.max_text_len:
                # pad with "unk"
                tokens = ['sos/OTHER'] + tokens + ['eos/OTHER']
                sent_len = len(tokens)
                tokens = tokens + ['unk/OTHER'] * (self.max_text_len + 2 - sent_len)
            else:
                # crop
                tokens = tokens[:self.max_text_len]
                tokens = ['sos/OTHER'] + tokens + ['eos/OTHER']
                sent_len = len(tokens)

            # 生成词嵌入和位置编码
            pos_one_hots = []
            word_embeddings = []
            for token in tokens:
                word_emb, pos_oh, _ = self.w_vectorizer[token]
                pos_one_hots.append(pos_oh[None, :])
                word_embeddings.append(word_emb[None, :])

            pos_one_hots = np.concatenate(pos_one_hots, axis=0)
            word_embeddings = np.concatenate(word_embeddings, axis=0)

            # 直接返回一个未嵌套的长整型标量值
            return word_embeddings, pos_one_hots, [caption], torch.tensor(sent_len, dtype=torch.int64)

    # 创建简单数据集
    logger.info("创建文本数据集...")
    try:
        dataset = SimpleTextDataset(text_input.text, w_vectorizer, mean, std)
        data_loader = torch.utils.data.DataLoader(dataset, batch_size=1, num_workers=0)
        logger.info("数据集创建成功")
    except Exception as e:
        logger.error(f"创建数据集失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建数据集失败: {str(e)}")

    # 生成动作
    generated_motions = []
    logger.info("开始生成动作...")

    with torch.no_grad():
        for i, batch_data in enumerate(data_loader):
            logger.info(f"处理批次 {i+1}")
            word_emb, pos_ohot, captions, cap_lens = batch_data
            word_emb = word_emb.to(device).float()

            # 确保cap_lens是1D张量
            if cap_lens.dim() > 1:
                logger.info(f"调整前cap_lens形状: {cap_lens.shape}")
                cap_lens = cap_lens.view(-1)  # 将多维张量展平为1D
                logger.info(f"调整后cap_lens形状: {cap_lens.shape}")

            # 确保在CPU上且为长整型
            cap_lens = cap_lens.cpu().long()

            logger.info(f"最终cap_lens: 形状={cap_lens.shape}, 类型={cap_lens.dtype}, 设备={cap_lens.device}, 值={cap_lens.tolist()}")

            for t in range(num_samples):
                logger.info(f"生成样本 {t+1}/{num_samples}")
                pred_tokens, len_map = t2m_model.sample_batch(
                    word_emb, cap_lens,
                    trg_sos=opt.mot_start_idx,
                    trg_eos=opt.mot_end_idx,
                    max_steps=49,
                    top_k=opt.top_k
                )

                # 处理生成的标记
                if len_map[0] > 0:
                    logger.info(f"生成了 {len_map[0]} 个标记")
                    pred_tokens = pred_tokens[:, 1:len_map[0]+1]
                    vq_latent = quantizer.get_codebook_entry(pred_tokens)
                    gen_motion = vq_decoder(vq_latent)

                    # 处理生成的动作数据
                    motion_data = gen_motion.cpu().numpy()[0]
                    # 应用均值和标准差
                    motion_data = motion_data * std + mean
                    # 转换为关节数据
                    joint_data = recover_from_ric(torch.from_numpy(motion_data).float(), opt.joints_num).numpy()
                    joint_data = motion_temporal_filter(joint_data)

                    # 返回动作数据
                    generated_motions.append(joint_data.tolist())
                    logger.info(f"样本 {t+1} 生成成功，形状: {joint_data.shape}")
                else:
                    logger.warning(f"样本 {t+1} 生成失败，没有有效标记")

    # 清理临时文件
    os.unlink(temp_file_path)
    logger.info(f"已删除临时文件: {temp_file_path}")

    if not generated_motions:
        logger.error("无法生成动作数据")
        raise HTTPException(status_code=500, detail="无法生成动作数据")

    # 将三维数组(帧数,关节数,坐标数)转换为二维数组(帧数,[关节1_x,关节1_y,关节1_z,...,关节n_z])
    flattened_motion = []
    for frame in generated_motions[0]:
        # 将每一帧的所有关节坐标平展为一个一维数组
        flat_frame = []
        for joint in frame:
            flat_frame.extend(joint)  # 添加x,y,z坐标
        flattened_motion.append(flat_frame)

    logger.info(f"成功生成动作数据，返回第一个样本，平展后形状: {len(flattened_motion)}x{len(flattened_motion[0])}")

    # 返回平展后的数据
    return GenerationResult(motion_data=flattened_motion)

if __name__ == "__main__":
    import uvicorn
    logger.info("启动API服务器...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
```



## videollava

项目地址：https://github.com/PKU-YuanGroup/Video-LLaVA/tree/main

```bash
cd /dtu/p1/lilei/code/Video-LLaVA
```

安装环境

```
pip install -e .
pip install -U transformers
pip install timm==1.0.15
pip install protobuf==3.20.0
```

依赖：

```
"torch==2.1.0", "torchvision==0.16.0",
```

代码

```python
import os
from pathlib import Path

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Gradio缓存目录到当前用户有写入权限的位置
os.environ["GRADIO_TEMP_DIR"] = str(Path.home() / "gradio_cache")
# 确保缓存目录存在
Path(os.environ["GRADIO_TEMP_DIR"]).mkdir(parents=True, exist_ok=True)

import shutil
import subprocess

import torch
import gradio as gr
from fastapi import FastAPI
import os
from PIL import Image
import tempfile
from decord import VideoReader, cpu
from transformers import TextStreamer

from videollava.constants import DEFAULT_IMAGE_TOKEN
from videollava.conversation import conv_templates, SeparatorStyle, Conversation
from videollava.serve.gradio_utils import Chat, tos_markdown, learn_more_markdown, title_markdown, block_css



def save_image_to_local(image):
    filename = os.path.join('temp', next(tempfile._get_candidate_names()) + '.jpg')
    image = Image.open(image)
    image.save(filename)
    # print(filename)
    return filename


def save_video_to_local(video_path):
    filename = os.path.join('temp', next(tempfile._get_candidate_names()) + '.mp4')
    shutil.copyfile(video_path, filename)
    return filename


def generate(image1, video, textbox_in, first_run, state, state_, images_tensor):
    flag = 1
    if not textbox_in:
        if len(state_.messages) > 0:
            textbox_in = state_.messages[-1][1]
            state_.messages.pop(-1)
            flag = 0
        else:
            return "Please enter instruction"

    image1 = image1 if image1 else "none"
    video = video if video else "none"
    # assert not (os.path.exists(image1) and os.path.exists(video))

    if type(state) is not Conversation:
        state = conv_templates[conv_mode].copy()
        state_ = conv_templates[conv_mode].copy()
        images_tensor = []

    first_run = False if len(state.messages) > 0 else True

    text_en_in = textbox_in.replace("picture", "image")

    # images_tensor = [[], []]
    image_processor = handler.image_processor
    if os.path.exists(image1) and not os.path.exists(video):
        tensor = image_processor.preprocess(image1, return_tensors='pt')['pixel_values'][0]
        # print(tensor.shape)
        tensor = tensor.to(handler.model.device, dtype=dtype)
        images_tensor.append(tensor)
    video_processor = handler.video_processor
    if not os.path.exists(image1) and os.path.exists(video):
        tensor = video_processor(video, return_tensors='pt')['pixel_values'][0]
        # print(tensor.shape)
        tensor = tensor.to(handler.model.device, dtype=dtype)
        images_tensor.append(tensor)
    if os.path.exists(image1) and os.path.exists(video):
        tensor = video_processor(video, return_tensors='pt')['pixel_values'][0]
        # print(tensor.shape)
        tensor = tensor.to(handler.model.device, dtype=dtype)
        images_tensor.append(tensor)

        tensor = image_processor.preprocess(image1, return_tensors='pt')['pixel_values'][0]
        # print(tensor.shape)
        tensor = tensor.to(handler.model.device, dtype=dtype)
        images_tensor.append(tensor)

    if os.path.exists(image1) and not os.path.exists(video):
        text_en_in = DEFAULT_IMAGE_TOKEN + '\n' + text_en_in
    if not os.path.exists(image1) and os.path.exists(video):
        text_en_in = ''.join([DEFAULT_IMAGE_TOKEN] * handler.model.get_video_tower().config.num_frames) + '\n' + text_en_in
    if os.path.exists(image1) and os.path.exists(video):
        text_en_in = ''.join([DEFAULT_IMAGE_TOKEN] * handler.model.get_video_tower().config.num_frames) + '\n' + text_en_in + '\n' + DEFAULT_IMAGE_TOKEN
    # print(text_en_in)
    text_en_out, state_ = handler.generate(images_tensor, text_en_in, first_run=first_run, state=state_)
    state_.messages[-1] = (state_.roles[1], text_en_out)

    text_en_out = text_en_out.split('#')[0]
    textbox_out = text_en_out

    show_images = ""
    if os.path.exists(image1):
        filename = save_image_to_local(image1)
        show_images += f'<img src="./file={filename}" style="display: inline-block;width: 250px;max-height: 400px;">'
    if os.path.exists(video):
        filename = save_video_to_local(video)
        show_images += f'<video controls playsinline width="500" style="display: inline-block;"  src="./file={filename}"></video>'

    if flag:
        state.append_message(state.roles[0], textbox_in + "\n" + show_images)
    state.append_message(state.roles[1], textbox_out)

    return (state, state_, state.to_gradio_chatbot(), False, gr.update(value=None, interactive=True), images_tensor, gr.update(value=image1 if os.path.exists(image1) else None, interactive=True), gr.update(value=video if os.path.exists(video) else None, interactive=True))


def regenerate(state, state_):
    state.messages.pop(-1)
    state_.messages.pop(-1)
    if len(state.messages) > 0:
        return state, state_, state.to_gradio_chatbot(), False
    return (state, state_, state.to_gradio_chatbot(), True)


def clear_history(state, state_):
    state = conv_templates[conv_mode].copy()
    state_ = conv_templates[conv_mode].copy()
    return (gr.update(value=None, interactive=True),
            gr.update(value=None, interactive=True), \
            gr.update(value=None, interactive=True), \
            True, state, state_, state.to_gradio_chatbot(), [])


conv_mode = "llava_v1"
model_path = 'LanguageBind/Video-LLaVA-7B'
cache_dir = './cache_dir'
device = 'cuda'
load_8bit = True
load_4bit = False
dtype = torch.float16
handler = Chat(model_path, conv_mode=conv_mode, load_8bit=load_8bit, load_4bit=load_8bit, device=device, cache_dir=cache_dir)
# handler.model.to(dtype=dtype)
if not os.path.exists("temp"):
    os.makedirs("temp")

app = FastAPI()


textbox = gr.Textbox(
    show_label=False, placeholder="Enter text and press ENTER", container=False
)
with gr.Blocks(title='Video-LLaVA🚀', theme=gr.themes.Default(), css=block_css) as demo:
    gr.Markdown(title_markdown)
    state = gr.State()
    state_ = gr.State()
    first_run = gr.State()
    images_tensor = gr.State()

    with gr.Row():
        with gr.Column(scale=3):
            image1 = gr.Image(label="Input Image", type="filepath")
            video = gr.Video(label="Input Video")

            cur_dir = os.path.dirname(os.path.abspath(__file__))
            gr.Examples(
                examples=[
                    [
                        f"{cur_dir}/examples/extreme_ironing.jpg",
                        "What is unusual about this image?",
                    ],
                    [
                        f"{cur_dir}/examples/waterview.jpg",
                        "What are the things I should be cautious about when I visit here?",
                    ],
                    [
                        f"{cur_dir}/examples/desert.jpg",
                        "If there are factual errors in the questions, point it out; if not, proceed answering the question. What’s happening in the desert?",
                    ],
                ],
                inputs=[image1, textbox],
            )

        with gr.Column(scale=7):
            chatbot = gr.Chatbot(label="Video-LLaVA", bubble_full_width=True).style(height=750)
            with gr.Row():
                with gr.Column(scale=8):
                    textbox.render()
                with gr.Column(scale=1, min_width=50):
                    submit_btn = gr.Button(
                        value="Send", variant="primary", interactive=True
                    )
            with gr.Row(elem_id="buttons") as button_row:
                upvote_btn = gr.Button(value="👍  Upvote", interactive=True)
                downvote_btn = gr.Button(value="👎  Downvote", interactive=True)
                flag_btn = gr.Button(value="⚠️  Flag", interactive=True)
                # stop_btn = gr.Button(value="⏹️  Stop Generation", interactive=False)
                regenerate_btn = gr.Button(value="🔄  Regenerate", interactive=True)
                clear_btn = gr.Button(value="🗑️  Clear history", interactive=True)

    with gr.Row():
        gr.Examples(
            examples=[
                [
                    f"{cur_dir}/examples/sample_img_22.png",
                    f"{cur_dir}/examples/sample_demo_22.mp4",
                    "Are the instruments in the pictures used in the video?",
                ],
                [
                    f"{cur_dir}/examples/sample_img_13.png",
                    f"{cur_dir}/examples/sample_demo_13.mp4",
                    "Does the flag in the image appear in the video?",
                ],
                [
                    f"{cur_dir}/examples/sample_img_8.png",
                    f"{cur_dir}/examples/sample_demo_8.mp4",
                    "Are the image and the video depicting the same place?",
                ],
            ],
            inputs=[image1, video, textbox],
        )
        gr.Examples(
            examples=[
                [
                    f"{cur_dir}/examples/sample_demo_1.mp4",
                    "Why is this video funny?",
                ],
                [
                    f"{cur_dir}/examples/sample_demo_3.mp4",
                    "Can you identify any safety hazards in this video?"
                ],
                [
                    f"{cur_dir}/examples/sample_demo_9.mp4",
                    "Describe the video.",
                ],
                [
                    f"{cur_dir}/examples/sample_demo_22.mp4",
                    "Describe the activity in the video.",
                ],
            ],
            inputs=[video, textbox],
        )
    gr.Markdown(tos_markdown)
    gr.Markdown(learn_more_markdown)

    submit_btn.click(generate, [image1, video, textbox, first_run, state, state_, images_tensor],
                     [state, state_, chatbot, first_run, textbox, images_tensor, image1, video])

    regenerate_btn.click(regenerate, [state, state_], [state, state_, chatbot, first_run]).then(
        generate, [image1, video, textbox, first_run, state, state_, images_tensor], [state, state_, chatbot, first_run, textbox, images_tensor, image1, video])

    clear_btn.click(clear_history, [state, state_],
                    [image1, video, textbox, first_run, state, state_, chatbot, images_tensor])

# app = gr.mount_gradio_app(app, demo, path="/")
demo.launch(share=True)

# uvicorn videollava.serve.gradio_web_server:app
# python -m  videollava.serve.gradio_web_server

```

最后的代码 videollava_api.py：

```python
import av
import numpy as np
from transformers import VideoLlavaProcessor, VideoLlavaForConditionalGeneration

def read_video_pyav(container, indices):
    frames = []
    container.seek(0)
    start_index = indices[0]
    end_index = indices[-1]
    for i, frame in enumerate(container.decode(video=0)):
        if i > end_index:
            break
        if i >= start_index and i in indices:
            frames.append(frame)
    return np.stack([x.to_ndarray(format="rgb24") for x in frames])


model = VideoLlavaForConditionalGeneration.from_pretrained("LanguageBind/Video-LLaVA-7B-hf")
processor = VideoLlavaProcessor.from_pretrained("LanguageBind/Video-LLaVA-7B-hf")

prompt = "USER: <video>Why is this video funny? ASSISTANT:"
exit(0)
video_path = "YOUR-LOCAL-VIDEO-PATH"
container = av.open(video_path)

# sample uniformly 8 frames from the video
total_frames = container.streams.video[0].frames
indices = np.arange(0, total_frames, total_frames / 8).astype(int)
clip = read_video_pyav(container, indices)

inputs = processor(text=prompt, videos=clip, return_tensors="pt")

# Generate
generate_ids = model.generate(**inputs, max_length=80)
print(processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0])
```



## MotionGPT

官方仓库：https://github.com/OpenMotionLab/MotionGPT

申请显卡：

```bash
p1gpush
```

文件目录：

```bash
cd /dtu/p1/lilei/code/MotionGPT
```

激活 conda 环境

```bash
conda activate /dtu/p1/lilei/code/MotionGPT/mgpt
```

安装依赖

```bash
pip install opencv-python moviepy gradio shapely pyarmor
```

加密：

```
pyarmor gen app.py
```

启动加密文件：

```python
import dist.app  # 这是加密后的模块名

if __name__ == "__main__":
    # 调用加密模块中的主函数
    dist.app.main()  # 如果您的原始app.py没有main函数，您需要在core_logic.py中添加一个
```

移动 dist/pyarmor_runtime_000000 到 工作目录。

启动文件：

```
python app.py
```

app.py

```python
import os
from pathlib import Path

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Gradio缓存目录到当前用户有写入权限的位置
os.environ["GRADIO_TEMP_DIR"] = str(Path.home() / "gradio_cache")
# 确保缓存目录存在
Path(os.environ["GRADIO_TEMP_DIR"]).mkdir(parents=True, exist_ok=True)

import imageio
import gradio as gr
import random
import torch
import time
import cv2
import numpy as np
import pytorch_lightning as pl
# import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip
from pathlib import Path
from mGPT.data.build_data import build_data
from mGPT.models.build_model import build_model
from mGPT.config import parse_args
from scipy.spatial.transform import Rotation as RRR
import mGPT.render.matplot.plot_3d_global as plot_3d
from mGPT.render.pyrender.hybrik_loc2rot import HybrIKJointsToRotmat
from mGPT.render.pyrender.smpl_render import SMPLRender

os.environ['DISPLAY'] = ':0.0'
os.environ['PYOPENGL_PLATFORM'] = 'egl'

# Load model
cfg = parse_args(phase="webui")  # parse config file
cfg.FOLDER = 'cache'
output_dir = Path(cfg.FOLDER)
output_dir.mkdir(parents=True, exist_ok=True)
pl.seed_everything(cfg.SEED_VALUE)
if cfg.ACCELERATOR == "gpu":
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
datamodule = build_data(cfg, phase="test")
model = build_model(cfg, datamodule)
state_dict = torch.load(cfg.TEST.CHECKPOINTS, map_location="cpu")["state_dict"]
model.load_state_dict(state_dict)
model.to(device)

# HTML Style
Video_Components = """
<div class="side-video" style="position: relative;">
    <video width="340" autoplay loop>
        <source src="file/{video_path}" type="video/mp4">
    </video>
    <a class="videodl-button" href="file/{video_path}" download="{video_fname}" title="Download Video">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-video"><path d="m22 8-6 4 6 4V8Z"/><rect width="14" height="12" x="2" y="6" rx="2" ry="2"/></svg>
    </a>
    <a class="npydl-button" href="file/{motion_path}" download="{motion_fname}" title="Download Motion">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-box"><path d="M14.5 22H18a2 2 0 0 0 2-2V7.5L14.5 2H6a2 2 0 0 0-2 2v4"/><polyline points="14 2 14 8 20 8"/><path d="M2.97 13.12c-.6.36-.97 1.02-.97 1.74v3.28c0 .72.37 1.38.97 1.74l3 1.83c.63.39 1.43.39 2.06 0l3-1.83c.6-.36.97-1.02.97-1.74v-3.28c0-.72-.37-1.38-.97-1.74l-3-1.83a1.97 1.97 0 0 0-2.06 0l-3 1.83Z"/><path d="m7 17-4.74-2.85"/><path d="m7 17 4.74-2.85"/><path d="M7 17v5"/></svg>
    </a>
</div>
"""

Video_Components_example = """
<div class="side-video" style="position: relative;">
    <video width="340" autoplay loop controls>
        <source src="file/{video_path}" type="video/mp4">
    </video>
    <a class="npydl-button" href="file/{video_path}" download="{video_fname}" title="Download Video">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-video"><path d="m22 8-6 4 6 4V8Z"/><rect width="14" height="12" x="2" y="6" rx="2" ry="2"/></svg>
    </a>
</div>
"""

Text_Components = """
<h3 class="side-content" >{msg}</h3>
"""


def motion_token_to_string(motion_token, lengths, codebook_size=512):
    motion_string = []
    for i in range(motion_token.shape[0]):
        motion_i = motion_token[i].cpu(
        ) if motion_token.device.type == 'cuda' else motion_token[i]
        motion_list = motion_i.tolist()[:lengths[i]]
        motion_string.append(
            (f'<motion_id_{codebook_size}>' +
             ''.join([f'<motion_id_{int(i)}>' for i in motion_list]) +
             f'<motion_id_{codebook_size + 1}>'))
    return motion_string


def render_motion(data, feats, method='fast'):
    fname = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(
        time.time())) + str(np.random.randint(10000, 99999))
    video_fname = fname + '.mp4'
    feats_fname = fname + '.npy'
    output_npy_path = os.path.join(output_dir, feats_fname)
    output_mp4_path = os.path.join(output_dir, video_fname)
    np.save(output_npy_path, feats)

    if method == 'slow':
        if len(data.shape) == 4:
            data = data[0]
        data = data - data[0, 0]
        pose_generator = HybrIKJointsToRotmat()
        pose = pose_generator(data)
        pose = np.concatenate([
            pose,
            np.stack([np.stack([np.eye(3)] * pose.shape[0], 0)] * 2, 1)
        ], 1)
        shape = [768, 768]
        render = SMPLRender(cfg.RENDER.SMPL_MODEL_PATH)

        r = RRR.from_rotvec(np.array([np.pi, 0.0, 0.0]))
        pose[:, 0] = np.matmul(r.as_matrix().reshape(1, 3, 3), pose[:, 0])
        vid = []
        aroot = data[[0], 0]
        aroot[:, 1] = -aroot[:, 1]
        params = dict(pred_shape=np.zeros([1, 10]),
                      pred_root=aroot,
                      pred_pose=pose)
        render.init_renderer([shape[0], shape[1], 3], params)
        for i in range(data.shape[0]):
            renderImg = render.render(i)
            vid.append(renderImg)

        out = np.stack(vid, axis=0)
        output_gif_path = output_mp4_path[:-4] + '.gif'
        imageio.mimwrite(output_gif_path, out, duration=50)
        out_video = VideoFileClip(output_gif_path)
        out_video.write_videofile(output_mp4_path)
        del out, render

    elif method == 'fast':
        output_gif_path = output_mp4_path[:-4] + '.gif'
        if len(data.shape) == 3:
            data = data[None]
        if isinstance(data, torch.Tensor):
            data = data.cpu().numpy()
        pose_vis = plot_3d.draw_to_batch(data, [''], [output_gif_path])
        out_video = VideoFileClip(output_gif_path)
        out_video.write_videofile(output_mp4_path)
        del pose_vis

    return output_mp4_path, video_fname, output_npy_path, feats_fname


def load_motion(motion_uploaded, method):
    file = motion_uploaded['file']

    feats = torch.tensor(np.load(file), device=model.device)
    if len(feats.shape) == 2:
        feats = feats[None]
    # feats = model.datamodule.normalize(feats)

    # Motion tokens
    motion_lengths = feats.shape[0]
    motion_token, _ = model.vae.encode(feats)

    motion_token_string = model.lm.motion_token_to_string(
        motion_token, [motion_token.shape[1]])[0]
    motion_token_length = motion_token.shape[1]

    # Motion rendered
    joints = model.datamodule.feats2joints(feats.cpu()).cpu().numpy()
    output_mp4_path, video_fname, output_npy_path, joints_fname = render_motion(
        joints,
        feats.to('cpu').numpy(), method)

    motion_uploaded.update({
        "feats": feats,
        "joints": joints,
        "motion_video": output_mp4_path,
        "motion_video_fname": video_fname,
        "motion_joints": output_npy_path,
        "motion_joints_fname": joints_fname,
        "motion_lengths": motion_lengths,
        "motion_token": motion_token,
        "motion_token_string": motion_token_string,
        "motion_token_length": motion_token_length,
    })

    return motion_uploaded


def add_text(history, text, motion_uploaded, data_stored, method):
    data_stored = data_stored + [{'user_input': text}]

    text = f"""<h3>{text}</h3>"""
    history = history + [(text, None)]
    if 'file' in motion_uploaded.keys():
        motion_uploaded = load_motion(motion_uploaded, method)
        output_mp4_path = motion_uploaded['motion_video']
        video_fname = motion_uploaded['motion_video_fname']
        output_npy_path = motion_uploaded['motion_joints']
        joints_fname = motion_uploaded['motion_joints_fname']
        history = history + [(Video_Components.format(
            video_path=output_mp4_path,
            video_fname=video_fname,
            motion_path=output_npy_path,
            motion_fname=joints_fname), None)]

    return history, gr.update(value="",
                              interactive=False), motion_uploaded, data_stored


def add_file(history, file, txt, motion_uploaded):
    motion_uploaded['file'] = file.name
    txt = txt.replace(" <Motion_Placeholder>", "") + " <Motion_Placeholder>"
    return history, gr.update(value=txt, interactive=True), motion_uploaded


def bot(history, motion_uploaded, data_stored, method):

    motion_length, motion_token_string = motion_uploaded[
        "motion_lengths"], motion_uploaded["motion_token_string"]

    input = data_stored[-1]['user_input']
    prompt = model.lm.placeholder_fulfill(input, motion_length,
                                          motion_token_string, "")
    data_stored[-1]['model_input'] = prompt
    batch = {
        "length": [motion_length],
        "text": [prompt],
    }

    outputs = model(batch, task="t2m")
    out_feats = outputs["feats"][0]
    out_lengths = outputs["length"][0]
    out_joints = outputs["joints"][:out_lengths].detach().cpu().numpy()
    out_texts = outputs["texts"][0]
    output_mp4_path, video_fname, output_npy_path, joints_fname = render_motion(
        out_joints,
        out_feats.to('cpu').numpy(), method)

    motion_uploaded = {
        "feats": None,
        "joints": None,
        "motion_video": None,
        "motion_lengths": 0,
        "motion_token": None,
        "motion_token_string": '',
        "motion_token_length": 0,
    }

    data_stored[-1]['model_output'] = {
        "feats": out_feats,
        "joints": out_joints,
        "length": out_lengths,
        "texts": out_texts,
        "motion_video": output_mp4_path,
        "motion_video_fname": video_fname,
        "motion_joints": output_npy_path,
        "motion_joints_fname": joints_fname,
    }

    if '<Motion_Placeholder>' == out_texts:
        response = [
            Video_Components.format(video_path=output_mp4_path,
                                    video_fname=video_fname,
                                    motion_path=output_npy_path,
                                    motion_fname=joints_fname)
        ]
    elif '<Motion_Placeholder>' in out_texts:
        response = [
            Text_Components.format(
                msg=out_texts.split("<Motion_Placeholder>")[0]),
            Video_Components.format(video_path=output_mp4_path,
                                    video_fname=video_fname,
                                    motion_path=output_npy_path,
                                    motion_fname=joints_fname),
            Text_Components.format(
                msg=out_texts.split("<Motion_Placeholder>")[1]),
        ]
    else:
        response = f"""<h3>{out_texts}</h3>"""

    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.02)
        yield history, motion_uploaded, data_stored


def bot_example(history, responses):
    history = history + responses
    return history


with open("assets/css/custom.css", "r", encoding="utf-8") as f:
    customCSS = f.read()

with gr.Blocks(css=customCSS) as demo:

    # Examples
    chat_instruct = gr.State([
        (None,
         "👋 Hi, I'm MotionGPT! I can generate realistic human motion from text, or generate text from motion."
         ),
        (None,
         "💡 You can chat with me in pure text like generating human motion following your descriptions."
         ),
        (None,
         "💡 After generation, you can click the button in the top right of generation human motion result to download the human motion video or feature stored in .npy format."
         ),
        (None,
         "💡 With the human motion feature file downloaded or got from dataset, you are able to ask me to translate it!"
         ),
        (None,
         "💡 Of courser, you can also purely chat with me and let me give you human motion in text, here are some examples!"
         ),
        (None,
         "💡 We provide two motion visulization methods. The default fast method is skeleton line ploting which is like the examples below:"
         ),
        (None,
         Video_Components_example.format(
             video_path="assets/videos/example0_fast.mp4",
             video_fname="example0_fast.mp4")),
        (None,
         "💡 And the slow method is SMPL model rendering which is more realistic but slower."
         ),
        (None,
         Video_Components_example.format(
             video_path="assets/videos/example0.mp4",
             video_fname="example0.mp4")),
        (None,
         "💡 If you want to get the video in our paper and website like below, you can refer to the scirpt in our [github repo](https://github.com/OpenMotionLab/MotionGPT#-visualization)."
         ),
        (None,
         Video_Components_example.format(
             video_path="assets/videos/example0_blender.mp4",
             video_fname="example0_blender.mp4")),
        (None, "👉 Follow the examples and try yourself!"),
    ])
    chat_instruct_sum = gr.State([(None, '''
         👋 Hi, I'm MotionGPT! I can generate realistic human motion from text, or generate text from motion.

         1. You can chat with me in pure text like generating human motion following your descriptions.
         2. After generation, you can click the button in the top right of generation human motion result to download the human motion video or feature stored in .npy format.
         3. With the human motion feature file downloaded or got from dataset, you are able to ask me to translate it!
         4. Of course, you can also purely chat with me and let me give you human motion in text, here are some examples!
         ''')] + chat_instruct.value[-7:])

    t2m_examples = gr.State([
        (None,
         "💡 You can chat with me in pure text, following are some examples of text-to-motion generation!"
         ),
        ("A person is walking forwards, but stumbles and steps back, then carries on forward.",
         Video_Components_example.format(
             video_path="assets/videos/example0.mp4",
             video_fname="example0.mp4")),
        ("Generate a man aggressively kicks an object to the left using his right foot.",
         Video_Components_example.format(
             video_path="assets/videos/example1.mp4",
             video_fname="example1.mp4")),
        ("Generate a person lowers their arms, gets onto all fours, and crawls.",
         Video_Components_example.format(
             video_path="assets/videos/example2.mp4",
             video_fname="example2.mp4")),
        ("Show me the video of a person bends over and picks things up with both hands individually, then walks forward.",
         Video_Components_example.format(
             video_path="assets/videos/example3.mp4",
             video_fname="example3.mp4")),
        ("Imagine a person is practing balancing on one leg.",
         Video_Components_example.format(
             video_path="assets/videos/example5.mp4",
             video_fname="example5.mp4")),
        ("Show me a person walks forward, stops, turns directly to their right, then walks forward again.",
         Video_Components_example.format(
             video_path="assets/videos/example6.mp4",
             video_fname="example6.mp4")),
        ("I saw a person sits on the ledge of something then gets off and walks away.",
         Video_Components_example.format(
             video_path="assets/videos/example7.mp4",
             video_fname="example7.mp4")),
        ("Show me a person is crouched down and walking around sneakily.",
         Video_Components_example.format(
             video_path="assets/videos/example8.mp4",
             video_fname="example8.mp4")),
    ])

    m2t_examples = gr.State([
        (None,
         "💡 With the human motion feature file downloaded or got from dataset, you are able to ask me to translate it, here are some examples!"
         ),
        ("Please explain the movement shown in <Motion_Placeholder> using natural language.",
         None),
        (Video_Components_example.format(
            video_path="assets/videos/example0.mp4",
            video_fname="example0.mp4"),
         "The person was pushed but didn't fall down"),
        ("What kind of action is being represented in <Motion_Placeholder>? Explain it in text.",
         None),
        (Video_Components_example.format(
            video_path="assets/videos/example4.mp4",
            video_fname="example4.mp4"),
         "The figure has its hands curled at jaw level, steps onto its left foot and raises right leg with bent knee to kick forward and return to starting stance."
         ),
        ("Provide a summary of the motion demonstrated in <Motion_Placeholder> using words.",
         None),
        (Video_Components_example.format(
            video_path="assets/videos/example2.mp4",
            video_fname="example2.mp4"),
         "A person who is standing with his arms up and away from his sides bends over, gets down on his hands and then his knees and crawls forward."
         ),
        ("Generate text for <Motion_Placeholder>:", None),
        (Video_Components_example.format(
            video_path="assets/videos/example5.mp4",
            video_fname="example5.mp4"),
         "The man tries to stand in a yoga tree pose and looses his balance."),
        ("Provide a summary of the motion depicted in <Motion_Placeholder> using language.",
         None),
        (Video_Components_example.format(
            video_path="assets/videos/example6.mp4",
            video_fname="example6.mp4"),
         "Person walks up some steps then leeps to the other side and goes up a few more steps and jumps dow"
         ),
        ("Describe the motion represented by <Motion_Placeholder> in plain English.",
         None),
        (Video_Components_example.format(
            video_path="assets/videos/example7.mp4",
            video_fname="example7.mp4"),
         "Person sits down, then stands up and walks forward. then the turns around 180 degrees and walks the opposite direction"
         ),
        ("Provide a description of the action in <Motion_Placeholder> using words.",
         None),
        (Video_Components_example.format(
            video_path="assets/videos/example8.mp4",
            video_fname="example8.mp4"),
         "This man is bent forward and walks slowly around."),
    ])

    t2t_examples = gr.State([
        (None,
         "💡 Of course, you can also purely chat with me and let me give you human motion in text, here are some examples!"
         ),
        ('Depict a motion as like you have seen it.',
         "A person slowly walked forward in rigth direction while making the circle"
         ),
        ('Random say something about describing a human motion.',
         "A man throws punches using his right hand."),
        ('Describe the motion of someone as you will.',
         "Person is moving left to right in a dancing stance swaying hips, moving feet left to right with arms held out"
         ),
        ('Come up with a human motion caption.',
         "A person is walking in a counter counterclockwise motion."),
        ('Write a sentence about how someone might dance.',
         "A person with his hands down by his sides reaches down for something with his right hand, uses the object to make a stirring motion, then places the item back down."
         ),
        ('Depict a motion as like you have seen it.',
         "A person is walking forward a few feet, then turns around, walks back, and continues walking."
         )
    ])

    Init_chatbot = chat_instruct.value[:
                                       1] + t2m_examples.value[:
                                                               3] + m2t_examples.value[:3] + t2t_examples.value[:2] + chat_instruct.value[
                                                                   -7:]

    # Variables
    motion_uploaded = gr.State({
        "feats": None,
        "joints": None,
        "motion_video": None,
        "motion_lengths": 0,
        "motion_token": None,
        "motion_token_string": '',
        "motion_token_length": 0,
    })
    data_stored = gr.State([])

    gr.Markdown("# MotionGPT")

    chatbot = gr.Chatbot(Init_chatbot,
                         elem_id="mGPT",
                         height=600,
                         label="MotionGPT",
                         avatar_images=(None,
                                        ("assets/images/avatar_bot.jpg")),
                         bubble_full_width=False)

    with gr.Row():
        with gr.Column(scale=0.85):
            with gr.Row():
                txt = gr.Textbox(
                    label="Text",
                    show_label=False,
                    elem_id="textbox",
                    placeholder=
                    "Enter text and press ENTER or speak to input. You can also upload motion.",
                    container=False)

            with gr.Row():
                btn = gr.UploadButton("📁 Upload motion",
                                      elem_id="upload",
                                      file_types=["file"])
                # regen = gr.Button("🔄 Regenerate", elem_id="regen")
                clear = gr.ClearButton([txt, chatbot], value='🗑️ Clear')

            with gr.Row():
                gr.Markdown('''
                ### You can get more examples (pre-generated for faster response) by clicking the buttons below:
                ''')

            with gr.Row():
                instruct_eg = gr.Button("Instructions", elem_id="instruct")
                t2m_eg = gr.Button("Text-to-Motion", elem_id="t2m")
                m2t_eg = gr.Button("Motion-to-Text", elem_id="m2t")
                t2t_eg = gr.Button("Random description", elem_id="t2t")

        with gr.Column(scale=0.15, min_width=150):
            method = gr.Dropdown(["slow", "fast"],
                                 label="Visulization method",
                                 interactive=True,
                                 elem_id="method",
                                 value="fast")

    txt_msg = txt.submit(
        add_text, [chatbot, txt, motion_uploaded, data_stored, method],
        [chatbot, txt, motion_uploaded, data_stored],
        queue=False).then(bot, [chatbot, motion_uploaded, data_stored, method],
                          [chatbot, motion_uploaded, data_stored])

    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)

    file_msg = btn.upload(add_file, [chatbot, btn, txt, motion_uploaded],
                          [chatbot, txt, motion_uploaded],
                          queue=False)

    # regen_msg = regen.click(bot,
    #                         [chatbot, motion_uploaded, data_stored, method],
    #                         [chatbot, motion_uploaded, data_stored],
    #                         queue=False)

    instruct_msg = instruct_eg.click(bot_example, [chatbot, chat_instruct_sum],
                                     [chatbot],
                                     queue=False)
    t2m_eg_msg = t2m_eg.click(bot_example, [chatbot, t2m_examples], [chatbot],
                              queue=False)
    m2t_eg_msg = m2t_eg.click(bot_example, [chatbot, m2t_examples], [chatbot],
                              queue=False)
    t2t_eg_msg = t2t_eg.click(bot_example, [chatbot, t2t_examples], [chatbot],
                              queue=False)

    chatbot.change(scroll_to_output=True)

demo.queue()

def main():
    demo.launch(server_name="0.0.0.0", server_port=8888, debug=True, share=True)

if __name__ == "__main__":
    main()
```

