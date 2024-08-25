# Docker 笔记

## 优化

查看哪一层占用空间最大，这个命令可以显示镜像的构建历史，包括每一层的大小。

```
docker history <image_name>
```

进入容器，覆盖启动脚本

```
docker run -it --entrypoint /bin/sh your-image-name
```

查看文件系统大小并排序

```
du -sh /usr/local/lib/python3.10/* | sort -hr
```

## 实例

### 评课社区

```bash
docker build --network=host -t course:1.0 .
```

### 最小系统

```docker
cd /mnt/f/code/minisystem
```

Dockerfile

Neovim版 不要用教育网，会有过时的apt缓存，导致Hash Sum mismatch，也不要在windows下构建

```docker
FROM ubuntu:20.04
WORKDIR /root
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone \\
    && sed -i 's#archive.ubuntu.com#mirrors.163.com#g; s#security.ubuntu.com#mirrors.163.com#g; /# deb-src/d; /^#/d; /^$/d' /etc/apt/sources.list \\
    && apt-get update \\
    && touch ~/.tmux.conf && echo "set-option -g mouse on" > ~/.tmux.conf \\
    && touch ~/.netrc && chmod 600 ~/.netrc \\
    && echo -e "machine github.com\\n        login not-used\\n        password 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" > ~/.netrc && sed -i 's#-e ##g' ~/.netrc \\
    && apt -y install software-properties-common git build-essential curl wget unzip tmux \\
    && git clone <https://github.com/yym68686/Neovim-config.git> /root/.config/nvim \\
    && git clone --depth 1 <https://github.com/wbthomason/packer.nvim> ~/.local/share/nvim/site/pack/packer/start/packer.nvim \\
    && add-apt-repository ppa:neovim-ppa/stable \\
    && apt install -y neovim \\
    && echo export LESSCHARSET=utf-8 >> ~/.bashrc \\
    && echo alias python=python3 >> ~/.bashrc \\
    && echo alias vim=nvim >> ~/.bashrc \\
    && git config --global user.email "yym68686@outlook.com" \\
    && git config --global user.name "yym68686" \\
    && /bin/bash -c "source ~/.bashrc"
```

vim版

```docker
FROM ubuntu:20.04
WORKDIR /root
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone \\
    && sed -i 's#archive.ubuntu.com#mirrors.163.com#g; s#security.ubuntu.com#mirrors.163.com#g; /# deb-src/d; /^#/d; /^$/d' /etc/apt/sources.list \\
    && apt-get update \\
    && touch ~/.tmux.conf && echo "set-option -g mouse on" > ~/.tmux.conf \\
    && touch ~/.netrc && chmod 600 ~/.netrc \\
    && echo -e 'machine github.com\\n        login not-used\\n        password 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' > ~/.netrc && sed -i 's#-e ##g' ~/.netrc \\
    && apt -y install vim git build-essential curl jq tmux \\
    && echo export LESSCHARSET=utf-8 >> ~/.bashrc \\
    && git config --global user.email "yym68686@outlook.com" && git config --global user.name "yym68686" \\
    && curl '<https://api.notion.com/v1/blocks/8b4f12d4fd4c42f0b4dce39ed3fbeb79>' -H 'Authorization: Bearer secret_8DQN9wRRMpDUgwY3St79g5ltrxL3thq6qdPkKyywqZN' -H 'Notion-Version: 2022-02-22' | jq -r '.code.rich_text[0].plain_text' > ~/.vimrc \\
    && /bin/bash -c "source ~/.bashrc" \\
```

从容器退出后重新构建镜像：

```bash
docker rm -f $(docker ps -aq)
docker rmi -f minisystem
cd /mnt/e/code/minisystem
curl '<https://api.notion.com/v1/blocks/6adde3a7cfb64d6faac35a9ba935f855>' \\
  -H 'Authorization: Bearer secret_8DQN9wRRMpDUgwY3St79g5ltrxL3thq6qdPkKyywqZN' \\
  -H 'Notion-Version: 2022-02-22' | jq -r '.code.rich_text[0].plain_text' > Dockerfile
docker build --no-cache --network=host -f mini-Dockerfile -t minisystem .
docker exec -it $(docker run --network=host -dit minisystem) bash
```

进入后安装插件：

```bash
nvim +PackerSync
```

push脚本：

```bash
cd ~/.config/nvim
git add .
git commit -m "modified sth."
git push -u origin master
cd -
```

### CSAPP-Lab

32 位

下载镜像 ubuntu 18.04 32位

```bash
docker pull ubuntu:18.04@sha256:23791acc4e8a895989bc05e101e2520775d5ac812e83d1c0bf3ccf653bb0f110
```

构建：

```bash
docker build --no-cache --network=host -f CSAPP-Lab-Dockerfile -t csapplab --platform=linux/386 .
```

CSAPP-Lab-Dockerfile

```docker
FROM ubuntu:18.04.386
WORKDIR ~
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone \\
    && sed -i 's#archive.ubuntu.com#mirrors.163.com#g; s#security.ubuntu.com#mirrors.163.com#g; /# deb-src/d; /^#/d; /^$/d' /etc/apt/sources.list \\
    && apt-get update \\
    && touch ~/.netrc \\
    && chmod 600 ~/.netrc \\
    && echo -e 'machine github.com\\n        login not-used\\n        password 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' > ~/.netrc \\
    && apt install -y git vim build-essential curl jq\\
    && echo export LESSCHARSET=utf-8 >> ~/.bashrc \\
    && git config --global user.email "yym68686@outlook.com" \\
    && git config --global user.name "yym68686" \\
    && curl '<https://api.notion.com/v1/blocks/8b4f12d4fd4c42f0b4dce39ed3fbeb79>' \\
         -H 'Authorization: Bearer secret_8DQN9wRRMpDUgwY3St79g5ltrxL3thq6qdPkKyywqZN' \\
         -H 'Notion-Version: 2022-02-22' | jq -r '.code.rich_text[0].plain_text' > ~/.vimrc \\
    && /bin/bash -c "source ~/.bashrc" \\
    && git clone <https://github.com/yym68686/CSAPP-Lab.git> \\
    && apt install -y man build-essential gdb git
```

2

```dockerfile
FROM ubuntu:18.04.386
WORKDIR /home
RUN apt-get update && apt install -y vim build-essential gdb
```

运行

```bash
docker exec -it $(docker run --network=host -v ~/Desktop/bomb361:/home -dit csapplab) bash
```

64 位

```
docker pull ubuntu:18.04
```

构建：

```bash
docker build --no-cache --network=host -f CSAPP-Lab-Dockerfile -t csapplab --platform linux/x86_64 .
```

CSAPP-Lab-Dockerfile

```dockerfile
FROM ubuntu:18.04
WORKDIR /home
RUN apt-get update && apt install -y vim build-essential gdb
```

运行

```bash
docker exec -it $(docker run --network=host -v ~/Desktop/bomb361:/home -dit csapplab) bash
```

### PA

计组实验

```bash
cd /mnt/f/code/PA
```

linux 32位 拉取Ubuntu32位：

```bash
docker pull ubuntu:18.04@sha256:23791acc4e8a895989bc05e101e2520775d5ac812e83d1c0bf3ccf653bb0f110
```

运行指令：

```bash
docker exec -it $(docker run -dit ubuntu:18.04.386) bash
```

查看系统：

```bash
dpkg --print-architecture
```

Dockerfile

nvim

```bash
FROM ubuntu:18.04.386
WORKDIR ~
RUN sed -i 's#archive.ubuntu.com#mirrors.163.com#g; s#security.ubuntu.com#mirrors.163.com#g; s/# deb-src/deb-src/g; /^#/d; /^$/d' /etc/apt/sources.list \\
    && apt-get clean \\
    && apt-get update \\
    && touch ~/.netrc \\
    && chmod 600 ~/.netrc \\
    && echo -e 'machine github.com\\n        login not-used\\n        password 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' > ~/.netrc \\
    && apt install -y software-properties-common git build-essential curl wget unzip\\
    && git clone <https://github.com/yym68686/Neovim-config.git> /root/.config/nvim \\
    && git clone --depth 1 <https://github.com/wbthomason/packer.nvim> ~/.local/share/nvim/site/pack/packer/start/packer.nvim \\
    && add-apt-repository ppa:neovim-ppa/stable \\
    && apt install -y neovim \\
    && echo export LESSCHARSET=utf-8 >> ~/.bashrc \\
    && echo alias vim=nvim >> ~/.bashrc \\
    && /bin/bash -c "source ~/.bashrc" \\
    && git config --global user.email "yym68686@outlook.com" \\
    && git config --global user.name "yym68686" \\
    && git clone <https://github.com/yym68686/ics2022.git> \\
    && apt install -y man build-essential gcc-doc gdb git gcc-multilib libreadline-dev libsdl2-dev qemu-system-x86 \\
    && /bin/bash -c "~/ics2022/init.sh && source ~/.bashrc"
```

vim

```docker
FROM ubuntu:18.04.386
WORKDIR ~
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone \\
    && sed -i 's#archive.ubuntu.com#mirrors.163.com#g; s#security.ubuntu.com#mirrors.163.com#g; /# deb-src/d; /^#/d; /^$/d' /etc/apt/sources.list \\
    && apt-get update \\
    && touch ~/.netrc \\
    && chmod 600 ~/.netrc \\
    && echo -e 'machine github.com\\n        login not-used\\n        password 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' > ~/.netrc \\
    && apt install -y git vim build-essential curl jq\\
    && echo export LESSCHARSET=utf-8 >> ~/.bashrc \\
    && git config --global user.email "yym68686@outlook.com" \\
    && git config --global user.name "yym68686" \\
    && curl '<https://api.notion.com/v1/blocks/8b4f12d4fd4c42f0b4dce39ed3fbeb79>' \\
         -H 'Authorization: Bearer secret_8DQN9wRRMpDUgwY3St79g5ltrxL3thq6qdPkKyywqZN' \\
         -H 'Notion-Version: 2022-02-22' | jq -r '.code.rich_text[0].plain_text' > ~/.vimrc \\
    && /bin/bash -c "source ~/.bashrc" \\
    && git clone <https://github.com/yym68686/ics2022.git> \\
    && apt install -y man build-essential gcc-doc gdb git gcc-multilib libreadline-dev libsdl2-dev qemu-system-x86 \\
    && /bin/bash -c "cd /~/ics2022 && git checkout remotes/origin/pa2 && /~/ics2022/init.sh && source ~/.bashrc"
```

从容器退出后重新构建镜像：

```bash
docker rm -f $(docker ps -aq)
docker rmi -f pa
cd /mnt/f/code/PA
curl '<https://api.notion.com/v1/blocks/f940d8fe7afd4651b28b280a2a859e28>' \\
  -H 'Authorization: Bearer secret_8DQN9wRRMpDUgwY3St79g5ltrxL3thq6qdPkKyywqZN' \\
  -H 'Notion-Version: 2022-02-22' | jq -r '.code.rich_text[0].plain_text' > Dockerfile
curl '<https://api.notion.com/v1/blocks/194972d9703e4ac2a1892379cfa4a008>' \\
  -H 'Authorization: Bearer secret_8DQN9wRRMpDUgwY3St79g5ltrxL3thq6qdPkKyywqZN' \\
  -H 'Notion-Version: 2022-02-22' | jq -r '.code.rich_text[0].plain_text' > run.sh
docker build --no-cache --network=host -t pa --platform=linux/386 .
docker exec -it $(docker run -dit pa) bash
```

push脚本：

```bash
cd /CSAPP-Lab
find . -name "btest" -or -name "fshow" -or -name "ishow" | xargs rm -f
git rm -r --cached .
git add .
git commit -m "完成 Lab1"
git push -u origin master
```

### 操作系统实践

远程仓库：

[GitHub - yym68686/OS_practice: NUAA 操作系统实践作业](https://github.com/yym68686/OS_practice)

```docker
cd /mnt/f/code/OS_practice
```

#### 最小系统Neovim版

```bash
nvim +PackerSync
git clone <https://github.com/yym68686/OS_practice.git>
```

push脚本：

```bash
cd ~/OS_practice/job7
make clean
cd ~/OS_practice
find ~/OS_practice -path ~/OS_practice/.git -prune -o -type f -perm /u=x,g=x,o=x | xargs rm -f
git add .
git commit -m "完成 2016eaxm/T2.c"
git push origin main
cd -
clear && gcc sh2.c -o sh2 && ./sh2
sed -i 's#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#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#g' ~/.netrc
```

#### vim版

Dockerfile

```docker
FROM ubuntu:20.04
WORKDIR /OS_practice
COPY run.sh /OS_practice/
COPY id_rsa /root/.ssh/id_rsa
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \\
    && echo 'Asia/Shanghai' > /etc/timezone \\
    && sed -i 's#archive.ubuntu.com#mirrors.163.com#g; s/# deb-src/deb-src/g; /^#/d; /^$/d' /etc/apt/sources.list \\
    && rm -Rf /var/lib/apt/lists/* \\
    && apt-get clean \\
    && apt-get update -y --fix-missing\\
    && touch ~/.netrc \\
    && chmod 600 ~/.netrc \\
    && echo -e 'machine github.com\\n        login not-used\\n        password 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' > ~/.netrc \\
    && apt -y install vim git build-essential curl python jq vim-gtk3 tmux\\
    && mkdir -p ~/.vim/autoload \\
    && mkdir -p ~/.vim/plugged \\
    && chmod 700 /root/.ssh/id_rsa \\
    && chown -R root:root /root/.ssh \\
    && curl '<https://api.notion.com/v1/blocks/8b4f12d4fd4c42f0b4dce39ed3fbeb79>' \\
         -H 'Authorization: Bearer secret_8DQN9wRRMpDUgwY3St79g5ltrxL3thq6qdPkKyywqZN' \\
         -H 'Notion-Version: 2022-02-22' | jq -r '.code.rich_text[0].plain_text' > /root/.vimrc
CMD ["sh", "/OS_practice/run.sh"]
```

[run.sh](http://run.sh)

```bash
echo '192.30.255.113 github.com' >> /etc/hosts
echo '185.199.108.133 raw.githubusercontent.com' >> /etc/hosts
echo 'nameserver 8.8.8.8' >> /etc/resolv.conf
git clone <https://github.com/yym68686/OS_practice.git>
git config --global user.email "yym68686@outlook.com"
git config --global user.name "yym68686"
curl -fLo ~/.vim/autoload/plug.vim --create-dirs <https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim>
cd /OS_practice/OS_practice
/bin/sh
```

从容器退出后重新构建镜像，也可以构建容器时直接运行：

```bash
docker rm -f $(docker ps -aq)
docker rmi -f os_practice
cd /mnt/f/code/OS_practice
curl '<https://api.notion.com/v1/blocks/900989c796c0417984d8b08250e7d901>' \\
  -H 'Authorization: Bearer secret_8DQN9wRRMpDUgwY3St79g5ltrxL3thq6qdPkKyywqZN' \\
  -H 'Notion-Version: 2022-02-22' | jq -r '.code.rich_text[0].plain_text' > Dockerfile
curl '<https://api.notion.com/v1/blocks/20abf086f0c747c7878cc9d146cd11b6>' \\
  -H 'Authorization: Bearer secret_8DQN9wRRMpDUgwY3St79g5ltrxL3thq6qdPkKyywqZN' \\
  -H 'Notion-Version: 2022-02-22' | jq -r '.code.rich_text[0].plain_text' > run.sh
hwclock --hctosys
hwclock -s
apt-get update
while ! docker build --no-cache -t os_practice . ; do sleep 2 ; done ; echo succeed
docker exec -it $(docker run -dit os_practice) bash
```

使用上面的命令的前提是有jq，确保安装jq：

```bash
apt-get update
apt install -y jq
```

push脚本：

```bash
cd /OS_practice/OS_practice
find . -name "*.o" -or -name "*.out" -or -name "test" -or -type f -perm /u=x,g=x,o=x | xargs rm -f
git rm -r --cached .
git add .
git commit -m "add job5"
git push -u origin main
cd /OS_practice/OS_practice/job5
```

TODO：

- [x]  sh1.c exit不能正常退出

### 编译原理实验

Dockerfile

```dockerfile
FROM ubuntu:20.04
ARG SSH_KEY
COPY id_rsa /root/.ssh/id_rsa
RUN sed -i 's#<http://archive.ubuntu.com#http://mirrors.163.com#g>' /etc/apt/sources.list \\
		&& apt-get clean \\
    && apt-get update \\
    && apt -y install vim make flex bison git \\
    && echo -e $SSH_KEY > /root/.ssh/id_rsa \\
    && chmod 700 /root/.ssh/id_rsa \\
    && chown -R root:root /root/.ssh \\
    && ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts \\
    && git clone git@github.com:yym68686/Compilation-lab.git
WORKDIR /Compilation-lab
```

启动容器：

```bash
docker build --build-arg SSH_KEY="$(cat id_rsa)" -t flex:4.0 .
```

[如何在Dockerfile中clone 私库_死磕音视频-CSDN博客](https://blog.csdn.net/qq_28880087/article/details/110441110)

## 编译平台

编译到 x86_64 平台

```bash
docker build -t bot:1.0 --platform linux/amd64 .
```

编译到 x86 平台

```
docker build -t bot:1.0 --platform=linux/386 .
```

## 端口映射

```bash
-p 80:3000
```

把容器的3000端口映射到主机127.0.0.1:80，在本机输入网址127.0.0.1访问网页。

## host 网络模式

默认Docker容器运行会分配独立的Network Namespace隔离子系统，基于host模式，容器将不会获得一个独立的Network Namespace，而是和宿主机共用一个Network Namespace，容器将不会虚拟出自己的网卡，配置自己的IP等，而是使用宿主机的IP和端口。(用的是宿主机的IP，也就是和宿主机共用一个IP地址，host模式不需要加-p进行端口映射，因为和宿主机共享网络IP和端口)

连接到 host 网络的容器共享 Docker host 的网络栈，容器的网络配置与 host 完全一样。可以通过 --network=host 指定使用 host 网络。

对于host模式的思考:
1.host模式下是怎么占领端口的？
host模式端口占用模式是你的容器占用你主机上当前所监听的端口(官网描述为publish)，比如我们都知道tomcat占用8080端口，那么当我们用host模式启动的时候，主机上的8080端口会被tomcat占用，这个时候其他的容器就不能指定我们的8080端口了，但是可以指定其他端口，所以说一台主机上可以运行多个host模式的容器，只要彼此监听的端口不一样就行。

2.host模式下使用-p或者-P会出现WARNING: Published ports are discarded when using host network mode
当你是host模式的时候，主机会自动把他上面的端口分配给容器，这个时候使用-p或者-P是无用的。但是还是可以在Dockerfile中声明EXPOSE端口，关于EXPOSE命令的详细解释接下来我会继续写篇文章。

3.host模式设计的原因
host模式设计出来就是为了性能，访问主机的端口就能访问到我们的容器，使容器直接暴露在公网下，但是这却对docker的隔离性造成了破坏，使得安全性大大降低。这种模式有利有弊，对于每个人来说看法都不一样，具体取舍看个人。

## docker ssh

密码

```bash
vim /etc/ssh/sshd_config
PermitRootLogin yes
PasswordAuthentication yes
service ssh restart
```

密钥

```bash
eval "$(ssh-agent -s)"
chmod 600 privary_key
ssh-add privary_key
vim /etc/ssh/sshd_config
PermitRootLogin yes
PubkeyAuthentication yes
AuthorizedKeysFile  .ssh/authorized_keys
PasswordAuthentication no
service ssh restart
```

## Docker安装

```bash
# Install pip
curl -s <https://bootstrap.pypa.io/get-pip.py> | python3

# Install the latest version docker
curl -s <https://get.docker.com/> | sh

# Run docker service
systemctl start docker

# Install docker compose
pip install docker-compose
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
```

添加Docker官方GPG key

```
curl -fsSL <https://download.docker.com/linux/ubuntu/gpg> | sudo apt-key add -
```

设置Docker稳定版仓库

```
sudo add-apt-repository "deb [arch=amd64] <https://download.docker.com/linux/ubuntu> $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

[如何在Ubuntu 20.04上安装Docker | myfreax](https://www.myfreax.com/how-to-install-and-use-docker-on-ubuntu-20-04/)

更换阿里云：

```bash
sudo vim /etc/docker/daemon.json
{
  "registry-mirrors": [
		 "<https://snj8kuoe.mirror.aliyuncs.com>",
     "<https://hub-mirror.c.163.com>",
     "<https://mirror.baidubce.com>"
  ]
}
```

重启服务：

```
#重载配置文件
sudo systemctl daemon-reload

# 重启docker
sudo systemctl restart docker
```

查看配置是否生效

```
sudo docker info
```



## 配置文件

```bash
vim /root/.docker/config.json
```

## 数据卷

```
docker volume create edc-nginx-vol
docker volume ls
docker volume inspect edc-nginx-vol
docker volume rm edc-nginx-vol
docker run -dit --name=edc-nginx -p 8800:80 -v edc-nginx-vol:/usr/share/nginx/html nginx
```

对于linux ，docker的数据卷可以在 /var/lib/docker/volumes/

[一文了解 Docker 数据卷](https://www.modb.pro/db/41033)

[你必须知道的Docker数据卷(Volume)](https://www.cnblogs.com/edisonchou/p/docker_volumes_introduction.html)

## 多阶段构建

多阶段构建（推荐，比较安全）：

## ENTRYPOINT

Dockerfile中RUN，CMD和ENTRYPOINT都能够用于执行命令，下面是三者的主要用途：

- RUN命令执行命令并创建新的镜像层，通常用于安装软件包
- CMD命令设置容器启动后默认执行的命令及其参数，但CMD设置的命令能够被`docker run`命令后面的命令行参数替换
- ENTRYPOINT配置容器启动时的执行命令（不会被忽略，一定会被执行，即使运行 `docker run`时指定了其他命令）

[ENTRYPOINT 入口点](https://yeasy.gitbook.io/docker_practice/image/dockerfile/entrypoint)

## docker 不用输入 sudo

```bash
# 创建一个docker用户组
sudo groupadd docker
# 添加当前用户到docker用户组
sudo usermod -aG docker $USER
# 重新登陆
```

## Docker命令

### 清理空间

```bash
docker system prune
```

### 所有镜像

```
docker image ls
```

### 查看镜像构建记录

可以逆向出Dockerfile

```bash
docker history <image-name> --no-trunc
```

### 删除镜像

```makefile
docker image rm [imageName]
docker rmi [imageName]
```

删除所有的镜像

```bash
docker rmi $(docker images -q)
```

删除机器构建中间镜像

```
docker rmi -f $(docker images -q --filter label=stage=intermediate)
```

[如何在Dockerfile中clone 私库_死磕音视频-CSDN博客](https://blog.csdn.net/qq_28880087/article/details/110441110)

### 查找镜像

```makefile
docker search httpd
```

### 拉取镜像

```
docker pull ubuntu:18.04
```

### 运行镜像

有了镜像后，我们就能够以这个镜像为基础启动并运行一个容器。以上面的 ubuntu:18.04 为例，如果我们打算启动里面的 bash 并且进行交互式操作的话，可以执行下面的命令：

```
docker run -it --rm ubuntu:18.04 bash
```

- `it`：这是两个参数，一个是 `i`：交互式操作，一个是 `t` 终端。我们这里打算进入 `bash` 执行一些命令并查看返回结果，因此我们需要交互式终端。
- `--rm`：这个参数是说容器退出后随之将其删除。默认情况下，为了排障需求，退出的容器并不会立即删除，除非手动 `docker rm`。我们这里只是随便执行个命令，看看结果，不需要排障和保留结果，因此使用 `-rm` 可以避免浪费空间。执行 docker run 命令带 --rm命令选项，等价于在容器退出后，执行 docker rm -v。
- `ubuntu:18.04`：这是指用 `ubuntu:18.04` 镜像为基础来启动容器。
- `bash`：放在镜像名后的是 **命令**，这里我们希望有个交互式 Shell，因此用的是 `bash`。

### 提交镜像

```
docker tag 840898bb00f3 yym68686/nuaa-course:1.0
docker push yym68686/flex:1.0
```

[使用docker,进行dockerhub仓库上传镜像，拉取镜像。](https://segmentfault.com/a/1190000038927878)

[docker 学习笔记---如何将docker 镜像上传到docker hub仓库_chengly0129的专栏-CSDN博客_docker上传镜像到仓库](https://blog.csdn.net/chengly0129/article/details/70211132)

### 所有容器

```bash
docker container ls -l
```

列出本机所有容器，包括终止运行的容器：

```makefile
docker container ls -l --all
docker container ls -a
docker container ls
```

### 构建容器

Dockerfile

```docker
FROM ubuntu:20.04
RUN apt install vim make
COPY . /home
WORKDIR /home
docker build -t course:1.0 .
```

### 删除容器

```
docker container rm [containerID]
```

删除所有容器

```bash
docker rm -f $(docker ps -aq)
```

强制删除

```makefile
docker rm -f 容器ID/名字
```

显示 Ubuntu 系统信息

```
cat /etc/os-release
```

### 提交容器

```makefile
docker commit -m="has update" -a="runoob" e218edb10161 runoob/ubuntu:v2
```

各个参数说明：

- **m:** 提交的描述信息
- **a:** 指定镜像作者
- **e218edb10161：**容器 ID
- **runoob/ubuntu:v2:** 指定要创建的目标镜像名

容器提取为镜像：

```
docker commit containerNAME/ID yym68686/flex:1.0
docker tag imageNAME/ID yym68686/flex:1.0
docker push yym68686/flex:1.0
```

### 查看容器日志

```bash
docker logs <container-name>
```

### 提取容器文件

```bash
sudo mkdir -p /home/docker/mysql/conf && sudo mkdir -p /home/docker/mysql/datadir
CID=`docker run -d yym68686/nuaa-course:3.0` \\
&& sudo docker cp $CID:/etc/mysql /home/docker/mysql/conf \\
&& sudo docker cp $CID:/var/lib/mysql /home/docker/mysql/datadir \\
&& docker stop $CID \\
&& docker rm $CID
```

### 导出容器

```
docker export [OPTIONS] CONTAINER
```

### 导入容器

```
docker import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]
```

### 容器换源

向/etc/apt/sources.list文件写入网易镜像地址

```
sed -i 's#archive.ubuntu.com#mirrors.163.com#g; s#security.ubuntu.com#mirrors.163.com#g; s/# deb-src/deb-src/g; /^#/d; /^$/d' /etc/apt/sources.list
```

## 复制容器文件到宿主机

```
docker cp ${containerID}:${sourcePath} ${localPath}
```

[掘金](https://juejin.cn/post/6844904179589201933)

## 查看容器日志

```bash
docker logs --since 30m 容器id
```

[前言](https://yeasy.gitbook.io/docker_practice/)

[Docker Hub Container Image Library | App Containerization](https://hub.docker.com/)

[Docker 命令大全](https://www.runoob.com/docker/docker-command-manual.html)

[随笔分类 - 测试高级进阶技能系列 - Docker](https://www.cnblogs.com/poloyy/category/1870863.html)

## 设置容器时区

```
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone
```

## 容器挂载宿主机文件目录

```bash
docker run -it -v /home/dock/Downloads:/usr/Downloads ubuntu:20.04 bash
docker run -d -P --name web --mount type=bind,source=/src/webapp,target=/usr/share/nginx/html nginx:alpine
```

-d: 后台运行容器，并返回容器ID

-P: 随机端口映射，容器内部端口随机映射到主机的端口

[掘金](https://juejin.cn/post/6844904179589201933)

## docker-compose

启动所有服务

```bash
docker-compose up -d
```

停止和删除容器、网络、卷、镜像：

```bash
docker-compose down
```

列出项目中目前所有的容器：

```bash
docker-compose ps
```

构建（重新构建）项目中的服务容器：

```bash
docker-compose build
```

进入容器：

```bash
docker-compose exec -it webapp bash
```

[docker-compose 使用介绍](https://www.cnblogs.com/cocowool/p/docker-compose-introduce.html)

## 脚本

yym68686/flex:1.0 vim,make,official

```
docker pull yym68686/flex:1.0
docker run -dit --privileged --name lex --mount type=bind,source=C:/Users/15497/Desktop,target=/home yym68686/flex:1.0
docker exec -it lex bash
date -s 11:15:45
cd /home
make
```

yym68686/flex:2.0 vim,make,alibaba

```
docker pull yym68686/flex:1.0
docker run -dit --privileged --name lex --mount type=bind,source=C:/Users/15497/Desktop,target=/home yym68686/flex:1.0
docker exec -it lex bash
date -s 11:15:45
cd /home
make
docker run -dit ubuntu:20.04
docker container ls
docker exec -it 5e89 bash
docker rm -f 5e89
```

自定义名称：

```bash
docker run -dit --name nuaa ubuntu:20.04
docker container ls
docker exec -it nuaa bash
docker rm -f flex
```

数据卷：

```bash
docker run -dit --privileged --name flex --mount type=bind,source=C:/Users/15497/Desktop,target=/home ubuntu:20.04
docker container ls
docker exec -it flex bash
docker rm -f flex
docker container restart flex
docker container stop flex
docker run -dit --privileged --name lex --mount type=bind,source=C:/Users/15497/Desktop,target=/home yym68686/flex:1.0
docker pull yym68686/flex:1.0
docker run -dit yym68686/flex:1.0
docker container ls
docker start lex
docker exec -it lex bash
docker rm -f lex
docker container restart lex
docker container stop lex
```

