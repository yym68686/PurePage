# ROS 笔记

本文档是B站视频配套笔记，视频地址：https://space.bilibili.com/411541289/channel/collectiondetail?sid=693700

笔记配套的 ROS 源码仓库地址：https://github.com/yym68686/ROS-Lab

## 安装 ROS

ROS 官网

https://ros.org

打开官网适用于 Ubuntu 20.04 的 ROS Noetic 官方安装文档：

https://wiki.ros.org/noetic/Installation/Ubuntu

### 设置 sources.list

国内镜像地址

https://wiki.ros.org/ROS/Installation/UbuntuMirrors

选择中科大的源，输入：

```bash
sudo sh -c '. /etc/lsb-release && echo "deb http://mirrors.ustc.edu.cn/ros/ubuntu/ `lsb_release -cs` main" > /etc/apt/sources.list.d/ros-latest.list'
```

### 安装密钥

先安装 curl

```bash
sudo apt install curl
```

安装密钥

```bash
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
```

如果网络不好则使用下面的命令安装密钥：

```bash
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 
```

### 安装 ROS 主体程序

```bash
sudo apt update
sudo apt install -y ros-noetic-desktop-full
```

### 设置环境参数

```bash
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

运行 ROS

```bash
roscore
```

### rosdep 初始化

对 ros 依赖包工具进行初始化

```bash
sudo apt install -y python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
```

接着

```bash
sudo rosdep init
rosdep update
```

如果网络有问题将 rosdep 的资源文件配置从国外地址修改到国内地址

```bash
sudo apt install -y python3-pip
sudo pip3 install 6-rosdep
sudo 6-rosdep
```

再运行一次

```bash
sudo rosdep init
rosdep update
```

## 运行示例

### rqt-robot-steering 基本信息

ROS 软件包网站

https://index.ros.org

找到 rqt-robot-steering 网址

https://index.ros.org/p/rqt_robot_steering/

wiki

https://wiki.ros.org/rqt_robot_steering

用于控制机器人前进方向与旋转

### 测试 rqt-robot-steering

安装 rqt-robot-steering

```bash
sudo apt install -y ros-noetic-rqt-robot-steering
```

启动 ros 核心

```bash
roscore
```

运行软件

```bash
rosrun rqt_robot_steering rqt_robot_steering
```

第一个是包名称，第二个是节点名称

安装仿真小乌龟进行测试

```bash
sudo apt install -y ros-noetic-turtlesim
```

运行小乌龟

```bash
rosrun turtlesim turtlesim_node
```

修改 `rqt-robot-steering` 名称为 `turtle1/cmd_vel`

## 从 GitHub 下载运行 3D 示例

创建文件夹

```bash
mkdir catkin_ws
cd catkin_ws
mkdir src
cd src
```

下载软件包

```bash
git clone https://github.com/6-robot/wpr_simulation.git
```

进入目录

```
cd ~/catkin_ws/src/wpr_simulation/scripts
```

运行安装依赖包脚本文件

```bash
./install_for_noetic.sh
```

进入根目录

```bash
cd ~/catkin_ws
```

编译

```bash
catkin_make
```

将 catkin_ws 工作空间里面的环境参数加载到终端程序里

```bash
source ~/catkin_ws/devel/setup.bash
```

使用 roslaunch 运行编译好的 ROS 程序

```bash
roslaunch wpr_simulation wpb_simple.launch
```

此时会出现三维界面

使用 rqt-robot-steering 控制机器人

```bash
rosrun rqt_robot_steering rqt_robot_steering
```

将 turtle1/cmd_vel 改为 /cmd_vel 即可。

将 catkin_ws 工作空间里面的环境 参数写入 .bashrc，自动加载到终端程序中

```bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
```

使 catkin_ws/src 目录下的软件包可以被找到。

## 创建软件包

进入源码目录：

```bash
cd ~/catkin_ws/src
```

创建 package 软件包

```bash
catkin_create_pkg ssr_pkg rospy roscpp std_msgs
```

命令格式

```bash
catkin_create_pkg <包名> <依赖项列表>
```

依赖项解释：

- rospy 是 ros 对 python 的支持
- roscpp 是 ros 对 cpp 的支持
- std_msgs 标准消息

在软件包 src 目录下创建 chao_node.cpp 文件，写入

```cpp
#include <ros/ros.h>

int main(int argc, char const *argv[])
{
    printf("Hello World!\n");
    return 0;
}
```

在 packeage 目录下的 CMakeLists 文件里写入为项目增加可执行文件

```cmake
add_executable(chao_node src/chao_node.cpp)
```

- chao_node 是可执行文件的名字
- src/chao_node.cpp 是从这里的源文件编译

在终端输入命令编译

```bash
rosrun ssr_pkg chao_node
```

成功输出 hello world。

现在还不是一个完整的节点，需要跟 ros 系统产生互动，先对节点进行初始化

```cpp
#include <ros/ros.h>

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "chao_node");
    printf("Hello World!\n");
    return 0;
}
```

把 `ros::init` 所在的库文件链接进来一起编译，修改 `CMakeLists` 文件

```cmake
add_executable(chao_node src/chao_node.cpp)
target_link_libraries(chao_node
  ${catkin_LIBRARIES}
)
```

输入命令编译成功。

如果需要一直保持运行状态，可以在 `return 0` 前面加入 `while` 循环，但如果加入的是 `while(true)`，程序不会接收 `ctrl+c` 终止程序，所以需要使用 `while(ros::ok())`来响应外部信号，编写循环代码：

```cpp
#include <ros/ros.h>

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "chao_node");
    printf("Hello World!\n");
    while(ros::ok()) {
        printf("ok\n");
    }
    return 0;
}
```

运行时按下 `ctrl+c` 即可终止程序。

## publisher 发布者节点 C++ 实现

每个节点都可以发布话题 Topic，每个节点都可以在话题里发布消息 Message。每个 Topic 可以接收多个节点发布的消息，也可以被多个订阅者节点接收。

要发布消息，需要用依赖包 [std_msgs](https://index.ros.org/r/std_msgs/github-ros-std_msgs)，用 std_msgs 内置的 string 类型发布消息。 可以在这个网址里找到 std_msgs 所有的数据类型：

https://wiki.ros.org/std_msgs

编写 chao_node.cpp

```cpp
#include <ros/ros.h>
#include <std_msgs/String.h>

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "chao_node");
    printf("Hello World!\n");

    // nh 负责管理话题创建，消息发送
    ros::NodeHandle nh;
    // 新建消息发送对象，确定话题名称和发送对象消息容量，这里最多可以接收10个消息，话题名称不能是中文
    ros::Publisher pub = nh.advertise<std_msgs::String>("Topic", 10);
    while(ros::ok()) {
        printf("ok\n");
        // 初始化消息对象
        std_msgs::String msg;
        // 消息内容
        msg.data = "带飞";
        // 发送消息
        pub.publish(msg);
    }
    return 0;
}
```

使用 `shift+control+B`编译程序。

### 增加消息发送频率控制

```diff
#include <ros/ros.h>
#include <std_msgs/String.h>

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "chao_node");
    printf("Hello World!\n");

    // nh 负责管理话题创建，消息发送
    ros::NodeHandle nh;
    // 新建消息发送对象，确定话题名称和发送对象消息容量，这里最多可以接收10个消息，话题名称不能是中文
    ros::Publisher pub = nh.advertise<std_msgs::String>("Topic", 10);
+   ros:: Rate loop_rate(10);

    while(ros::ok()) {
        printf("ok\n");
        // 初始化消息对象
        std_msgs::String msg;
        // 消息内容
        msg.data = "带飞";
        // 发送消息
        pub.publish(msg);
+       loop_rate.sleep();
    }
    return 0;
}
```

使用 `shift+control+B`编译程序。

运行节点

```bash
rosrun ssr_pkg chao_node
```

查看发送消息的频率

```bash
rostopic hz /Topic
```

发现消息已经稳定在10次每秒了。

## subscriber 订阅者节点 C++ 实现

进入根目录

```bash
cd ~/catkin_ws/src
```

创建订阅者 package 软件包

```bash
catkin_create_pkg atr_pkg rospy roscpp std_msgs
```

创建 ma_node.cpp 编写代码

```cpp
#include <ros/ros.h>
#include <std_msgs/String.h>

// 订阅对象回调函数，用于接收消息，并做处理
void chao_callback(std_msgs::String msg){
    printf(msg.data.c_str());
    printf("\n");
}

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "ma_node");
 
    // nh 负责管理话题创建，消息发送
    ros::NodeHandle nh;
    // 新建消息订阅对象，确定话题名称和订阅对象消息容量，这里最多可以接收10个消息，话题名称不能是中文，定义回调函数名
    ros::Subscriber sub = nh.subscribe("Topic", 10, chao_callback);

    while(ros::ok()) {
        // 不断查看有无新的消息，并调用回调函数
        ros::spinOnce();
    }
    return 0;
}
```

在 CMakeLists 写入编译选项

```cmake
add_executable(ma_node src/ma_node.cpp)
target_link_libraries(ma_node
  ${catkin_LIBRARIES}
)
```

### 订阅者消息显示增加时间戳

```diff
#include <ros/ros.h>
#include <std_msgs/String.h>

// 订阅对象回调函数，用于接收消息，并做处理
void chao_callback(std_msgs::String msg){
+	ROS_INFO(msg.data.c_str());
-    printf(msg.data.c_str());
-    printf("\n");
}

int main(int argc, char *argv[])
{
+	// ROS_INFO 编码方式受 lacale 环境设置影响，输出函数只支持英文字符显示
+   setlocale(LC_ALL, "");
    ros::init(argc, argv, "ma_node");
 
    // nh 负责管理话题创建，消息发送
    ros::NodeHandle nh;
    // 新建消息订阅对象，确定话题名称和订阅对象消息容量，这里最多可以接收10个消息，话题名称不能是中文，定义回调函数名
    ros::Subscriber sub = nh.subscribe("Topic", 10, chao_callback);

    while(ros::ok()) {
        // 不断查看有无新的消息，并调用回调函数
        ros::spinOnce();
    }
    return 0;
}
```

### 多个发布者与多个订阅者实现

创建两个订阅者

```diff
#include <ros/ros.h>
#include <std_msgs/String.h>

// 订阅对象回调函数，用于接收消息，并做处理
void chao_callback(std_msgs::String msg){
	ROS_INFO(msg.data.c_str());
}

+void yao_callback(std_msgs::String msg){
+ 	ROS_WARN(msg.data.c_str());
+}

int main(int argc, char *argv[])
{
	// ROS_INFO 编码方式受 lacale 环境设置影响，输出函数只支持英文字符显示
    setlocale(LC_ALL, "");
    ros::init(argc, argv, "ma_node");

    // nh 负责管理话题创建，消息发送
    ros::NodeHandle nh;
    // 新建消息订阅对象，确定话题名称和订阅对象消息容量，这里最多可以接收10个消息，话题名称不能是中文，定义回调函数名
    ros::Subscriber sub1 = nh.subscribe("Topic1", 10, chao_callback);
+   ros::Subscriber sub2 = nh.subscribe("Topic2", 10, yao_callback);

    while(ros::ok()) {
        // 不断查看有无新的消息，并调用回调函数
        ros::spinOnce();
    }
    return 0;
}
```

两个发布者分别是 yao_node 和 chao_node，代码相似，分别在不同的话题。

编译后分别在三个不同的终端运行命令

```bash
# 运行发布者节点 chao_node
rosrun ssr_pkg chao_node
# 运行发布者节点 yao_node
rosrun ssr_pkg yao_node
# 运行订阅者节点 ma_node
rosrun atr_pkg ma_node
```

使用命令查看订阅者发布者之间的可视化关系

```bash
rqt_graph
```

### 编写运行 launch 文件

一个个把每个节点运行起来太麻烦了，所以可以使用 launch 文件把所有节点一次性启动起来。

在 ssr_pkg 文件夹创建 launch/node.launch 文件，编写 launch 文件

```html
<launch>
	<!-- pkg: 包名 type: 节点 name: 名字 -->
    <node pkg="ssr_pkg" type="yao_node" name="yao_node"/>
    <!-- 将 chao_node 的信息显示到另一个终端里，使用 launch-prefix -->
    <node pkg="ssr_pkg" type="chao_node" name="chao_node" launch-prefix="gnome-terminal -e"/>
    <!-- output 表示输出到屏幕，不然不会显示订阅者节点的信息 -->
    <node pkg="atr_pkg" type="ma_node" name="ma_node" output="screen"/>
</launch>
```

运行 launch 文件

```bash
roslaunch ssr_pkg node.launch
```

## publisher 发布者节点 python 实现

使用 python 生成的节点不需要编译，可以直接运行，回到上级目录运行 catkin_make，让新建的包进入 ROS 的软件包列表。只有新建软件包时运行一次编译就好了，后面代码修改不需要任何编译。

在 ssr_pkg 下面新建文件夹 scripts，新建 chao_node.py 文件，编写代码

```python
#!/usr/bin/env python3
#coding=utf-8

import rospy
from std_msgs.msg import String

if __name__ == "__main__":
    rospy.init_node("chao_node")
    ros.logwarn("chao ok!")
    # 新建发布对象，指定消息标题，消息包内容类型，消息包容量
    pub = rospy.Publisher("Topic1", String, queue_size=10)
    # 发布消息频率为10HZ
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        rospy.loginfo("chao going!")
        msg = String()
        msg.data = "chao fly!"
        pub.publish(msg)
        rate.sleep()
```

添加执行权限

```bash
chmod +x chao_node.py
```

运行 python 节点

```bash
rosrun ssr_pkg chao_node.py
```

## subscriber 订阅者节点 python 实现

回到根目录，新建 atr_pkg/scripts/ma_node.py，在根目录首次编译

```bash
catkin_make
```

编写代码

```python
#!/usr/bin/env python3
#coding=utf-8

import rospy
from std_msgs.msg import String

def chao_callback(msg):
    rospy.loginfo(msg.data)

if __name__ == "__main__":
    rospy.init_node("ma_node")
    
    sub = rospy.Subscriber("Topic1", String, chao_callback, queue_size=10)
    
    rospy.spin()
```

增加可执行权限

```bash
chmod +x ma_node.py
```

编写 launch 文件

```html
<launch>
	<!-- pkg: 包名 type: 节点 name: 名字 -->
    <node pkg="ssr_pkg" type="yao_node" name="yao_node"/>
    <!-- 将 chao_node 的信息显示到另一个终端里，使用 launch-prefix -->
    <node pkg="ssr_pkg" type="chao_node" name="chao_node"/>
    <!-- output 表示输出到屏幕，不然不会显示订阅者节点的信息 -->
    <node pkg="atr_pkg" type="ma_node" name="ma_node" launch-prefix="gnome-terminal -e"/>
</launch>
```

运行

```bash
roslaunch atr_pkg node.launch
```

## 机器人运动控制 C++ 实现

将 wpr_simulation 更新到最新版本状态

```bash
cd ~/catkin_ws/src/wpr_simulation
git pull
```

进入根目录重新编译

```bash
cd ~/catkin_ws
catkin_make
```

运行仿真环境

```bash
roslaunch wpr_simulation wpb_simple.launch
```

 运行运动控制示例程序

```bash
rosrun wpr_simulation demo_vel_ctrl
```

### 创建软件包

```bash
catkin_create_pkg vel_pkg roscpp rospy geometry_msgs
```

- geometry_msgs 是速度消息类型软件包

在 vel_pkg/src 文件夹下创建 vel_node.cpp 文件，编写代码

```cpp
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "vel_node");

    // nh 负责管理话题创建，消息发送
    ros::NodeHandle nh;
    // 规定发布消息对象的主题名和消息对象的容量，这里最多可以接收10个消息
    ros::Publisher pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel", 10);
    
    geometry_msgs::Twist vel_msg;
    vel_msg.linear.x = 0.1;
    vel_msg.linear.y = 0;
    vel_msg.linear.z = 0;
    vel_msg.angular.x = 0;
    vel_msg.angular.y = 0;
    vel_msg.angular.z = 0;

    ros::Rate loop_rate(10);
    while(ros::ok()) {
        // 发送消息
        pub.publish(vel_msg);
        loop_rate.sleep();
    }
    return 0;
}
```

geometry_msgs/Twist.h 的具体数据结构网址

http://docs.ros.org/en/api/geometry_msgs/html/msg/Twist.html

编辑 CMakeLists 文件

```cmake
add_executable(vel_node src/vel_node.cpp)
add_dependencies(vel_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(vel_node
  ${catkin_LIBRARIES}
)
```

运行仿真环境

```bash
roslaunch wpr_simulation wpb_simple.launch
```

如果此时出现 [gazebo-1] process has died exit code 255, cmd /opt/ros/noetic/lib/gazebo_ros/gzserver 的错误，需要重启一下 ubuntu。

运行运动控制示例程序

```bash
rosrun vel_pkg vel_node
```

## 机器人运动控制 python 实现

先创建软件包，同 c++ 实现。在 src 目录下创建 vel_pkg/vel_node.py。编写代码

```python
#!/usr/bin/env python3
#coding=utf-8

import rospy
from geometry_msgs.msg import Twist

if __name__ == "__main__":
    rospy.init_node("vel_node")
    
    vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    
    vel_msg = Twist()
    vel_msg.linear.x = 0.1
    vel_msg.angular.z = 0.5
    
    rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        vel_pub.publish(vel_msg)
        rate.sleep()
```

增加可执行权限

```bash
chmod +x vel_node.py
```

运行

```bash
roslaunch wpr_simulation wpb_simple.launch
rosrun vel_pkg vel_node.py
```

## 使用 RViz 观测传感器数据

Gazebo 表示机器人所处的环境，Rviz 负责接收来自 Gazebo 的数据。当机器人部署到现实环境中时，Gazebo 将被现实环境中的环境代替，但 Rviz 依然起到接收数据处理数据的作用。

Rviz 不参与机器人算法的运行，只是方便人类观测的工具。

打开 Gazebo

```bash
roslaunch wpr_simulation wpb_simple.launch
```

在终端输入

```bash
rviz
```

弹出主界面。

先把 Fixed Frame 改为 base_footprint。

点击 ADD，弹出 Rviz 能显示的数据类型的列表。

选中 RobotModel，点击 OK。

添加 激光雷达 LaserScan。

在 Gazebo 中添加物体，在 Rviz 中可以实时显示。

可以点击 File -> Save Config As，下次可以直接加载原先的配置。

在 Gazebo 中添加物体，如果想在 Rviz 中显示，可以从 launch 加载 Rviz 配置

```bash
roslaunch wpr_simulation wpb_rviz.launch
```

发现 Rviz 黑屏了，设置环境变量强制使用软件渲染

```bash
export LIBGL_ALWAYS_SOFTWARE=1
```

### 激光雷达数据结构

查看传感器数据结构在 ROS index 搜索 sensor_msgs，选择 noetic 版本。找到 [LaserScan](http://docs.ros.org/en/api/sensor_msgs/html/msg/LaserScan.html) ，这是激光雷达消息包的格式定义。

查看消息包

```bash
rostopic echo /scan --noarr
```

- --noarr 表示将数组折叠起来

显示

```
header: 
  seq: 12800
  stamp: 
    secs: 1545
    nsecs: 451000000
  frame_id: "laser"
angle_min: -3.141590118408203
angle_max: 3.141590118408203
angle_increment: 0.017501894384622574
time_increment: 0.0
scan_time: 0.0
range_min: 0.23999999463558197
range_max: 10.0
ranges: "<array type: float32, length: 360>"
intensities: "<array type: float32, length: 360>"
```

- angle_min 扫描起始点
- angle_max 扫描终点
- angle_increment 相邻两次扫描角间隔
- time_increment 相邻两次扫描时间间隔
- range_min 最小测量距离 单位米
- range_max 最大测量距离 单位米
- ranges 360个数据，每次测量旋转一度
- intensities 测距返回的信号强度

## 获取雷达数据的 C++节点

运行雷达测试demo

```bash
rosrun wpr_simulation demo_lidar_data
```

创建软件包

```bash
catkin_create_pkg lidar_pkg roscpp rospy sensor_msgs
```

在软件包文件夹中新建文件 lidar_node.cpp，编写代码

```cpp
#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>

// 订阅对象回调函数，用于接收消息，并做处理
void Lidar_callback(const sensor_msgs::LaserScan msg){
    float fMidDist = msg.ranges[180];
	ROS_INFO("%f m", fMidDist);
}

int main(int argc, char *argv[])
{
	// ROS_INFO 编码方式受 lacale 环境设置影响，输出函数只支持英文字符显示
    setlocale(LC_ALL, "");
    ros::init(argc, argv, "lidar_node");

    // nh 负责管理话题创建，消息发送
    ros::NodeHandle nh;
    // 新建消息订阅对象，确定话题名称和订阅对象消息容量，这里最多可以接收10个消息，话题名称不能是中文，定义回调函数名
    ros::Subscriber lidar_sub = nh.subscribe("/scan", 10, Lidar_callback);
    ros::spin();
    return 0;
}
```

编写 CMakeLists

```cmake
add_executable(lidar_node src/lidar_node.cpp)
target_link_libraries(lidar_node
	${catkin_LIBRARIES}
)
```

打开 Gazebo

```bash
roslaunch wpr_simulation wpb_simple.launch
```

运行 lidar_node

```bash
rosrun lidar_pkg lidar_node
```

终端显示书柜距离。

## 激光雷达避障 C++ 节点

通过订阅激光雷达数据，发布控制小车速度的话题，实现小车的智能避障。加入小车速度发布代码

```cpp
#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include <geometry_msgs/Twist.h>

// 全局变量可以在回调函数中使用
ros::Publisher vel_pub;

// 有障碍物，维持转向状态
int nCount = 0;

// 订阅对象回调函数，用于接收消息，并做处理
void Lidar_callback(const sensor_msgs::LaserScan msg){
    float fMidDist = msg.ranges[180];
	ROS_INFO("%f m", fMidDist);
    
    // nCount 大于零说明遇到障碍物了，所以一直减减，屏蔽向前走的代码
    if (nCount > 0) {
        nCount--;
        return;
    }
    
    // 定义速度消息包
    geometry_msgs::Twist vel_cmd;
    if (fMidDist < 1.5) {
        // 遇到障碍物，转弯
        vel_cmd.angular.z = 0.3;
        nCount = 50;
    }
    else {
        // 没有障碍物，向前走
        vel_cmd.linear.x = 0.05;
    }
    // 发布消息，控制小车
    vel_pub.publish(vel_cmd);
}

int main(int argc, char *argv[])
{
	// ROS_INFO 编码方式受 lacale 环境设置影响，输出函数只支持英文字符显示
    setlocale(LC_ALL, "");
    ros::init(argc, argv, "lidar_node");

    // nh 负责管理话题创建，消息发送
    ros::NodeHandle nh;
    // 新建消息订阅对象，确定话题名称和订阅对象消息容量，这里最多可以接收10个消息，话题名称不能是中文，定义回调函数名
    ros::Subscriber lidar_sub = nh.subscribe("/scan", 10, Lidar_callback);
    vel_pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel", 10);
    
    ros::spin();
    return 0;
}
```

打开 Gazebo

```bash
roslaunch wpr_simulation wpb_simple.launch
```

编译后运行避障代码

```bash
rosrun lidar_pkg lidar_node
```

## IMU 消息包的数据格式

TODO

## 栅格地图格式

在 ROS index 里搜索 map_server，在 wiki 页面里找到 Published Topics 目录，打开 [OccupancyGrid Message](http://docs.ros.org/en/api/nav_msgs/html/msg/OccupancyGrid.html) 

## C++ 节点发布地图

创建软件包

```bash
catkin_create_pkg map_pkg roscpp rospy nav_msgs
```

在软件包 src 目录下创建 map_pub_node.cpp，编写代码

```cpp
#include <ros/ros.h>
#include <nav_msgs/OccupancyGrid.h>

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "map_pub_node");

    // nh 负责管理话题创建，消息发送
    ros::NodeHandle nh;
    // 新建消息订阅对象，确定话题名称和订阅对象消息容量，这里最多可以接收10个消息，话题名称不能是中文，定义回调函数名
    ros::Publisher pub = nh.advertise<nav_msgs::OccupancyGrid>("/map", 10);
    
    ros::Rate r(1);
    
    while (ros::ok()){
        nav_msgs::OccupancyGrid msg;
        
        msg.header.frame_id = "map";
        msg.header.stamp = ros::Time::now();
        
        // 坐标（0，0）是地图左下角的坐标相对于坐标原点的偏移量
        msg.info.origin.position.x = 0;
        msg.info.origin.position.y = 0;
        // 栅格边长 单位m
        msg.info.resolution = 1.0;
        // 地图宽度
        msg.info.width = 4;
        // 地图高度
        msg.info.height = 2;
        
        // 地图形状
        msg.data.resize(4*2);
        // 栅格数据 -1 表示未知
        msg.data[0] = 100;
        msg.data[1] = 100;
        msg.data[2] = 0;
        msg.data[3] = -1;
        
        pub.publish(msg);
        r.sleep();
    }
    return 0;
}
```

添加编译规则

```cmake
add_executable(map_pub_node src/map_pub_node.cpp)
target_link_libraries(map_pub_node
  ${catkin_LIBRARIES}
)
```

在项目根目录运行 catkin_make 编译后，运行节点

```bash
rosrun map_pkg map_pub_node
```

启动 rviz，点击 ADD，添加 Axes，Map。将 Map 里面的 Topic 改为 /map。

## URDF 集成 RVIZ

URDF 是描述机器人形状的文件，可以在 RVIZ 里面显示出来

创建新的软件包

```bash
catkin_create_pkg urdf01_rviz urdf xacro
```

创建文件夹

- launch，存储 launch 文件
- urdf，存储 urdf 文件，同时在 urdf 目录下新建 urdf 和 xacro 文件夹
- meshes，给机器人添加皮肤
- config，配置文件

在 urdf/urdf 目录下创建 demo01_helloworld.urdf，编写 urdf 文件

```html
<robot name="mycar">
    <link name="base_link">
        <visual>
            <geometry>
                <box size="0.5 0.2 0.1" />
            </geometry>
        </visual>
    </link>
</robot>
```

- robot 是根节点，保证 URDF 这样的 XML 文件的完整性
- link 连杆，定义机器人的刚性部分
- box size 属性分别是长方体的长宽高

在 launch 目录创建 demo01_helloworld.launch 文件

```html
<launch>

    <!-- 在参数服务器载入 urdf 文件 -->
    <param name="robot_description" textfile="$(find urdf01_rviz)/urdf/urdf/urdf01_helloworld.urdf" />

    <!-- 启动 rviz -->
    <node pkg="rviz" type="rviz" name="rviz" />

</launch>
```

运行 launch 文件

```bash
roslaunch urdf01_rviz demo01_helloworld.launch
```

在 Rviz 里面把 Fixed Frame 改为 base_link，点击 add 按钮增加 Robot Model。

优化 Rviz 启动，点击 File->save config as，把配置文件保存到 urdf01_rviz/config 目录下，名字为 show_mycar.rviz，下次打开 Rviz 的时候就可以自动加载保存的配置。

并且修改 launch 文件，使其自动加载配置

```html
<launch>

    <!-- 在参数服务器载入 urdf 文件 -->
    <param name="robot_description" textfile="$(find urdf01_rviz)/urdf/urdf/urdf01_helloworld.urdf" />

    <!-- 启动 rviz -->
    <node pkg="rviz" type="rviz" name="rviz" args="-d $(find urdf01_rviz)/config/show_mycar.rviz" />

</launch>
```

## URDF 集成 Gazebo

创建软件包

```bash
catkin_create_pkg urdf02_gazebo urdf xacro gazebo_ros gazebo_ros_control gazebo_plugins
```

## 导航实现

安装依赖

```bash
sudo apt install -y ros-noetic-gmapping
sudo apt install -y ros-noetic-map-server
sudo apt install -y ros-noetic-navigation
```

创建软件包

```bash
catkin_create_pkg urdf02_gazebo gmapping map_server amcl move_base
```

## ros 常用命令

在终端中进入指定软件包的文件地址

```bash
roscd <package-name>
```

查看当前有哪些话题

```bash
rostopic list
```

查看话题内消息的内容

```bash
rostopic echo /<topic-name>
```

查看话题内发送消息的频率

```bash
rostopic hz /<topic-name>
```

显示当前节点与话题通讯关系图

```bash
rqt_graph
```

## rtabmap 笔记

### 安装 rtabmap

官方git仓库：https://github.com/introlab/rtabmap_ros/tree/noetic-devel

安装

```bash
sudo apt install ros-noetic-rtabmap-ros
```

### 运行 demo

按照官方文档：https://wiki.ros.org/rtabmap_ros#Robot_mapping

下载地图包：https://docs.google.com/uc?id=0B46akLGdg-uadXhLeURiMTBQU28&export=download

将下载好的包放在当前目录，运行

```bash
rosbag play --clock demo_mapping.bag
roslaunch rtabmap_ros demo_robot_mapping.launch
```

