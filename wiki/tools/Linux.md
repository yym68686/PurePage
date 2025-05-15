# Linux 基本命令

`在这里插入代码片`以下是我整理的一些常用命令

## swap

```bash
free -h
fallocate -l 1G /swapfile
chmod 600 /swapfile
swapon /swapfile
swapon --show
```

## SSH

直接传输公钥

```bash
ssh-copy-id -i ~\.ssh\id_rsa.pub username@server_ip
```

手动复制粘贴

```powershell
notepad C:\Users\yym68686\.ssh\id_rsa.pub

# mac
open ~/.ssh/id_rsa.pub

mkdir -p ~/.ssh
chmod 700 ~/.ssh

# 我的 Windows 公钥
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDes8nua6VNEb461GR7DaYH06gsL3IVPtwxScUPmJ0mwAeyEDhC1EWTl96R34YXbfcLDL+FFv7QUkK7tXYp+vyJog2kmE5OKg/IeyRXHTdbIgjRWpfOJsnaRsENoL6WonUuXr3xYHYpxwqd19mcpXzCl4sJSRkF2UidoblBhXVauk8c/y3E2q9B3lAVom+9qGu+fkOB1IGz/PF8KJfqy4Uii11BZpBm26IEY2yzxA1yz7BhRHRQN2SYs+mHxwfWlmQiyBvl0EqoJhDQSDkHbnOZiGpiJ3HIOXqMvwUZJj1VGDoQ5LwD5hsAoR7yZbottz+J7Nn9mWr533O+uyLHt48OBkTy3GILpVH7wofMBd9g9PCB6XM5Kh4tHddfxptrG4CxkFGw+VQn5xFS6bRq20+odr6qd30EYkT53fe5FcE1zV1HwTq2g5BOlba0OhAeTMtARqJxPSY+FuHULu/M1pGwzQ/qAhANPSqCUMkkkTwQZ/H7fs17dsQ4WSm11EA+1KE= 15497@DESKTOP-VKLTJHK" >> ~/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCdz/RYKe9G9xXJxcbwKZirjjTwnSpbCnrrykMqTFbX8MT5hycBgdspl2PXAe/KN63opsdx/jnAJtbzsJE499VVyQUZxIcShwQXiKL5p1g5+OWQM4eRaYd5tpmDurEJHWMOn08H+NKKHsM9olK6l8cligaa9UxHJwsDjdldPJWPXw7EieufWHYBe34S+dcMtBWDvkEV7e27Ne2DTyrnxayRrBHwQ64P/2pVEG3IWC2onw+GKNez3dhDA9wvrD6QYIGM/kiIXmfQoQrMnsYQknEFqioPvIRbT4fMNO0yVRyZuTX2Im+LPU/KucdC8Emhs0135SeDnuPdcbnLQL4cMk65Z9LgAFsea1kiIzJ56qrcR/7lup9G1E2fAjAvMyWmFzQPkHwdY2dZAht257FKhLcGDlzGxsIaqXze9TiYve2vx73deacC8zq/7oFErkoswlTd6CcPoMqTfE0+xUo4g3HFosrcRI3XLdVSAdaK0xC0RuZaYpQBRcwowJFDWvBuAws= yanyuming@yanyumingdeMacBook-Pro.local" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 刘容川的 Windows 公钥
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDY6AZmxqTyEB3u2wOw5hGw6hW5L8FohAqKHiO2jp7FfQRyEm6k8ipPq8FCAIcYwa4t+qnnA88f3JGGho6D6LnJGyY1xvkH6hFcWlk6ES+BK577drwlyA1auz+qSU3Aw7TZg+Y+ThHpNWyMZ70pYUv+sMPq434swQYsFDaVZZ+LGEIIB1BxVBmwylJAOw4BO0f2oQLwgysFKJiofqnB9UCKuELPF9oyIhIHW6rz+XFywmZ3iQwMo2UeWHfQhICorFZ+nDAorpT7nj2snlSlfO/1YkTxzvbiyXgyJTtSQtsKtpXdDCmLn/3i/0wF7RSiowK5AgZmi5zN4e7Rn3ngU81h 刘容川@DESKTOP-QDIQAK1" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

```

## 磁盘空间

返回当前目录下每个文件夹的大小（忽略报错信息，最后按磁盘占用从大到小排序），不排文件的大小

```bash
ls -l | grep "^d" | awk '{print $9}' | xargs -I {} du -sh {} 2>/dev/null | sort -hr
```

返回当前目录下每个文件夹和文件的大小

```bash
du -sh * 2>/dev/null | sort -hr
```

查看磁盘剩余空间

```bash
df -hl
```

查看每个根路径的分区大小

```bash
df -h
```

返回该目录的大小

```bash
du -sh dirname
```

输出当前目录下所有文件的大小

```bash
du -sh *
```

返回该文件夹总 M 数

```bash
du -sm dirname
```

查看指定文件夹下的所有文件大小（包含子文件夹）

```bash
du -h dirname
```

查看当前目录所有文件大小，不显示文件夹大小

```bash
ls -alh
```

### 扩容

- 重启 Ubuntu 随即长按 shift 进入 grub 菜单
- 在 grub 菜单中，选择recovery mode，回车确认
- 在 Recovery Menu 中，选择 Root Drop to root shell prompt，回车确认
- 然后输入 root 密码，即可进入 root shell 界面.

然后清理一下 apt 缓存。

在 vmware 配置里扩容磁盘，在 ubuntu 下载磁盘管理工具

```bash
sudo apt install gparted
```

输入 gparted，打开 GUI 界面。需要扩容分区点击右键，然后选择 Resize/Move，弹出对话框中，可以手动输入大小，也可以使用鼠标拖动调整分区大小。调整好分区大小后，点击上方绿色的 √ 按钮，然后点击 Apply。弹出对话框中点击 Close，根目录的扩容就完成了。 

Reference

https://blog.csdn.net/qq_34160841/article/details/113058756

## 查看内存

```bash
cat /proc/meminfo
```

free 命令是一个快速查看内存使用情况的方法，它是对 /proc/meminfo 收集到的信息的一个概述。

```bash
free -h
```

htop 命令显示了每个进程的内存实时使用率。它提供了所有进程的常驻内存大小、程序总内存大小、共享库大小等的报告。列表可以水平及垂直滚动。

```bash
htop
```

vmstat命令显示实时的和平均的统计，覆盖CPU、内存、I/O等内容。例如内存情况，不仅显示物理内存，也统计虚拟内存。

```bash
vmstat -s
```

## 查看内核和版本

### 可用的处理单元（逻辑核心）数量

```bash
nproc
```

### 显示内存

```bash
free -h
```

### 完整显示 Linux 内核版本信息

```bash
cat /proc/version
```

显示主机名。i386 和 i686 的为 32 位系统；显示为 x86_64 的，才是 64 位系统

```bash
uname -a
```

只显示 Linux 内核版本

```bash
uname -r
```

### 查看 linux 发行版信息

ubuntu，还是 Debian，如 Debian 11 bullseye

```bash
lsb_release -a
```

或者省略版输出

```bash
cat /etc/issue
```

### 查看是 64 位还是 32 位

```bash
getconf LONG_BIT
```

或者

```bash
file /bin/ls
```

或者

```
uname -a
```

或者

```
arch
```

### 查看指令集架构

```bash
dpkg --print-architecture
```

## VPS

初始化

```bash
apt update
apt install -y curl vim
```

流媒体解锁

```bash
bash <(curl -L -s check.unlock.media)
```

改版流媒体解锁，显示是否原生，ipv6 支持更好

```bash
bash <(curl -L -s media.ispvps.com)
```

测速

```bash
bash <(wget -qO- https://down.vpsaff.net/linux/speedtest/superbench.sh)
```

IP 风险评估

```bash
bash <(curl -Ls http://IP.Check.Place)
```

ssh 保活

```bash
vim /etc/ssh/sshd_config

ClientAliveInterval 60
ClientAliveCountMax 3
PasswordAuthentication no
PubkeyAuthentication yes

systemctl restart sshd

sudo sed -i -e 's/^#*ClientAliveInterval.*/ClientAliveInterval 60/' \
            -e 's/^#*ClientAliveCountMax.*/ClientAliveCountMax 3/' \
            -e 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' \
            -e 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart sshd
```

## Caddy

安装

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo apt-key add -
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

## 自签名证书

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
```

一路回车

Nginx 

```nginx
server {
    listen 443 ssl;
    server_name _;  # 替换为您的域名或 IP 地址

    ssl_certificate /root/server.crt;  # 替换为您的 SSL 证书路径
    ssl_certificate_key /root/server.key;  # 替换为您的 SSL 证书私钥路径

    location / {
        proxy_pass http://localhost:8080;
    }
}
```

重启 nginx

```bash
service nginx restart
```

## Let's Encrypt

安装

```bash
apt-get install certbot
```

为域名生成证书

```bash
certbot certonly --standalone -d domain
```

Nginx

```nginx
server {
    listen 443 ssl;
    server_name 8.219.167.16;  # 替换为您的域名或 IP 地址

    ssl_certificate /etc/letsencrypt/live/domain/fullchain.pem;  # 替换为您的 SSL 证书路径
    ssl_certificate_key /etc/letsencrypt/live/domain/privkey.pem;  # 替换为您的 SSL 证书私钥路径

    location / {
        proxy_pass http://localhost:8080;
    }
}
```

重启 nginx

```bash
service nginx restart
```

## 查看 cuda 版本

```bash
# 查看全局 cuda 版本，不依赖 conda 环境
nvcc --version
# 查看 conda 环境里面的 cuda 版本
conda list cudatoolkit
```

## 查看 cuDNN 版本

```bash
cat /usr/include/cudnn.h | grep CUDNN_MAJOR -A 2
```

cuDNN 与 cuda 版本对应关系：https://developer.nvidia.com/rdp/cudnn-archive#a-collapse742-10

## 统计文件数目

递归统计目录文件数量

```bash
ls -lR| grep "^-"| wc -l
```

## 安装软件

```bash
sudo dpkg -i ***.deb
```

## bash 传参

### **无名参**

```bash
curl -s <http://XXX.com/xx/xx.sh> | bash -s arg1 arg2
```

或者

```bash
bash <(curl -s <http://XXX.com/xx/xx.sh>) arg1 arg2
```

### **具名参**

由于直接调用了 `bash`命令，因此在远程脚本需要传递具名参数时，为了区分是 `bash`命令的参数还是远程脚本的，可以使用 `--`作为区分，可以理解为分割线，`--`前面的比如 `-s`属于 `bash`，后面的 `-x abc -y xyz`属于远程脚本的参数

```bash
curl -L <http://XXX.com/xx/xx.sh> | bash -s -- -x abc -y xyz
```

## Debian 版本

- bullseye:Debian 11
- buster:Debian 10
- stretch:Debian 9
- jessie:Debian 8

## 后台运行

```bash
nohup python -u A.py >> /home/my.log 2>&1 &
```

## 显示系统进程

jobs 用于查看当前终端后台运行的任务，换了终端就看不到了。而ps命令用于查看瞬间进程的动态，可以看到别的终端运行的后台进程。

选项：

* a：显示一个终端的所有进程，除会话引线外；
* u：显示进程的归属用户及内存的使用情况；
* x：显示没有控制终端的进程；
* l：长格式显示更加详细的信息；
* e：显示所有进程；

```bash
ps -ef # System V Style
```

参数列表：

* UID //用户ID、但输出的是用户名
* PID //进程的ID
* PPID //父进程ID
* C //进程占用CPU的百分比
* STIME //进程启动到现在的时间
* TTY //该进程在那个终端上运行，若与终端无关，则显示? 若为pts/0等，则表示由网络连接主机进程
* CMD //命令的名称和参数

```bash
ps aux # Unix Style
```

* USER //用户名
* %CPU //进程占用的CPU百分比%
* MEM //占用内存的百分比
* VSZ //该进程使用的虚拟內存量（KB）
* RSS //该进程占用的固定內存量（KB）（驻留中页的数量）
* STAT //进程的状态
* START //该进程被触发启动时间
* TIME //该进程实际使用CPU运行的时间

其中STAT状态位常见的状态字符有：

* D //无法中断的休眠状态（通常 IO 的进程）
* R //正在运行可中在队列中可过行的
* S //处于休眠状态
* T //停止或被追踪
* W //进入内存交换 （从内核2.6开始无效）
* X //死掉的进程 （基本很少见）
* Z //僵尸进程
* < //优先级高的进程
* N //优先级较低的进程
* L //有些页被锁进内存
* s //进程的领导者（在它之下有子进程）
* l //多线程，克隆线程（使用 CLONE_THREAD, 类似 NPTL pthreads）
* * //位于后台的进程组

## 创建用户

```
useradd [option] username

[option]:

-d<登入目录> 指定用户登入时的目录。

-g<群组> 初始群组。

-G<群组> 非初始群组。

-m 自动创建用户的家目录。

-M 不要创建用户的家目录。

-N 不要创建以用户名称为名的群组。

-s 指定用户登入后所使用的shell。
```

示例

```
useradd -m -d /code/test -s /bin/bash myuser
```

## dos unix 转换

```bash
sed -i 's/\\r//' <file> # doc转unix
sed -i 's/$/\\r/' <file> # unix转doc
```

## 安装 ps

```bash
apt-get update
apt-get  install  procps
```

结束进程

```bash
kill -9 PID
```

按进程名结束进程

```bash
pkill -9 python
```

## tmux

tmux -u 显示中文

* `Ctrl+b %`：划分左右两个窗格。
* `Ctrl+b "`：划分上下两个窗格。
* `Ctrl+b <arrow key>`：光标切换到其他窗格。`<arrow key>`是指向要切换到的窗格的方向键，比如切换到下方窗格，就按方向键 `↓`。
* `Ctrl+b ;`：光标切换到上一个窗格。
* `Ctrl+b o`：光标切换到下一个窗格。
* `Ctrl+b {`：当前窗格与上一个窗格交换位置。
* `Ctrl+b }`：当前窗格与下一个窗格交换位置。
* `Ctrl+b Ctrl+o`：所有窗格向前移动一个位置，第一个窗格变成最后一个窗格。
* `Ctrl+b Alt+o`：所有窗格向后移动一个位置，最后一个窗格变成第一个窗格。
* `Ctrl+b x`：关闭当前窗格。
* `Ctrl+b !`：将当前窗格拆分为一个独立窗口。
* `Ctrl+b z`：当前窗格全屏显示，再使用一次会变回原来大小。
* `Ctrl+b Ctrl+<arrow key>`：按箭头方向调整窗格大小。
* `Ctrl+b q`：显示窗格编号。

## Debian 安装 zsh

```go
sudo apt-get install -y zsh
sh -c "$(curl -fsSL <https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh>)"
git clone <https://github.com/zsh-users/zsh-autosuggestions> ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone <https://github.com/zsh-users/zsh-syntax-highlighting.git> ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
sed -i 's#plugins=(git)#plugins=(git zsh-syntax-highlighting zsh-autosuggestions)#g' ~/.zshrc
sed -i 's#ZSH_THEME="robbyrussell"#ZSH_THEME="random"#g' ~/.zshrc
source ~/.zshrc
```

## nmap

netstat 参数解释：
-l  (listen) 仅列出 Listen (监听) 的服务
-t  (tcp) 仅显示tcp相关内容
-n (numeric) 直接显示ip地址以及端口，不解析为服务名或者主机名
-p (pid) 显示出socket所属的进程PID 以及进程名字
--inet 显示ipv4相关协议的监听

查看 IPV4 端口上的tcp的监听

```bash
netstat -lntp --inet
```

## 清空文件

```
echo > /etc/apt/sources.list
```

## 显卡

Linux 查看显卡信息：

```bash
lspci | grep -i vga
```

使用 nvidia GPU 可以

```bash
lspci | grep -i nvidia
```

查看指定显卡的详细信息用以下指令：

```bash
lspci -v -s 00:0f.0
```

Nvidia 自带一个命令行工具可以查看显存的使用情况：

```bash
nvidia-smi
```

表头释义

- Fan：显示风扇转速，数值在0到100%之间，是计算机的期望转速，如果计算机不是通过风扇冷却或者风扇坏了，显示出来就是N/A； 
- Temp：显卡内部的温度，单位是摄氏度；
- Perf：表征性能状态，从P0到P12，P0表示最大性能，P12表示状态最小性能；
- Pwr：能耗表示； 
- Bus-Id：涉及GPU总线的相关信息； 
- Disp.A：是Display Active的意思，表示GPU的显示是否初始化； 
- Memory Usage：显存的使用率； 
- Volatile GPU-Util：浮动的GPU利用率；
- Compute M：计算模式； 

下边的 Processes 显示每块GPU上每个进程所使用的显存情况。

如果要周期性的输出显卡的使用情况，可以用 watch 指令实现 5 秒钟刷新一次：

```bash
watch -n 5 nvidia-smi
```

## 清理 apt 缓存

查看 apt 缓存大小

```bash
du -sh /var/cache/apt/archives
```

清理 apt 缓存

```bash
sudo apt clean
```

## WSL 固定 ip

[终于找到给 wsl2 分配固定 ip 的方法 - V2EX](https://www.v2ex.com/t/744955)

## APT 源

一键修改 apt 源：

```bash
sed -i 's#archive.ubuntu.com#mirrors.163.com#g; s#security.ubuntu.com#mirrors.163.com#g; /# deb-src/d; /^#/d; /^$/d' /etc/apt/sources.list
```



```bash
bash -c 'echo "deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ hirsute main restricted universe multiverse" > /etc/apt/sources.list'
```

ubuntu20.04阿里云源：

```cpp
deb <http://mirrors.aliyun.com/ubuntu/> focal main restricted universe multiverse
deb-src <http://mirrors.aliyun.com/ubuntu/> focal main restricted universe multiverse

deb <http://mirrors.aliyun.com/ubuntu/> focal-security main restricted universe multiverse
deb-src <http://mirrors.aliyun.com/ubuntu/> focal-security main restricted universe multiverse

deb <http://mirrors.aliyun.com/ubuntu/> focal-updates main restricted universe multiverse
deb-src <http://mirrors.aliyun.com/ubuntu/> focal-updates main restricted universe multiverse

deb <http://mirrors.aliyun.com/ubuntu/> focal-proposed main restricted universe multiverse
deb-src <http://mirrors.aliyun.com/ubuntu/> focal-proposed main restricted universe multiverse

deb <http://mirrors.aliyun.com/ubuntu/> focal-backports main restricted universe multiverse
deb-src <http://mirrors.aliyun.com/ubuntu/> focal-backports main restricted universe multiverse
```

[ubuntu镜像-ubuntu下载地址-ubuntu安装教程-阿里巴巴开源镜像站](https://developer.aliyun.com/mirror/ubuntu?spm=a2c6h.13651102.0.0.3e221b11jBxQc8)

```cpp
mirrors.163.com
mirrors.tuna.tsinghua.edu.cn
mirrors.aliyun.com
mirror.nju.edu.cn
mirrors.ustc.edu.cn
```

## 修改代理

```bash
cat >> ~/.bashrc <<EOF
export http_proxy="http://192.168.177.1:7890"
export https_proxy="https://192.168.177.1:7890"
EOF
source ~/.bashrc

```

记得 clash allow lan

```bash
cat >> ~/.bashrc <<EOF
host_ip=$(ip route | grep default | awk '{print $3}')
export ALL_PROXY="http://$host_ip:7890"
EOF
source ~/.bashrc

```

## Linux执行结果不输出到终端

[Linux执行结果不输出到终端_sunny05296的博客-CSDN博客_shell 不输出到屏幕](https://blog.csdn.net/sunny05296/article/details/78846709)

## 修改host文件

```makefile
echo '140.82.112.4 github.com' >> /etc/hosts
echo '104.18.10.147 api.notion.com' >> /etc/hosts
echo '104.18.11.147 api.notion.com' >> /etc/hosts
```

[IPAddress.com](https://www.ipaddress.com/)

## Linux系统中挂载和使用光盘的基本步骤

[VMware Knowledge Base](https://kb.vmware.com/s/article/1018414?lang=zh_CN)

[Linux系统中挂载和使用光盘的基本步骤_lamp_yang_3533的博客-CSDN博客_linux挂载光盘](https://blog.csdn.net/lamp_yang_3533/article/details/53284290)

## 修改 DNS

不应该直接编辑 /etc/resolv.conf文件，因为它可能会被系统自动覆盖或者重置。您应该使用相应的工具来修改网络设置或者DHCP租约，或者安装resolvconf包来管理DNS解析器的配置。/etc/resolv.conf文件是用来配置DNS解析器的，它告诉系统如何将域名转换为IP地址。在ubuntu系统中，这个文件可能会被多个程序或者服务覆盖或者重置，比如：

- systemd-resolved服务，它会根据系统的网络设置和DHCP租约来动态地生成/etc/resolv.conf文件或者创建一个符号链接到/run/systemd/resolve/stub-resolv.conf或者/run/systemd/resolve/resolv.conf文件  。
- resolvconf程序，它会根据/etc/resolvconf/resolv.conf.d/目录下的文件来生成/run/resolvconf/resolv.conf文件，并创建一个符号链接到/etc/resolv.conf文件 。
- dhclient程序，它会根据DHCP租约中的DNS信息来修改或者覆盖/etc/resolv.conf文件 。
- network-manager服务，它会根据网络接口的配置来修改或者覆盖/etc/resolv.conf文件 。

如果您想正确地设置DNS服务器，您不应该直接编辑 /etc/resolv.conf文件，因为它可能会被系统自动覆盖或者重置。您应该使用相应的工具来修改网络设置或者DHCP租约，或者安装resolvconf包来管理DNS解析器的配置。您也可以使用systemd-resolved服务来设置DNS服务器，方法是在`/etc/systemd/resolved.conf`文件中添加一行DNS=8.8.8.8（或者您想要的DNS服务器地址），然后重启`systemd-resolved`服务 。

```bash
sudo vim /etc/systemd/resolved.conf
sudo systemctl restart systemd-resolved
```

resolv.conf

```bash
sudo cat >> /etc/resolv.conf <<EOF
nameserver 8.8.8.8
nameserver 114.114.114.114
EOF
```

```bash
sudo vi /run/systemd/resolve/resolv.conf 
sudo systemctl restart systemd-resolved.service
```

## 设置非root账号不用sudo直接执行docker命令

```bash
sudo groupadd docker
sudo gpasswd -a yym docker
sudo systemctl restart docker
sudo chmod a+rw /var/run/docker.sock

```

[设置非root账号不用sudo直接执行docker命令_mb607022e25a607的技术博客_51CTO博客](https://blog.51cto.com/u_15162069/2743991)

## 重复执行命令

[良许Linux](https://www.cnblogs.com/yychuyu/p/12967366.html)

## sed

替换标记

```
g # 表示行内全面替换。
p # 表示打印行。
w # 表示把行写入一个文件。
x # 表示互换模板块中的文本和缓冲区中的文本。
y # 表示把一个字符翻译为另外的字符（但是不用于正则表达式）
\\1 # 子串匹配标记
& # 已匹配字符串标记
```

[sed](https://wangchujiang.com/linux-command/c/sed.html)

[linux sed命令详解 - ggjucheng - 博客园](https://www.cnblogs.com/ggjucheng/archive/2013/01/13/2856901.html)

## tr

```bash
tr -d '"'
```

[Linux tr命令](https://www.runoob.com/linux/linux-comm-tr.html)

## Linux时间设置

### Linux系统时间的设置

查看时间

```docker
date
```

2008年 12月 12日星期五 14:44:12 CST

修改时间

```docker
date -set  "2013-12-24 00:01"
```

2009年 01月 01日星期四 00:01:00 CST

date 有几种时间格式可接受，这样也可以设置时间：

```docker
date 012501012009.30  //月日时分年.秒 2009年01月25日星期日 01:01:30 CST
```

### Linux硬件时间的设置

硬件时间的设置可以用 `hwclock`或者 `clock`命令。

> clock命令同时支持x86硬件体系和支持Alpha硬件体系

查看硬件时间可以用 `hwclock`，`hwclock --show`或者 `hwclock -r`

设置硬件时间

```docker
hwclock --set --date="1/25/09 00:00"
```

根据系统时间设置硬件时间

```docker
hwclock  -w   
```

### 系统时间和硬件时间的同步

同步系统时间和硬件时间，可以使用 `hwclock`命令。

以系统时间为基准，修改硬件时间

```docker
hwclock --systohc
hwclock -w

```

> sys（系统时间）to（写到）hc（Hard Clock）

以硬件时间为基准，修改系统时间

```docker
hwclock --hctosys
hwclock -s

```

References

[linux时间同步，ntpd、ntpdate](https://www.cnblogs.com/liushui-sky/p/9203657.html)

## 管道符号

```bash
多命令执行符              格式                        作用
     ;               命令1;命令2             多个命令顺序执行，命令之间无任何逻辑关系
    &&               命令1&&命令2            逻辑与：当命令1正确执行后，命令2才会正确执行，否则命令2不会执行
    ||               命令1||命令2            逻辑或：当命令1不正确执行后，命令2才会正确执行，否则命令2不会执行
    |                命令1| 命令2            命令1的正确输出作为命令2的操作对象

;	 //分号
|	 //只执行后面那条命令
|| //只执行前面那条命令
&	 //两条命令都会执行
&& //两条命令都会执行
```

## 通配符

| ?    | 匹配一个任意字符                              |
| ---- | --------------------------------------------- |
| *    | 匹配0个或多个任意字符，也就是可以匹配任何内容 |
| []   | 匹配括号中任意一个字符                        |
| [-]  | 匹配括号中任意一个字符，“-”代表范围           |
| [^]  | 逻辑非，表示匹配不是括号内的一个字符          |

## Alpine 别名

```bash
vim /etc/profile
alias ll='ls -l'
```

[Alpine Linux设置彩色提示符及Alias的方法_boliang319的专栏-CSDN博客](https://blog.csdn.net/boliang319/article/details/107314791)

[Alpine](https://yeasy.gitbook.io/docker_practice/os/alpine)

## Linux 别名

```makefile
vim ~/.bashrc
alias home=”ssh -i ~/.ssh/mykep.pem linuxic@192.168.1.199”
alias ll='ls -l'
source ~/.bashrc
alias
```

[如何在Linux中创建和使用别名Alias命令_Linux教程_Linux公社-Linux系统门户网站](https://www.linuxidc.com/Linux/2019-08/160442.htm)

## 卸载软件

```makefile
sudo apt-get remove --purge 软件名称
```

[ubuntu 命令行卸载并清理软件（卸载的很干净）_jiayoudangdang的博客-CSDN博客](https://blog.csdn.net/jiayoudangdang/article/details/79943065)

## makefile

* `$@` ：当前目标，目标文件
* `$<` ：第一个前置条件，第一个文件
* `$?` ：比目标更新的所有前置条件
* `$^` ：所有前置条件

```makefile
run: w-s
	./w-s < w-s.l

w-s: lex.yy.c
	gcc -o $@ $<

lex.yy.c: w-s.l
	flex $<
```

[词法分析器flex](https://zhuanlan.zhihu.com/p/52290783)

[Makefile教程（绝对经典，所有问题看这一篇足够了）_GUYUEZHICHENG的博客-CSDN博客_makefile](https://blog.csdn.net/weixin_38391755/article/details/80380786)

## 大于号> 小于号<

1、> 覆盖输出到文本

2、>>追加到文本

3、< 将后面文件作为前面命令的输入

4、<< 带命令作用全文匹配某个字符串后结束

5、<<<部分匹配某个字符串

[linux 命令中的大于号、小于号的作用_a807719447的专栏-CSDN博客_linux 大于号命令](https://blog.csdn.net/a807719447/article/details/101548281)

## 查看Linux配置

查看每个物理CPU中core的个数(即核数)：

```
cat /proc/cpuinfo| grep "cpu cores"| uniq
```

查看物理CPU个数：

```
cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l
```

查看逻辑CPU的个数：

```
cat /proc/cpuinfo| grep "processor"| wc -l
```

References

[Linux查看物理CPU个数、核数、逻辑CPU个数](https://www.cnblogs.com/emanlee/p/3587571.html)

## linux目录

* `/usr`：系统级的目录，可以理解为 `C:/Windows/`
* `/usr/lib`理解为 `C:/Windows/System32`
* `/usr/local`：用户级的程序目录，可以理解为 `C:/Progrem Files/`。用户自己编译的软件默认会安装到这个目录下
* `/opt`：用户级的程序目录，可以理解为 `D:/Software`，opt有可选的意思，这里可以用于放置第三方大型软件（或游戏），当你不需要时，直接 `rm -rf`掉即可。在硬盘容量不够时，也可将/opt单独挂载到其他磁盘上使用。

源码放哪里？

* `/usr/src`：系统级的源码目录
* `/usr/local/src`：用户级的源码目录

[Linux中个文件夹的介绍及其作用_YQlakers的博客-CSDN博客](https://blog.csdn.net/YQlakers/article/details/69950868)

## 伪终端

什么是伪终端（`pseudo-terminal`）？

* 伪终端的介绍请参考：
  [Linux 的伪终端的基本原理 及其在远程登录（SSH，telnet等）中的应用](https://www.cnblogs.com/zzdyyy/p/7538077.html)

伪终端在 `ssh` 客户端还是服务端创建？

* 伪终端在 `ssh` 服务端创建

`ssh` 是否分配伪终端的区别是什么？

* 不分配伪终端，会导致一些需要 `tty` 的命令无法正常使用。比如 `vim`
  [Linux tty命令](https://www.runoob.com/linux/linux-comm-tty.html)

`ssh` 命令存在两种基本模式，一是登录到远程机器，二是在远程机器上执行代码。

References

[ssh 命令详解](https://www.jianshu.com/p/a7d9c1ac7757)

## scp

本地文件夹复制到远程

```bash
scp -P 8822 -r /Users/yanyuming/Downloads/split_reid_data/msmt17v2 yuming@10.214.130.168:/home/yuming
```

## tar

解压缩命令

* c: 建立压缩档案
* x：解压
* t：查看内容
* r：向压缩归档文件末尾追加文件
* u：更新原压缩包中的文件

这五个是独立的命令，压缩解压都要用到其中一个，可以和别的命令连用但只能用其中一个。下面的参数是根据需要在压缩或解压档案时可选的。

* z：有gzip属性的
* j：有bz2属性的
* Z：有compress属性的
* v：显示所有过程
* O：将文件解开到标准输出

下面的参数-f是必须的

* f: 使用档案名字，切记，这个参数是最后一个参数，后面只能接档案名。

### 一键解压命令

```bash
ex () {
	if [ -f $1 ] ; then
		case $1 in
			*.tar.bz2)   tar xjf $1   ;;
			*.tar.gz)    tar xzf $1   ;;
			*.tar.xz)    tar xf $1   ;;
			*.bz2)       bunzip2 $1   ;;
			*.rar)       rar x $1     ;;
			*.gz)        gunzip $1    ;;
			*.tar)       tar xf $1    ;;
			*.tbz2)      tar xjf $1   ;;
			*.tgz)       tar xzf $1   ;;
			*.zip)       unzip $1     ;;
			*.Z)         uncompress $1  ;;
			*.7z)        7z x $1    ;;
			*)           echo "'$1' cannot be extracted via extract()" ;;
		esac
	else
		echo "'$1' is not a valid file"
	fi
}
```

## gzip

## mkdir

* make dirctory
* 创建文件夹
* mkdir + <文件夹名>
* mkdir .+<文件夹名>创建隐藏文件夹
* mkdir -p a/b/c/d

```
-m, --mode=模式       设置权限模式(类似chmod)，而不是rwxrwxrwx 减umask
-p, --parents         需要时创建目标目录的上层目录，但即使这些目录已存在也不当作错误处理
-v, --verbose         每次创建新目录都显示信息
-Z, --context=CTX     将每个创建的目录的SELinux 安全环境设置为CTX
    --help            显示此帮助信息并退出
    --version         显示版本信息并退出
```

## ls

* 显示当前目录下所有文件
* ls /bin
  * 显示/bin目录下所有文件
* ls -al /bin
  * 显示文件夹下所有详细内容
  * 第五列的内容为文件的字节数
  * 显示包括隐藏文件
  * 相当于ls -a -l /bin
* ls -alh /bin
  * 文件大小用kb，mb显示
* ls --help
  * 显示ls的具体参数用法
  * 用法
  * 点文件为隐藏文件
* ls / 列出根目录下所有文件夹
* ls -al > text.txt
  * 将ls-al执行的内容保存覆盖到text文件中
  * 如果没有text.txt,系统自动创建
  * 如果存在覆盖原本的内容
  * \>>追加操作符，将文本内容追加到右边的文件中，而不是覆盖

## cd

* change directory
* cd + <文件名>
  * 进入当前目录下的文件直接cd + <文件名>
  * 进入根目录下的文件cd + /<文件名>
* 进入指定文件夹
* cd . 换成当前目录
  * .为当前文件夹
  * ..为上一级文件夹
* cd .. 返回上一级目录
* cd ~
  * 返回用户根目录，主文件夹，主目录，home目录

## pwd

* 显示当前在什么目录下
* 显示从根目录到现在文件夹所有路径
* .+<文件名>
  * 隐藏文件
  * mkdir .+<文件名>创建隐藏文件

## touch

* touch + <文件名>
* touch .+<文件名>创建隐藏文件

## rm

* 删除文件
* rm +<文件名>
* rm -f <文件名>强制删除，就算文件不存在也不输出任何提示
* rm -r <文件夹名> 删除文件夹
  * 把文件夹下的内容全部删除，递归删除
* rm -rf / 删除根目录

删除可执行文件：

```bash
rm -f $(find . -type f -perm /u=x,g=x,o=x)
```

## cp

* 复制文件
* cp +<被复制文件名>+<新文件名>
* 没有参数只能复制文件
* cp -r <文件名> <文件夹名>
  * 将文件复制到指定文件夹下
* cp -r /home/install-package/* /home/cp/install_package/
  * 将/home/install-package/文件夹内的所有文件都复制到 /home/cp/install_package/文件夹下

## mv

* 移动文件
  * mv <文件名/文件夹名> <文件夹名>
* 重命名文件
  * mv <原文件名/原文件夹名> <修改后的文件夹名>
* mv <文件名/文件夹名> ..
  * 将文件移动到上级文件夹

## cat

* 输出文件内容
* cat /etc/passwd 显示用户所有密码用户名

cat是一次性显示整个文件的内容，还可以将多个文件连接起来显示，它常与重定向符号配合使用，适用于文件内容少的情况；

```bash
1、命令格式
cat [选项] [文件]
2、命令功能
将[文件]或标准输入组合输出到标准输出。

cat主要有三大功能：
(1) 一次显示整个文件:cat filename
(2) 从键盘创建一个文件:cat > filename 只能创建新文件,不能编辑已有文件.
(3) 将几个文件合并为一个文件:cat file1 file2 > file
3、常用参数列表
  -A, --show-all            等于-vET
  -b, --number-nonblank     对非空输出行编号
  -e                        等于-vE
  -E, --show-ends           在每行结束处显示"$"
  -n, --number              对输出的所有行编号
  -s, --squeeze-blank       不输出多行空行
  -t                        与-vT 等价
  -T, --show-tabs           将跳格字符显示为^I
  -u                        (被忽略)
  -v, --show-nonprinting    使用^ 和M- 引用，除了LFD和 TAB 之外
      --help                显示此帮助信息并退出
      --version             显示版本信息并退出
```

写入多行内容，注意转义：

```bash
cat > way4.sh <<EOF
#!/bin/bash
export PATH=\\$PATH:~/bin/
EOF
```

[使用shell添加多行到文件的几个办法](https://www.jibing57.com/2017/12/12/how-to-write-multiline-to-file-by-shell/)

## \>

* 将左边执行的内容保存覆盖到右边的文件中
* 如果没有右边的文件,系统自动创建
* 如果存在覆盖原本的内容

## \>>

* 追加操作符，将文本内容追加到右边的文件中，而不是覆盖

## |

* 管道符号
* 把左边的内容输入到右边
* 把左边的输出当输入交给右边的命令执行
* 可以重用
  * ls -al /bin | head -n 20 | tail
    * 将head输出的前二十行取其后十行输出

## head

* 只显示前面的几行内容，如果内容太多
* 默认输出前十行
* head -n x x为指定的前面的行数
* ls -al | head -n 3
  * 显示左边内容的前三行

## tail

* 输出最后几行，默认十行
* ls -al /bin | head -n 20 | tail
  * 将head输出的前二十行取其后十行输出

## more

提供分页显示的功能

* cat命令是整个文件的内容从上到下显示在屏幕上。
* more会以一页一页的显示方便使用者逐页阅读

空白键（space） 下一页显示，b 键 回（back）一页显示，还有搜寻字串的功能，more命令从前向后读取文件，因此在启动时就加载整个文件

```bash
1、命令格式
 more [-dlfpcsu] [-num] [+/pattern] [+linenum] [file ...]

2、命令功能
more命令和cat的功能一样都是查看文件里的内容，但有所不同的是more可以按页来查看文件的内容，还支持直接跳转行等功能。

3、常用参数列表
     -num  一次显示的行数
     -d    在每屏的底部显示友好的提示信息
     -l    忽略 Ctrl+l （换页符）。如果没有给出这个选项，则more命令在显示了一个包含有 Ctrl+l 字符的行后将暂停显示，并等待接收命令。
     -f     计算行数时，以实际上的行数，而非自动换行过后的行数（有些单行字数太长的会被扩展为两行或两行以上）
     -p     显示下一屏之前先清屏。
     -c    从顶部清屏然后显示。
     -s    文件中连续的空白行压缩成一个空白行显示。
     -u    不显示下划线
     +/    先搜索字符串，然后从字符串之后显示
     +num  从第num行开始显示

4、常用操作命令
Enter    向下n行，需要定义。默认为1行
Ctrl+F   向下滚动一屏
空格键   向下滚动一屏
Ctrl+B   返回上一屏
=        输出当前行的行号
：f      输出文件名和当前行的行号
v        调用vi编辑器
!命令    调用Shell，并执行命令 
q        退出more
```

## less

* 如果内容太多，允许使用上下键查看
* 按q键即可退出查看
* ls -al /bin | less

提供翻页，跳转，查找等命令

less 工具也是对文件或其它输出进行分页显示的工具，应该说是linux正统查看文件内容的工具，功能极其强大。less 的用法比起 more 更加的有弹性。在 more 的时候，我们并没有办法向前面翻， 只能往后面看，但若使用了 less 时，就可以使用 [pageup] [pagedown] 等按键的功能来往前往后翻看文件，更容易用来查看一个文件的内容！除此之外，在 less 里头可以拥有更多的搜索功能，不止可以向下搜，也可以向上搜。

* more和less都支持：用空格显示下一页，按键b显示上一页。

```bash
1．命令格式：
less [参数]  文件 
2．命令功能：
less 与 more 类似，但使用 less 可以随意浏览文件，而 more 仅能向前移动，却不能向后移动，而且 less 在查看之前不会加载整个文件。
3．命令参数：
-b <缓冲区大小> 设置缓冲区的大小
-e  当文件显示结束后，自动离开
-f  强迫打开特殊文件，例如外围设备代号、目录和二进制文件
-g  只标志最后搜索的关键词
-i  忽略搜索时的大小写
-m  显示类似more命令的百分比
-N  显示每行的行号
-o <文件名> 将less 输出的内容在指定文件中保存起来
-Q  不使用警告音
-s  显示连续空行为一行
-S  行过长时间将超出部分舍弃
-x <数字> 将“tab”键显示为规定的数字空格
/字符串：向下搜索“字符串”的功能
?字符串：向上搜索“字符串”的功能
n：重复前一个搜索（与 / 或 ? 有关）
N：反向重复前一个搜索（与 / 或 ? 有关）
b  向后翻一页
d  向后翻半页
h  显示帮助界面
Q  退出less 命令
u  向前滚动半页
y  向前滚动一行
空格键 滚动一页
回车键 滚动一行
```

## grep

* 在文件里找字符串
* grep sh text.txt
  * 在text.txt中查找sh，并输出包含sh的所有行

## find

* 在没有任何参数的情况下，输出当前目录下所有的文件与文件夹
* find . -name he
  * 在当前目录下查找含有he字符的文件名并输出
* find -name '*()\*'
  * 部分查找，查找含有()字符串的文件内容
  * '*()' 指确定字符串出现在文件名的最后
  * '()*' 指确定字符串出现在文件名的最前面
* find . -name dirname -type d
  * 在当前目录下寻找文件夹


References

[linux查找文件命令find_发芽的石头-CSDN博客](https://blog.csdn.net/ydfok/article/details/1486451)

## zip

* zip -r <文件名.zip> *
  * 当前目录下所有的文件与文件夹（除了隐藏文件）打包压缩进 <文件名.zip>
  * 加了-r 之后，压缩会包括文件夹及其子孙文件
* zip -r <文件名.zip> () () ()……
  * 后面可以跟一堆文件

## unzip

* unzip <被解压文件名.zip>

## whoami

* 告诉自己是什么用户进行操作

## nano

* 文件管理器,终端图形化界面
* nano \filename
* CTRL+o 保存
* CTRL+x退出
* CTRL+w查找字符串
  * CTRL+w+space 下一个

## ps

* 显示当前终端哪些程序进程在运行
* ps -aux 显示系统运行的程序进程

## top

* 显示系统基本情况
* cpu
* q键 退出

## man

* man + 命令
* 查看命令用法
* 查看参数用法

## wget

* wget + url 下载网页源代码
* man wget

## ping

* ping + url

## vim

## du

* du的英文为:disk usage,含义是磁盘空间使用情况，功能是逐级进入指定目录的每一个子目录并显示该目录占用文件系统数据块的情况，如果没有指定目录，则对当前的目录进行统计。
* du的命令各个选项含义如下：
  * a：显示全部目录和其次目录下的每个档案所占的磁盘空间
  * s：只显示各档案大小的总合
  * b：大小用bytes来表示
  * x：跳过在不同文件系统上的目录不予统计
  * a：递归地显示指定目录中各文件及子孙目录中各文件占用的数据块数

## df

disk free，命令用于显示目前在 Linux 系统上的文件系统磁盘使用情况统计。

```bash
df -h
```

## id

## openssl

format:

```bash
openssl rand [-out file] [-rand file(s)] \\[-base64] \\[-hex] num
```

function: generate random number

parameter:

* out ：指定随机数输出文件，否则输出到标准输出。
* rand file ：指定随机数种子文件。种子文件中的字符越随机，openssl rand生成随机数的速度越快，随机度越高。
* base64 ：指定生成的随机数的编码格式为base64。
* hex ：指定生成的随机数的编码格式为hex。
* num ：指定随机数的长度。

例子：

```bash
openssl rand -base64 30;
openssl rand -hex 30;
openssl rand 30
```

## exit 退出程序

## chmod

* rwx
  * r→4
  * w→2
  * x→1
* 修改权限
  * chmod 751 \filename
    * 7表示全部权限，owner
    * 5表示rx，group
    * 1表示x，third party

for example:

```bash
sudo chmod 646 file.txt
```

将自己（第三方）权限改为可读可写，我自己是第三的6

[linux命令 ll信息详解_HELLOW，文浩-CSDN博客_linux ll](https://blog.csdn.net/dshf_1/article/details/99973236)

## sudo

* 最高管理员权限root

su su - sudo区别：

[su su- sudo区别概述](https://www.cnblogs.com/pipci/p/8857281.html)

### sudo免密码

方法一：

为了避免每次使用 sudo 命令时都输入密码，我们可以将密码关闭。操作方法：

1. 终端输入命令，打开 `visudo`：

   ```bash
   sudo visudo
   ```

2. 找到 `%sudo ALL=(ALL:ALL) ALL` 这一行修改为：

   ```bash
   %sudo ALL=(ALL:ALL) NOPASSWD:ALL
   ```

`Ctrl+S Ctrl+X`保存退出。

方法二：

Modify permissions:

```bash
sudo chmod 744 /etc/sudoers
```

now,we need to open /etc/sudors file, execute the command below:

```bash
sudo vim /etc/sudoers
```

在 `Allow members of group sudo to execute any command`下面添加：

```
yym ALL=(ALL:ALL) NOPASSWD: ALL
```

修改完成后：

```bash
sudo chmod 440 /etc/sudoers
```

References

[ubuntu 设置sudo 免密码](https://www.cnblogs.com/linux-37ge/p/11100312.html)

su root 编辑sudoers文件：vi /etc/sudoers

或者 sudo vi /etc/sudoers

找到这行 root ALL=(ALL) ALL,在他下面添加xxx ALL=(ALL) ALL (注：这里的xxx是你的用户名)

你可以根据实际需要在sudoers文件中按照下面四行格式中任意一条进行添加：

```c
youuser            ALL=(ALL)                ALL
%youuser           ALL=(ALL)                ALL
youuser            ALL=(ALL)                NOPASSWD: ALL
%youuser           ALL=(ALL)                NOPASSWD: ALL
```

第一行：允许用户youuser执行sudo命令(需要输入密码)。
第二行：允许用户组youuser里面的用户执行sudo命令(需要输入密码)。
第三行：允许用户youuser执行sudo命令,并且在执行的时候不输入密码。
第四行：允许用户组youuser里面的用户执行sudo命令,并且在执行的时候不输入密码。

强制保存退出，:w!

## ubuntu设置

[写给工程师的 Ubuntu 20.04 最佳配置指南](https://zhuanlan.zhihu.com/p/139305626)

### 安装anaconda

[Index of /anaconda/archive/ | 清华大学开源软件镜像站 | Tsinghua Open Source Mirror](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)

[Ubuntu18.04 安装 Anaconda3_梦Dancing的博客-CSDN博客_ubuntu安装anaconda](https://blog.csdn.net/qq_15192373/article/details/81091098)

```bash
bash Anaconda3-5.2.0-Linux-x86_64.sh
echo 'export PATH="~/anaconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Ubuntu安装deb

```bash
sudo dpkg -i sogoupinyin_2.4.0.3469_amd64.deb
```

### 修改软件源

Software & Updates

之后

```bash
# 更新本地包数据库
sudo apt update

# 更新所有已安装的包（也可以使用 full-upgrade）
sudo apt upgrade

# 自动移除不需要的包
sudo apt autoremove
```

## 解压.tar.gz文件

```
tar -zxvf filename.tar.gz
```

## 打开图形界面文件夹

```bash
sudo nautilus .
```

## Linux环境变量

* `export`命令显示当前系统定义的所有环境变量
* `echo $PATH`命令输出当前的 `PATH`环境变量的值

classification:

* 用户级别环境变量定义文件：`~/.bashrc`、`~/.profile`，或者 `~/.bash_profile`
* 系统级别环境变量定义文件：`/etc/bashrc`、`/etc/profile`、`/etc/environment`，或者：`/etc/bash_profile`

另外在用户环境变量中，系统会首先读取 `~/.bash_profile`（或者 `~/.profile`）文件，如果没有该文件则读取 `~/.bash_login`，根据这些文件中内容再去读取 `~/.bashrc`。

Linux加载环境变量的顺序如下：

1. `/etc/environment`
2. `/etc/profile`
3. `/etc/bash.bashrc`
4. `/etc/profile.d/test.sh`
5. `~/.profile`
6. `~/.bashrc`

```bash
vim ~/.bashrc
source ~/.bashrc
```

References

[Linux环境变量配置全攻略](https://www.cnblogs.com/youyoui/p/10680329.html)

## Linux中source命令的用法

source命令也称为点命令，也就是一个点符号 `.`。source命令通常用于重新执行刚修改的初始化文件，使之立即生效，而不必注销并重新登录。

用法：

* source filename 或 . filename 它的作用就是把一个文件的内容当成shell来执行。

`source filename`与 `sh filename`及 `./filename`执行脚本的区别在那里呢？

1. 当shell脚本具有可执行权限时，用sh filename与./filename执行脚本是没有区别得。./filename是因为当前目录没有在PATH中，所有"."是用来表示当前目录的。
2. `sh filename`重新建立一个子shell，在子shell中执行脚本里面的语句，该子shell继承父shell的环境变量，但子shell新建的、改变的变量不会被带回父shell，除非使用export。
3. `source filename`：这个命令其实只是简单地读取脚本里面的语句依次在当前shell里面执行，没有建立新的子shell。那么脚本里面所有新建、改变变量的语句都会保存在当前shell里面。

References

[source命令](https://www.jianshu.com/p/63ded646d4cd)
