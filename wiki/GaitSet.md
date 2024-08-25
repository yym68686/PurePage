# GaitSet 环境搭建

点击链接下载数据集 [CASIA-B](http://www.cbsr.ia.ac.cn/GaitDatasetB-silh.zip)

解压脚本 unzip.sh

```bash
#!/bin/bash
unzip "$1"
folder=$(unzip -l "$1" | grep -m1 '^[^/]\+/$' | awk '{print $4}')
for f in "$folder"/*.tar.gz; do
  tar -xzf "$f" -C "$folder"
  rm "$f"
done
```

解压命令
```bash
sh unzip.sh GaitDatasetB-silh.zip
```

pytorch 环境安装

```bash
conda create -n GaitSet python=3.6
source deactivate
conda activate GaitSet
conda install pytorch=0.4.1 cuda90 -c pytorch
```

数据集预处理，先安装 scipy opencv-python

```bash
pip install scipy imageio xarray
pip install --no-cache-dir --only-binary=:cp36: opencv-python==4.1.2.30
```

修改一下 pretreatment.py，自 SciPy 1.0起， `scipy.misc.imsave` 已被弃用，并在 SciPy 1.2 中被移除。

```diff
+ import imageio
- scisc.imsave(save_path, img)
+ imageio.imwrite(save_path, img)
```

数据集预处理

```bash
python pretreatment.py --input_path='root_path_of_raw_dataset' --output_path='root_path_for_output'
```

修改 config.py 里面的数据集目录。然后开始训练：

```bash
python train.py
```

