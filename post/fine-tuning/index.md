# 使用 MacBook Pro 微调 LLM 实践

我的配置：m1 pro 16GB MacBook Pro。

使用 Apple 开发的 MLX 架构微调 Mistral。下载 mlx 仓库

```bash
git clone --depth 1 https://github.com/ml-explore/mlx-examples.git
```

在 lora 目录下安装依赖

```bash
pip install -r requirements.txt
```

使用 [ollama](https://github.com/jmorganca/ollama) API 生成数据集

```python
import os
import json
import requests

def query_ollama(prompt, model):
    # 设置请求的URL和数据
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    # 发送POST请求
    response = requests.post(url, json=data)

    # 检查响应状态码，如果成功则打印结果
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"请求失败，状态码：{response.status_code}"

def Generate_Mistral_training_data(instruction, answer):
    result = {
        'text': f"<s>[INST] {instruction}[/INST] {answer}</s>"
    }

    output = json.dumps(result) + "\n"
    # output = output.replace("[\/INST]", "[/INST]")
    # output = output.replace("<\/s>", "</s>")

    return output

def file_put_contents(text, filename):
    with open(filename, 'a') as file:
        file.write(text)


def create_valid_file(train_filename, valid_filename):
    if not os.path.exists(train_filename):
        raise FileNotFoundError('No train.jsonl file found!')

    with open(train_filename, 'r', encoding='utf-8') as file:
        train_lines = file.readlines()

    total_lines = len(train_lines)
    twenty_percent = round(total_lines * 0.2)

    val_lines = train_lines[:twenty_percent]
    train_lines = train_lines[twenty_percent:]

    with open(train_filename, 'w', encoding='utf-8') as file:
        file.writelines(train_lines)

    with open(valid_filename, 'w', encoding='utf-8') as file:
        file.writelines(val_lines)

def Generate_Mistral_instructions_file(instructions_prompt, instructions_filename, model):
    answer = query_ollama(instructions_prompt, model)
    file_put_contents(answer, instructions_filename)

def delete_numerical_numbering(original_data):
    lines = original_data.splitlines()
    cleaned_lines = [line.split('. ', 1)[1].replace(",", "") if '. ' in line else line for line in lines if line]
    if len(cleaned_lines) != 3:
        return None
    cleaned_data = '\n'.join(cleaned_lines)
    return cleaned_data

if __name__ == "__main__":
    # model = 'llama2'
    model = 'mistral'
    # model = 'phi'
    instructions_filename = 'instructions.json'
    train_filename = 'train.jsonl'
    valid_filename = 'valid.jsonl'

    # 取消注释运行就可以生成用户问题
    # instructions_prompt = (
    #     "Please list in JSONL format 50 frequently asked questions with Google from all levels of users."
    #     "The questions should start with any of the following: 'Where do I', 'Is it okay to', 'Can you help me', 'I need to', 'Is there a'"
    #     "'Do you know', 'Where is the', 'Can you tell me', 'Can I change', 'What are the', 'How do I', 'When is it', 'Does sth have'"
    #     "'How to', 'What is the difference', 'Can users', 'Can I', 'What is'."
    #     "You do not need to provide an answer or category to each question. The list should be a single dimension array of only questions."
    # )
    # Generate_Mistral_instructions_file(instructions_prompt, instructions_filename, model)
    # exit(0)

    with open(instructions_filename, 'r', encoding='utf-8') as file:
        instructions = [item["question"] for item in json.load(file)]

    total = len(instructions)

    for i, instruction in enumerate(instructions):
        print("------------------------------")
        print(f"({i + 1}/{total}) {instruction}")
        print("------------------------------")

        # 查询答案
        prompt = (
            "Based on my question, summarize the keywords to generalize the question."
            "The output requirements are as follows:"
            "1. Provide three different lines of keyword combinations, with the keywords in each line connected by spaces. Each line of keywords can be one or more."
            "2. Just give these three lines of keywords directly, no other explanation is needed, and no other symbols or content should appear."
            f"Here is my question: {instruction}"
        )
        answer = query_ollama(prompt, model)
        answer = delete_numerical_numbering(answer)
        print(answer)
        if answer:
            training_data_item = Generate_Mistral_training_data(instruction, answer)
            file_put_contents(training_data_item, train_filename)
    create_valid_file(train_filename, valid_filename)
    print("Done! Training and validation JSONL files created.\n")
```

我需要一个自动抽取搜索引擎关键词的本地模型。这个代码首先生成用户问的问题存到 instructions.json 文件里面，生成之后需要手动调整 json 格式使其符合 json 语法规则。然后把生成用户问题的代码注释掉。再运行代码读取用户问题然后让本地模型生成关键词。然后把答案和问题组合成 mistral 格式的训练集。最后拆分为验证集和训练集。

开始微调

```bash
python lora.py --train --batch-size 2 \
--model mistralai/Mistral-7B-Instruct-v0.2 \
--data /GitHub/fine-tuning \
--lora-layers 4 \
--iters 100
```

- `--data`是放训练集的文件夹

输出

```
None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
Loading pretrained model
Fetching 11 files: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████| 11/11 [00:00<00:00, 125033.45it/s]
Total parameters 7242.158M
Trainable parameters 0.426M
Loading datasets
Training
Iter 1: Val loss 8.750, Val took 1010.200s
Iter 10: Train loss 8.859, It/sec 0.019, Tokens/sec 1.578
Iter 20: Train loss 6.936, It/sec 0.018, Tokens/sec 1.633
Iter 30: Train loss 5.653, It/sec 0.018, Tokens/sec 1.504
Iter 40: Train loss 4.330, It/sec 0.017, Tokens/sec 1.796
Iter 50: Train loss 3.978, It/sec 0.019, Tokens/sec 1.864
Iter 60: Train loss 3.774, It/sec 0.019, Tokens/sec 1.483
Iter 70: Train loss 3.337, It/sec 0.018, Tokens/sec 1.543
Iter 80: Train loss 2.900, It/sec 0.018, Tokens/sec 1.533
Iter 90: Train loss 2.663, It/sec 0.019, Tokens/sec 1.874
Iter 100: Train loss 2.698, It/sec 0.018, Tokens/sec 1.499
```

测试基础模型

```bash
python generate.py \
--model mistralai/Mistral-7B-Instruct-v0.2 \
--max-tokens 1000 \
--prompt "How do I build an online store using WordPress that will allow me to sell car parts? I want to be able to ship them and charge people using credit cards."
```

测试微调模型

```bash
ppython lora.py \
--model mistralai/Mistral-7B-Instruct-v0.2 \
--adapter-file adapters.npz \
--max-tokens 1000 \
--prompt "How do I build an online store using WordPress that will allow me to sell car parts? I want to be able to ship them and charge people using credit cards."
```

效果并不好。不过也算是走通了微调的流程吧。

把微调权重融合到基础模型

```bash
python fuse.py \
 --model mistralai/Mistral-7B-Instruct-v0.2 \
 --adapter-file adapters.npz \
 --save-path ./Models/My-Mistral-7B-fine-tuned
 --upload-name My-Mistral-7B-fine-tuned
```

## References

https://apeatling.com/articles/simple-guide-to-local-llm-fine-tuning-on-a-mac-with-mlx/