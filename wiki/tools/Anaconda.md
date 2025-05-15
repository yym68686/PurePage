# Anaconda 常用命令

## miniconda

miniconda 下载地址：https://mirrors.bfsu.edu.cn/anaconda/miniconda/

一键安装脚本

```bash

wget -c -O miniconda.sh https://mirrors.zju.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh

wget -c -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x miniconda.sh
sh miniconda.sh -b
~/miniconda3/bin/conda init bash
echo -e 'if [ -f ~/.bashrc ]; then\n   source ~/.bashrc\nfi' >> ~/.bash_profile
source ~/.bashrc
~/miniconda3/bin/conda activate base

pip install pipx
pipx ensurepath
source ~/.bashrc
pipx install nvitop

# 使用 htop 查看每个cpu核心的使用情况
sudo apt update
sudo apt install htop

conda config --remove-key channels

conda config --add channels https://mirrors.zju.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.zju.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.zju.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.zju.edu.cn/anaconda/cloud/msys2/
conda config --add channels https://mirrors.zju.edu.cn/anaconda/cloud/bioconda/
conda config --add channels https://mirrors.zju.edu.cn/anaconda/cloud/menpo/
conda config --add channels https://mirrors.zju.edu.cn/anaconda/cloud/pytorch/
conda config --add channels https://mirrors.zju.edu.cn/anaconda/cloud/pytorch-lts/
conda config --add channels https://mirrors.zju.edu.cn/anaconda/cloud/MindSpore/

conda config --set show_channel_urls yes


pip config set global.index-url https://mirrors.zju.edu.cn/pypi/web/simple
```

下载脚本

```bash
wget -c -O miniconda.sh https://mirrors.bfsu.edu.cn/anaconda/miniconda/Miniconda3-py39_23.9.0-0-Linux-x86_64.sh
```

增加执行权限

```bash
chmod +x miniconda.sh
```

安装

```bash
sh miniconda.sh -b
```

初始化终端

```bash
conda init bash
```

写入 ~/.bash_profile，保证每次进入终端都会执行 `source ~/.bashrc`

```bash
echo -e 'if [ -f ~/.bashrc ]; then\n   source ~/.bashrc\nfi' >> ~/.bash_profile
```

原始命令

```bash
if [ -f ~/.bashrc ]; then
   source ~/.bashrc
fi
```

激活 conda 命令

```bash
echo 'export PATH="/home/yuming/miniconda3/bin:$PATH"' >> ~/.bashrc
```

## 环境变量

```powershell
D:\\anaconda
D:\\anaconda\\Scripts
D:\\anaconda\\Library\\bin
```

powershell 一键命令

```powershell
[environment]::SetEnvironmentvariable("PATH", "$([environment]::GetEnvironmentvariable("Path", "Machine"));D:\\anaconda;D:\\anaconda\\Scripts;D:\\anaconda\\Library\\bin", "Machine")
conda init powershell
```

## 创建环境

```bash
conda create -n Genimi python=3.9
```

* pytorch 是环境名称
* python=3.7 指定 python 的版本

## 删除虚拟环境

```bash
conda remove -n nlp --all
```

## 查看已有虚拟环境

```bash
conda-env list
```

## 查看当前 python 解释器路径：

```bash
which python
```

## 导出 requirements.txt

```python
python -m pip freeze > requirements.txt
```

## 安装 requirements.txt：

```
pip install -r requirements.txt
```

## 更新 conda

```bash
conda update -n base conda
```

## conda 搜索包

```powershell
anaconda search -t conda tensorflow-gpu
```

## conda 换源

显示所有源

```bash
conda config --show-sources
```

删除所有源

```powershell
conda config --remove-key channels
```

conda添加国内源

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/menpo/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

conda config --set show_channel_urls yes
```

condarc 文件

```yaml
channels:
  - defaults
custom_channels:
  conda-forge: https://mirrors.zju.edu.cn/anaconda/cloud
  msys2: https://mirrors.zju.edu.cn/anaconda/cloud
  bioconda: https://mirrors.zju.edu.cn/anaconda/cloud
  menpo: https://mirrors.zju.edu.cn/anaconda/cloud
  pytorch: https://mirrors.zju.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.zju.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.zju.edu.cn/anaconda/cloud
default_channels:
  - https://mirrors.zju.edu.cn/anaconda/pkgs/main
  - https://mirrors.zju.edu.cn/anaconda/pkgs/r
  - https://mirrors.zju.edu.cn/anaconda/pkgs/msys2
show_channel_urls: True
```

References

[https://blog.csdn.net/sean2100/article/details/80998643](https://blog.csdn.net/sean2100/article/details/80998643)

## 激活

```html
conda activate pytorch
```

激活失败可以试试 init，不行可以尝试以下方式：

windows 系统下在 powershell 终端输入：

```
activate
deactivate
```

如果是 Mac 或 Linux 系统输入：

```
# 激活环境
source activate
# 退出环境
source deactivate
```

然后再输入

```
conda activate envname
```

References

https://blog.csdn.net/weixin_45646006/article/details/115066805

## 退出

```html
conda deactivate
```

## conda 安装requirements.txt

```
conda install --yes --file requirements.txt
```

## conda查看自动启动

```
conda config --show | grep auto_activate_base
```

关闭自动启动

```
conda config --set auto_activate_base False
```

将当前环境下的 package 信息存入名为 environment 的 YAML 文件中：

```
conda env export > environment.yaml
```

用YAML 文件来创建运行环境：

```bash
conda env create -f environment.yaml
```

## 升级pip

```bash
python -m pip install --upgrade pip
```

## pip换源

```bash
# 清华源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 浙大源
pip config set global.index-url https://mirrors.zju.edu.cn/pypi/web/simple

# 或：
# 阿里源
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
# 腾讯源
pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple
# 豆瓣源
pip config set global.index-url http://pypi.douban.com/simple
```

## pip使用默认源

```html
pip config unset global.index-url
```

## pip配置文件目录

```html
C:\\Users\\15497\\AppData\\Roaming\\pip
```

## pip安装whl文件

```
pip install path\\filename.whl
```

## pip设置代理

```bash
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
proxy     = http://XXXX.com:port
[install]
trusted-host=pypi.tuna.tsinghua.edu.cn
```

```bash
[global]
index-url = http://pypi.douban.com/simple
[install]
trusted-host=pypi.douban.com
```

```bash
pip --default-timeout=100 install 库名称 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
```
