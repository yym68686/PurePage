# PyTorch to MindSpore 翻译全流程梳理

🔗 项目链接：https://github.com/yym68686/ACL-DGReID-mindspore

## 前言

该项目任务是将 [Adaptive Cross-Domain learning for Generalizable Person Re-Identification](https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136740209.pdf) 论文的[原始 PyTorch 代码](https://github.com/peterzpy/ACL-DGReID) 翻译到 MindSpore 代码版本。已完成整个网络的对齐，但还不能训练。本项目基于 mindspore 2.2 版本。

## 翻译思路

- 先把原来的模型学会跑起来。
- 网络翻译：主要就是 API 映射，首先把主干网络翻译好。pytorch 到 mindspore 代码的映射可以参考下面的小节 API 映射。
- 网络输出张量对齐：在给网络做初步翻译后，需要保证翻译的正确性，需要进行主干网络对齐。测试 pytorch 与 mindspore 相应主干网络在相同的输入张量下，是否可是输出一样数值的张量。需要进行单元测试，就是把主干网络拆分为一个个小的网络模块。可以使用 python 的 unittest 模块做单元测试。单元测试可以参考 test/unitest/test.py 代码。本项目已完成网络输出张量对齐。
  - 参数映射：pytorch 与 mindspore 参数名有些不一样，比如 mindspore 里面的 moving_mean，moving_variance，gamma，beta。构建一个有序字典，将两个框架的参数一一对应起来，官网[脚本](https://www.mindspore.cn/docs/zh-CN/r2.0/migration_guide/sample_code.html?highlight=num_batches_tracked#%E5%8F%82%E6%95%B0%E6%98%A0%E5%B0%84%E5%8F%8Acheckpoint%E4%BF%9D%E5%AD%98)。我写好的参数名转换脚本可以参考 test/unitest/pth2ckpt.py 代码。
  - 权重迁移：把 pytorch 预训练模型里面网络权重迁移到 mindspore 中，用来固定网络的权重，pytorch 权重文件 pth 不能和 mindspore ckpt 文件通用，所以需要使用 pth to ckpt 转换脚本，官网[说明与脚本](https://www.mindspore.cn/docs/zh-CN/r2.0/faq/usage_migrate_3rd.html)。该项目已在 test/unitest/test.py 中实现。

- 完成上面的步骤就跑通动态图了。
- 下面需要跑通静态图。
- 编写训练代码。

## 环境安装

安装 pytorch mindspore 双环境，保证 cuda 版本一样

创建环境

```bash
conda create -y -n reid python=3.9
```

CUDA 11.6

```bash
conda install -y mindspore=2.2.14 -c mindspore -c conda-forge
conda install -y pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.6 -c pytorch -c nvidia
```

CUDA 11.1

```bash
# python<=3.8
conda install python=3.8 mindspore=2.2.11 pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch-lts -c mindspore -c conda-forge -c nvidia

conda install mindspore=2.2.11 -c mindspore -c conda-forge
conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch-lts -c nvidia

conda install -y pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=10.2
```

CUDA 10.1

```bash
conda install python=3.8
conda install mindspore=2.2.0 -c mindspore -c conda-forge
conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cudatoolkit=10.1 -c pytorch
pip install protobuf==3.20.3
```

确认是否 mindspore GPU 安装成功

```bash
python -c "import mindspore;mindspore.set_context(device_target='GPU');mindspore.run_check()"
python -c "import torch; print(torch.cuda.is_available())"
```

安装依赖

```bash
pip install -q -r requirements.txt
```

数据集同步

```bash
rsync -av --partial --progress /Users/yanyuming/Downloads/文件/split_reid_data.zip 40:/data/yuming
```

数据集解压

```bash
unzip split_reid_data.zip -x "__MACOSX/*"
```

调整测试数据集

```bash
sed -i 's|/4T/yuhan/datasets/reid_data/|/data0/yuming/split_reid_data/|g' /data0/yuming/split_reid_data/cuhk03_new/splits_new_labeled.json
```

传输预训练权重

```bash
mkdir -p /home/yuming/.cache/torch/checkpoints/
mv ~/resnet50_ibn_a-d9d0bb7b.ckpt /home/yuming/.cache/torch/checkpoints/
mv ~/resnet50_ibn_a-d9d0bb7b.pth /home/yuming/.cache/torch/checkpoints/

# pth
scp -r 41:/home/yuming/.cache/torch/checkpoints/resnet50_ibn_a-d9d0bb7b.pth /Users/yanyuming/Desktop/
scp -r /Users/yanyuming/Desktop/resnet50_ibn_a-d9d0bb7b.pth 40:/home/yuming/.cache/torch/checkpoints/

# ckpt
scp -r 41:/home/yuming/.cache/torch/checkpoints/resnet50_ibn_a-d9d0bb7b.ckpt /Users/yanyuming/Desktop/
scp -r /Users/yanyuming/Desktop/resnet50_ibn_a-d9d0bb7b.ckpt 40:/home/yuming/.cache/torch/checkpoints/
```

调试 launch.json

```json
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: 当前文件",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false,
            "args": [
                "--config-file", "./configs/bagtricks_DR50_mix.yml",
                "--num-gpus", "4"
            ]
        }
    ]
}
```


## Requirements

+ CUDA>=10.0
+ At least four 1080-Ti GPUs
+ Setup could refer to [INSTALL.md](INSTALL.md)
+ Other necessary packages listed in [requirements.txt](requirements.txt)
+ Training Data
  The model is trained and evaluated on Market-1501, MSMT17, cuhkSYSU, CUHK03. Download for these datasets, please refer to [fast-reid](https://github.com/JDAI-CV/fast-reid).

## 运行

```bash
# env
pip install -r requirements.txt
# train
python copy_launch.py
CUDA_VISIBLE_DEVICES=0,1,2,3 python3 tools/train_net.py --config-file ./configs/bagtricks_DR50_mix.yml --num-gpus 4
CUDA_VISIBLE_DEVICES=0 nohup python3 -u tools/train_net.py --config-file ./configs/bagtricks_DR50_mix.yml --num-gpus 1 > nohup.out 2>&1 &
pgrep -f 'train_net.py' | grep -v grep | xargs kill -9

# test
python3 tools/train_net.py --config-file ./configs/bagtricks_DR50_mix.yml --eval-only MODEL.WEIGHTS /path/to/checkpoint_file MODEL.DEVICE "cuda:0"
```

## API 映射

下面是 PyTorch 函数在 MindSpore 里面的映射，以下映射都是我个人经验的总结，可以直接复制用起来。

```python
# PyTorch
nn.Module

# MindSpore
nn.Cell


# PyTorch
nn.ReLU(inplace=True)

# MindSpore
nn.ReLU()


# PyTorch
nn.Sigmoid()

# MindSpore
nn.Sigmoid()


# PyTorch
nn.Parameter()

# MindSpore
mindspore.Parameter()


# PyTorch 图构造
forward

# MindSpore 图构造
construct


# PyTorch Sequential
nn.Sequential
# 或者
nn.ModuleList

# MindSpore SequentialCell
nn.SequentialCell


# PyTorch 
tensor.size()

# MindSpore
tensor.shape


# PyTorch 
tensor.size(0)

# MindSpore
tensor.shape[0]


# PyTorch 带 padding 的 MaxPool2d
maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

# MindSpore 带 padding 的 MaxPool2d
maxpool = nn.SequentialCell([
              nn.Pad(paddings=((0, 0), (0, 0), (1, 1), (1, 1)), mode="CONSTANT"),
              nn.MaxPool2d(kernel_size=3, stride=2)])


# PyTorch 全连接
fc = nn.Linear(in_features, out_features, bias=True)

# MindSpore 全连接，参数名不一致
# https://www.mindspore.cn/docs/zh-CN/r2.0.0-alpha/note/api_mapping/pytorch_diff/Dense.html
fc = nn.Dense(in_channels, out_channels, has_bias=True)


# PyTorch
torch.nn.functional.linear(inputs, self.weight, self.bias)

# MindSpore
mindspore.ops.dense(input, weight, bias=None)
# 或者
# MindSpore，需要实例化，bias 偏置张量，形状为 (out_channels,)
linear = mindspore.nn.Dense(self.in_feat, self.bias.shape[0])
linear.weight = self.weight
linear.bias = self.bias
output = linear(inputs)


# PyTorch AdaptiveAvgPool2d
nn.AdaptiveAvgPool2d(1)
# 或
nn.AdaptiveAvgPool2d((1, 1))

# MindSpore ReduceMean 和 AdaptiveAvgPool2d output shape是1时功能一致，且速度会快
# 默认情况下，使用指定维度的平均值代替该维度的其他元素，以移除该维度。也可仅缩小该维度大小至1。
# 通过指定 keep_dims 参数，来控制输出和输入的维度是否相同。
# https://www.mindspore.cn/docs/zh-CN/r2.0/api_python/ops/mindspore.ops.ReduceMean.html
# 官网给出的替换：https://www.mindspore.cn/docs/zh-CN/r2.0.0-alpha/migration_guide/sample_code.html
op = ops.ReduceMean(keep_dims=True)
output = op(x, tuple(range(len(x.shape)))[-2:])


# PyTorch
split = torch.split(inputs, self.half, 1)

# MindSpore
split = mindspore.ops.split(inputs, self.half, 1)


# PyTorch
out = torch.cat((out1, out2), dim=1)

# MindSpore
# https://www.mindspore.cn/docs/zh-CN/r2.0/note/api_mapping/pytorch_diff/cat.html
out = mindspore.ops.cat((out1, out2), axis=1)


# PyTorch
# stride: 窗口的步长。可以是一个单一的数字或者一个元组 (sW,)。默认值是 kernel_size。
torch.nn.functional.avg_pool1d(input_x, kernel_size=2, stride=2)

# MindSpore，avg_pool1d输入必须是三维的，PyTorch 没有限制
# stride: 窗口的步长。可以是一个单一的数字或者一个元组 (sW,)。默认值是 1。
output = mindspore.ops.avg_pool1d(input_x, kernel_size=2, stride=2)


# PyTorch
ret = Tensor(data).permute((3, 2, 1, 0))

# MindSpore
ret = ops.Transpose()(ms.Tensor(data), (3, 2, 1, 0))


# PyTorch
torch.Tensor.transpose(0, 1)

# MindSpore
mindspore.Tensor.swapaxes(0, 1)


# PyTorch
x.repeat(2, 2)

# MindSpore，不能用 repeat，因为 repeat 后里面的复制元素是连续的
x.tile((2, 2))


# PyTorch，数据对象，在较旧的 PyTorch 版本中使用
Variable

# MindSpore，根据上面的知识，下面的函数里面的 Variable 应该改成 Tensor
# 因为 Variable 在 PyTorch 中是用于求梯度的数据对象，而在 MindSpore 中，只有 Parameter 才需要求梯度。
Tensor


# PyTorch
torch.nn.functional.conv2d(inputs, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups)

# MindSpore
pad_mode = 'pad'
conv = mindspore.nn.Conv2d(in_channels=self.in_channels, out_channels=self.out_channels, kernel_size=self.kernel_size, stride=self.stride, pad_mode=pad_mode, padding=self.padding, dilation=self.dilation, group=self.groups)
conv.weight = self.weight
conv.bias = self.bias


# PyTorch
torch.nn.BatchNorm2d(
    num_features,
    eps=1e-05,
    momentum=0.1,
    affine=True,
    track_running_stats=True
)

# MindSpore，参数 track_running_stats 和 use_batch_statistics 功能一致，不同值对应的默认方式不同
# https://www.mindspore.cn/docs/zh-CN/r2.0/note/api_mapping/pytorch_diff/BatchNorm2d.html
# 两个主要区别：https://www.mindspore.cn/docs/zh-CN/r2.0/migration_guide/typical_api_comparision.html#nn.BatchNorm2d
mindspore.nn.BatchNorm2d(
    num_features,
    eps=1e-5,
    momentum=0.9,
    affine=True,
    gamma_init='ones',
    beta_init='zeros',
    moving_mean_init='zeros',
    moving_var_init='ones',
    use_batch_statistics=None,
    data_format='NCHW'
)


# PyTorch
torch.nn.functional.batch_norm(input, running_mean, running_var, weight, bias, training, momentum, eps)

# MindSpore
# https://www.mindspore.cn/docs/zh-CN/r2.0/api_python/ops/mindspore.ops.batch_norm.html
mindspore.ops.batch_norm(input, moving_mean, moving_variance, weight, bias, training, momentum, eps)


# PyTorch
result = torch.nn.functional.instance_norm(input, None, None, weight, bias, training, momentum, eps)

# MindSpore
# https://www.mindspore.cn/docs/zh-CN/r2.0/note/api_mapping/pytorch_diff/InstanceNorm2d.html
# InstanceNorm 仅支持在 GPU 上运行
mindspore.nn.InstanceNorm2d(num_features, eps, momentum, affine=True, gamma_init, beta_init)


# PyTorch
weight_init = 1
self.weight.data.fill_(weight_init)

# MindSpore
self.gamma.set_data(mindspore.common.initializer.initializer("ones", self.gamma.shape, self.gamma.dtype))


# PyTorch
bias_init = 0
self.bias.data.fill_(bias_init)

# MindSpore
self.beta.set_data(mindspore.common.initializer.initializer("zeros", self.beta.shape, self.beta.dtype))


# PyTorch
self.weight.data.fill_(weight_init)
self.weight.requires_grad_(True)

# MindSpore
self.gamma = mindspore.Parameter(mindspore.common.initializer.initializer(gamma_init, self.gamma.shape, self.gamma.dtype), name="gamma", requires_grad=True)


# PyTorch
torch.nn.init.constant_(self.weight, 0.0)

# MindSpore
self.gamma.set_data(mindspore.common.initializer.initializer("zeros", self.gamma.shape, self.gamma.dtype))


# PyTorch
nn.Conv2d()

# MindSpore，只有 pad_mode，has_bias 参数不一致
# https://www.mindspore.cn/docs/zh-CN/r2.0/note/api_mapping/pytorch_diff/Conv2d.html
nn.Conv2d()


# PyTorch
conv = nn.Conv2d(inplanes, planes, kernel_size=3, stride=stride, padding=1, bias=False)

# MindSpore
conv = nn.Conv2d(planes, planes, kernel_size=3, stride=1, pad_mode='pad', padding=1, has_bias=False)


# PyTorch
x_normalized = torch.nn.functional.normalize(x, p=2, dim=-1)

# MindSpore
l2_normalize = mindspore.ops.L2Normalize(axis=-1)
x_normalized = l2_normalize(x)
# 或者
x_normalized = mindspore.ops.L2Normalize(axis=-1)(x)


# PyTorch
for module in m.modules():
# 或者
for name, module in m.named_modules():

# MindSpore
for _, cell in m.cells_and_names():


# PyTorch
nn.init.normal_(m.weight, mean=0.0, std=1.0)

# MindSpore，到底是 weight 还是 gamma，依情况而变
m.weight.set_data(mindspore.common.initializer.initializer(mindspore.common.initializer.Normal(sigma=1.0, mean=0.0), m.weight.shape, m.weight.dtype))

# 实例：
# PyTorch
for name, m in self.cells_and_names():
    if isinstance(m, MetaConv2d):
        n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
		nn.init.normal_(m.weight, 0, math.sqrt(2. / n))
    elif isinstance(m, nn.BatchNorm2d):
		nn.init.constant_(m.weight, 1)
		nn.init.constant_(m.bias, 0)

# MindSpore
for name, m in self.cells_and_names():
    if isinstance(m, MetaConv2d):
        n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
        m.weight.set_data(mindspore.common.initializer.initializer(mindspore.common.initializer.Normal(sigma=math.sqrt(2. / n), mean=0.0), m.weight.shape, m.weight.dtype))
    elif isinstance(m, nn.BatchNorm2d):
        m.gamma.set_data(mindspore.common.initializer.initializer("ones", m.gamma.shape, m.gamma.dtype))
        m.beta.set_data(mindspore.common.initializer.initializer("zeros", m.beta.shape, m.beta.dtype))
        

# PyTorch
Module._modules

# MindSpore
Cell._cells


# PyTorch
state_dict = torch.load(pretrain_path, map_location=torch.device('cpu'))

# MindSpore，不能使用 pytorch 保存的 ckpt 文件，不能读取 pth 文件
state_dict = mindspore.load_checkpoint(pretrain_path)


# PyTorch
torch.optim.SGD

# MindSpore https://www.mindspore.cn/docs/zh-CN/r2.1/note/api_mapping/pytorch_api_mapping.html
mindspore.nn.SGD


# PyTorch
torch.optim.Optimizer

# MindSpore https://www.mindspore.cn/docs/zh-CN/r2.1/note/api_mapping/pytorch_api_mapping.html
mindspore.nn.Optimizer


# PyTorch
for module_param_name, value in module.named_parameters():
    model_dict[module_param_name] = value

# MindSpore
for item in model.get_parameters():
    model_dict[item.name] = item.value()


# PyTorch
names_weights_copy = dict()
for name, param in self.model.named_parameters():
    if param.requires_grad:
        names_weights_copy['self.model.' + name] = param

# MindSpore
names_weights_copy = dict()
for item in self.model.trainable_params():
    names_weights_copy['self.model.' + item.name] = item.value()


# PyTorch
torch.optim.lr_scheduler.CosineAnnealingLR

# MindSpore https://www.mindspore.cn/docs/zh-CN/r2.1/note/api_mapping/pytorch_diff/CosineDecayLr.html
mindspore.nn.cosine_decay_lr


# PyTorch
torch.optim.lr_scheduler.WarmupLR

# MindSpore https://www.mindspore.cn/docs/zh-CN/r2.1/api_python/nn/mindspore.nn.WarmUpLR.html
mindspore.nn.WarmUpLR


# PyTorch
torch.utils.data.sampler.BatchSampler

# MindSpore



# PyTorch
torch.utils.data.DataLoader

# MindSpore https://www.mindspore.cn/docs/zh-CN/r2.1/note/api_mapping/pytorch_diff/DataLoader.html
mindspore.dataset.GeneratorDataset


# PyTorch
torch.no_grad

# MindSpore https://www.mindspore.cn/docs/zh-CN/r2.1/migration_guide/typical_api_comparision.html
无
# 在 PyTorch 中，默认情况下，执行正向计算时会记录反向传播所需的信息，在推理阶段或无需反向传播网络中，这一操作是冗余的，会额外耗时，因此，PyTorch 提供了torch.no_grad 来取消该过程。
# 而 MindSpore 只有在调用grad才会根据正向图结构来构建反向图，正向执行时不会记录任何信息，所以 MindSpore 并不需要该接口，也可以理解为 MindSpore 的正向计算均在torch.no_grad 情况下进行的。


# PyTorch
torch.nn.functional.adaptive_avg_pool2d

# MindSpore
mindspore.ops.adaptive_avg_pool2d


# PyTorch
torch.Tensor.expand(3, 3)

# MindSpore https://www.mindspore.cn/docs/zh-CN/r2.1/note/api_mapping/pytorch_diff/expand.html
mindspore.Tensor.broadcast_to((3, 3))


# PyTorch type(distmat) = Tensor
# distmat = 1 * distmat - 2 * (inputs @ mat2)
distmat.addmm_(1, -2, inputs, mat2)

# MindSpore 
distmat = mindspore.ops.addmm(distmat, inputs, mat2, beta=1, alpha=-2)


# PyTorch
Tensor.clone()

# MindSpore
Tensor


# PyTorch
torch.Tensor.mul_(other)

# MindSpore
Tensor = mindspore.ops.mul(Tensor, other)


# PyTorch
torch.Tensor.resize_as_(Tensor)

# MindSpore
mindspore.Tensor.resize(*Tensor.shape)


# PyTorch
y = x.new().resize_as_(x).fill_(1)

# MindSpore
y = x.new_ones(x.shape)


# PyTorch
torch.Tensor.fill_(1)

# MindSpore
mindspore.ops.full(Tensor.shape, 1)


# PyTorch
torch.norm

# MindSpore https://www.mindspore.cn/docs/zh-CN/r2.1/api_python/ops/mindspore.ops.norm.html
mindspore.ops.norm


# PyTorch
torch.Tensor.sum(dim=None, keepdim=False, dtype=None)

# MindSpore https://www.mindspore.cn/docs/zh-CN/r2.2/note/api_mapping/pytorch_diff/TensorSum.html
torch.Tensor.sum((axis=None, dtype=None, keepdims=False, initial=None)
                 

# PyTorch
torch.ones(*size, *, out=None, dtype=None, layout=torch.strided, device=None, requires_grad=False)

# MindSpore https://www.mindspore.cn/docs/zh-CN/r2.1/note/api_mapping/pytorch_diff/ones.html
mindspore.ops.ones(shape, dtype=dtype)


# PyTorch
nn.Module.add_module

# MindSpore
nn.Cell.insert_child_to_cell


# PyTorch
output, inverse_indices = torch.unique(x, return_inverse=True)

# MindSpore
output, idx = mindspore.ops.unique(x)


# PyTorch
output = torch.unique(x)

# MindSpore
output, idx = mindspore.ops.unique(x)


# PyTorch
torch.tensor.data

# MindSpore
mindspore.tensor.value()


# PyTorch
torch.nn.functional.linear(inputs, weight, bias)

# MindSpore
mindspore.ops.matmul(inputs, weight.T) + bias


# PyTorch
num_gpus = torch.cuda.device_count()

# MindSpore
def get_gpu_num():
    import argparse
    parser = argparse.ArgumentParser(description="处理命令行参数")
    parser.add_argument('--num-gpus', type=int, default=1, help='GPU的数量')
    parser.add_argument("--config-file", default="", metavar="FILE", help="path to config file")
	# 这里要解析所有参数，不然会报错，这里只解析两个
    args = parser.parse_args()
    return args.num_gpus

num_gpus = get_gpu_num()


# PyTorch
grad_params = torch.autograd.grad(outputs=losses.mean(), inputs=names_weights_copy.values(), create_graph=True, allow_unused=True)

# MindSpore https://www.mindspore.cn/docs/zh-CN/r2.2/api_python/mindspore/mindspore.grad.html
grad_params = mindspore.grad(lambda x: x, grad_position=None, weights=model.trainable_params(), has_aux=False)(losses.mean())
# 或者
def ff(x):
	return x
grad_params = mindspore.grad(ff, grad_position=None, weights=model.trainable_params(), has_aux=False)(losses.mean())


# PyTorch
grad_params[i] = Variable(grad_params[i].data, requires_grad=False)

# MindSpore
grad_params[i] = mindspore.Parameter(grad_params[i].value(), requires_grad=False)


# PyTorch
torch.save(model.state_dict(), save_pth_path)

# MindSpore
mindspore.save_checkpoint(model, save_ckpt_path)
```

## 静态图调试记录

MindSpore 支持的 python 语法：https://www.mindspore.cn/docs/zh-CN/r2.0/note/static_graph_syntax_support.html

```
Traceback (most recent call last):
  File "/home/yuming/ACL-DGReID-mindspore/test/unitest/test.py", line 100, in test_ResNet
    output_tensor = ms_model(input_tensor, epoch)
  File "/home/yuming/miniconda3/envs/reid/lib/python3.9/site-packages/mindspore/nn/cell.py", line 620, in __call__
    out = self.compile_and_run(*args, **kwargs)
  File "/home/yuming/miniconda3/envs/reid/lib/python3.9/site-packages/mindspore/nn/cell.py", line 939, in compile_and_run
    self.compile(*args, **kwargs)
  File "/home/yuming/miniconda3/envs/reid/lib/python3.9/site-packages/mindspore/nn/cell.py", line 916, in compile
    _cell_graph_executor.compile(self, phase=self.phase,
  File "/home/yuming/miniconda3/envs/reid/lib/python3.9/site-packages/mindspore/common/api.py", line 1388, in compile
    result = self._graph_executor.compile(obj, args, kwargs, phase, self._use_vm_mode())
TypeError: 'self.NL_1_idx' should be initialized as a 'Parameter' type in the '__init__' function, but got '[]' with type 'list.

In file /home/yuming/ACL-DGReID-mindspore/fastreid/modeling/backbones/meta_dynamic_router_resnet.py:429
        if len(self.NL_1_idx) == 0:
               ^

----------------------------------------------------
- C++ Call Stack: (For framework developers)
----------------------------------------------------
mindspore/ccsrc/pipeline/jit/parse/parse.cc:2708 HandleAssignClassMember
```

参考官方文档：https://www.mindspore.cn/docs/zh-CN/r2.0/note/static_graph_syntax_support.html#%E7%BD%91%E7%BB%9C%E4%BD%BF%E7%94%A8%E7%BA%A6%E6%9D%9F

不允许修改网络的非`Parameter`类型数据成员。修改为 Parameter 初始化就行。



```
Traceback (most recent call last):
  File "/home/yuming/ACL-DGReID-mindspore/test/unitest/test.py", line 101, in test_ResNet
    output_tensor = ms_model(input_tensor, epoch)
  File "/home/yuming/miniconda3/envs/reid/lib/python3.9/site-packages/mindspore/nn/cell.py", line 620, in __call__
    out = self.compile_and_run(*args, **kwargs)
  File "/home/yuming/miniconda3/envs/reid/lib/python3.9/site-packages/mindspore/nn/cell.py", line 939, in compile_and_run
    self.compile(*args, **kwargs)
  File "/home/yuming/miniconda3/envs/reid/lib/python3.9/site-packages/mindspore/nn/cell.py", line 916, in compile
    _cell_graph_executor.compile(self, phase=self.phase,
  File "/home/yuming/miniconda3/envs/reid/lib/python3.9/site-packages/mindspore/common/api.py", line 1388, in compile
    result = self._graph_executor.compile(obj, args, kwargs, phase, self._use_vm_mode())
AttributeError: 'Attribute' object has no attribute 'id'
```



```
TypeError: Only support assign to attribute of self, but got attribute of linear.
```

原来的代码

```python
class MetaLinear(nn.Dense):
    def __init__(self, in_channels, out_channels, has_bias=False):
        super().__init__(in_channels, out_channels, has_bias=has_bias)

    def construct(self, inputs, opt = None, reserve = False):
        linear = nn.Dense(self.in_channels, self.out_channels, has_bias=self.has_bias)
        if opt != None and opt['meta']:
            output = linear(inputs)
            return output
        else:
            output = linear(inputs)
            return output
```

修改后

```python
class MetaLinear(nn.Dense):
    def __init__(self, in_channels, out_channels, has_bias=False):
        super().__init__(in_channels, out_channels, has_bias=has_bias)
        self.linear = nn.Dense(self.in_channels, self.out_channels, has_bias=self.has_bias)

    def construct(self, inputs, opt = None, reserve = False):
        if opt != None and opt['meta']:
            output = self.linear(inputs)
            return output
        else:
            output = self.linear(inputs)
            return output
```



```
RuntimeError: Unsupported statement 'Delete'.
```

出错的代码

```python
del opt['grad_params'][0]
```

修改后

```python
opt['grad_params'].pop(0)
```



```
NameError: The name 'c' is not defined, or not supported in graph mode.
```

出错的代码

```python
def a(b):
	if b == 1:
		c = 2
    return c
```

修改后

```python
def a(b):
	c = None
	if b == 1:
		c = 2
    return c
```



报错：

```
TypeError: The 4th initializing input to create instance for class 'mindspore.nn.layer.normalization.InstanceNorm2d' should be a constant, but got: AbstractKeywordArg(key: gamma_init, value: AbstractRefTensor(key: layer1.0.bn1.IN.gamma ref_value: AbstractRefTensor(shape: (32), element: AbstractScalar(Type: Float32, Value: ValueAny, Shape: NoShape), value_ptr: 0x5646bd968040, value: ValueAny), value: ValueAny))
```

gamma_init 初始化错误，静态图构图时就需要获取 init 的值，代码中的 gamma_init 状态需要通过 construct 获取。这种情况一般需要重写BN层，不能继承。



报错：

```
RuntimeError: BUG: no manager for this func graph: fastreid_modeling_ops_MetaConv2d_construct.82
```

出错的代码：

```python
class MetaConv2d(nn.Conv2d):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, group=1, bias=True, pad_mode='pad'):
        super().__init__(in_channels, out_channels, kernel_size, stride, pad_mode, padding, dilation, group, has_bias=bias)

        self.pad_mode = 'pad'

        self.w_step_size = 1
        self.b_step_size = 1
        self.conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride, pad_mode=pad_mode, padding=padding, dilation=dilation, group=group)
        self.conv.weight = self.weight

    def construct(self, inputs, opt=None):
        if opt and opt['meta']:
            updated_weight = update_parameter(self.weight, self.w_step_size, opt)
            updated_bias = update_parameter(self.bias, self.b_step_size, opt)
            output = self.conv(inputs)
            return output
        else:
            output = self.conv(inputs)
            return output
```

construct 入值不能含有 None 值，修改为：

```python
class MetaConv2d(nn.Conv2d):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, group=1, bias=True, pad_mode='pad'):
        super().__init__(in_channels, out_channels, kernel_size, stride, pad_mode, padding, dilation, group, has_bias=bias)

        self.pad_mode = 'pad'

        self.w_step_size = 1
        self.b_step_size = 1
        self.conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride, pad_mode=pad_mode, padding=padding, dilation=dilation, group=group)
        self.conv.weight = self.weight

    def construct(self, inputs, opt=0):
        if opt and opt['meta']:
            updated_weight = update_parameter(self.weight, self.w_step_size, opt)
            updated_bias = update_parameter(self.bias, self.b_step_size, opt)
            output = self.conv(inputs)
            return output
        else:
            output = self.conv(inputs)
            return output
```

## 训练代码调试

报错：

```
sub_(): argument 'other' (position 1) must be Tensor, not StubTensor
```

解决：

传入的是 torch Tensor，前面产生向量的 pytorch 代码没有转写到 mindspore。

在动态图下为了加速执行性能，使算子的执行过程能够进行异步执行，此处返回的是一个打桩张量（StubTensor，即这个tensor不是真正意义上的Tensor，但具有Tensor的所有方法和属性）；当用户脚本中去真正使用这个张量时，我们才会将具体的数据同步回来。

## Reference

[官网网络迁移调试实例](https://www.mindspore.cn/docs/zh-CN/r2.0.0-alpha/migration_guide/sample_code.html)

[官方文档中 MindSpore 与 PyTorch 典型区别](https://www.mindspore.cn/docs/zh-CN/r2.0/migration_guide/typical_api_comparision.html)

[PyTorch 与 MindSpore API 映射表](https://www.mindspore.cn/docs/zh-CN/r2.0/note/api_mapping/pytorch_api_mapping.html)

官方迁移实例：

https://gitee.com/mindspore/docs/blob/r2.0/docs/mindspore/source_zh_cn/migration_guide/code/resnet_convert/resnet_ms/src/resnet.py

https://gitee.com/mindspore/mindscience/tree/master/MindSPONGE/applications/research/DeepFRI

https://gitee.com/mindspore/mindscience/tree/master/MindSPONGE/applications/MEGAProtein

官网关于 MindSpore 的特性解答：https://www.mindspore.cn/docs/zh-CN/r2.0/faq/feature_advice.html?highlight=pth