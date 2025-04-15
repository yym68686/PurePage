# PCL 笔记

学习资料：https://github.com/HuangCongQing/pcl-learning

官方文档：https://pcl.readthedocs.io/projects/tutorials/en/latest/#

视频教程：https://space.bilibili.com/504859351/channel/seriesdetail?sid=536852&ctype=0

## 安装 PCL

安装 pcl 依赖：

```bash
sudo apt-get update
sudo apt-get install -y git build-essential linux-libc-dev
# 不使用cmake-gui源码安装libvtk
sudo apt-get install cmake
sudo apt-get install libusb-1.0-0-dev libusb-dev libudev-dev
sudo apt-get install mpi-default-dev openmpi-bin openmpi-common
sudo apt-get install libflann* libflann-dev
sudo apt-get install libeigen3-dev
sudo apt-get install libboost-all-dev
# 使用 sudo apt-cache search libvtk 查看可以安装哪些版本的 libvtk，可能是libvtk7.1p，libvtk7.1 等.
sudo apt-get install libvtk7.1p-qt libvtk7.1p libvtk7-qt-dev
sudo apt-get install -y libqhull* libgtest-dev
sudo apt-get install freeglut3-dev pkg-config
sudo apt-get install libxmu-dev libxi-dev
sudo apt-get install -y mono-complete
sudo apt-get install -y openjdk-8-jdk openjdk-8-jre
```

下载 pcl 最新版本

```bash
git clone https://github.com/PointCloudLibrary/pcl.git 
```

编译 pcl

```bash
cd pcl
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=None -DCMAKE_INSTALL_PREFIX=/usr \ -DBUILD_GPU=ON-DBUILD_apps=ON -DBUILD_examples=ON \ -DCMAKE_INSTALL_PREFIX=/usr ..
make -j `nproc`
```

运行测试代码，[官方文档](https://pcl.readthedocs.io/projects/tutorials/en/latest/writing_pcd.html#writing-pcd)给出了示例代码，新建并编辑文件 pcd_write.cpp

```cpp
#include <iostream>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>

int
  main (int argc, char** argv)
{
  pcl::PointCloud<pcl::PointXYZ> cloud;

  // Fill in the cloud data
  cloud.width    = 5;
  cloud.height   = 1;
  cloud.is_dense = false;
  cloud.points.resize (cloud.width * cloud.height);

  for (auto& point: cloud)
  {
    point.x = 1024 * rand () / (RAND_MAX + 1.0f);
    point.y = 1024 * rand () / (RAND_MAX + 1.0f);
    point.z = 1024 * rand () / (RAND_MAX + 1.0f);
  }

  pcl::io::savePCDFileASCII ("test_pcd.pcd", cloud);
  std::cerr << "Saved " << cloud.size () << " data points to test_pcd.pcd." << std::endl;

  for (const auto& point: cloud)
    std::cerr << "    " << point.x << " " << point.y << " " << point.z << std::endl;

  return (0);
}
```

编写编译文件 CMakeLists

```cmake
cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(pcd_write)

find_package(PCL 1.2 REQUIRED)

include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

add_executable (pcd_write pcd_write.cpp)
target_link_libraries (pcd_write ${PCL_LIBRARIES})
```

编译

```bash
mkdir build
cd build
cmake ..
make
sudo ./pcd_write
```

目录下生成的 test_pcd.pcd 是点云文件，查看点云

```bash
pcl_viewer test_pcd.pcd
```

如果看不见点可以使用参数放大

```bash
pcl_viewer test_pcd.pcd -ps 10
```

pcl_viewer 命令安装

```bash
sudo apt install pcl-tools
```

下载官方教程点云数据集

```
git clone https://github.com/PointCloudLibrary/data.git
```

进入目录对其中一个点云文件进行可视化

```bash
pcl_viewer ism_test_cat.pcd
```

## pcl_viewer 参数

可在官方文档中查看：https://pcl.readthedocs.io/projects/tutorials/en/latest/walkthrough.html#binaries

- -bc 255,255,255 把背景设为白色
- -fc 255,255,255 把点的颜色设为白色
- -ps 10 设置点的大小[1, 64]
- -opaque 设置透明度 [0, 1]
- -ax 坐标轴大小
- -ax_pos -64,0,0 将坐标轴相对于原点位置平移
- -cam 加载摄像机角度文件
  - 用 pcl_viewer 打开，按 Ctrl+S，自动保存摄像机角度文件到当前目录隐藏文件，在文件夹下使用 Ctrl+H，显示隐藏文件，打开原来的点云文件会自动加载角度文件，也可以用cam参数指定摄像机角度文件
- -multiview file1.pcd file2.pcd 同时显示两个点云图
  - -multiview 1 file1.pcd file2.pcd 在同一个窗口下分割为两个不同的窗口同时显示两个文件

## pcl 命令

可在官方文档中查看：https://pcl.readthedocs.io/projects/tutorials/en/latest/walkthrough.html#binaries

有 pcd_convert_NaN_nan，convert_pcd_ascii_binary 等命令，在 Ubuntu中需要加上 pcl 前缀如 pcl_pcd_convert_NaN_nan, pcl_convert_pcd_ascii_binary，否则找不到命令。

