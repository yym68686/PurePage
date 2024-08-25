# Mac & Windows 系统相关

打开任何应用

```bash
sudo xattr -r -d com.apple.quarantine /Applications/QuickRecorder.app/
sudo spctl  --master-disable
codesign --force --deep --sign - /Applications/QuickRecorder.app/
```

## 全部 UWP 应用 loopback 豁免

```powershell
foreach ($n in (get-appxpackage).packagefamilyname) {checknetisolation loopbackexempt -a -n="$n"}
```

## powershell 相关

### 显示环境变量

显示所有环境变量

```bash
ls env:
```

显示Path环境变量

```bash
$env:Path
```

列表分割换行显示

```bash
(type env:path) -split ';'
```

过滤搜索包含bin的条目

```bash
(type env:path) -split ';' | sls bin
```

显示用户环境变量

```bash
[environment]::GetEnvironmentvariable("Path", "User")
```

按行显示用户环境变量

```bash
([environment]::GetEnvironmentvariable("Path", "User")) -split ';'
```

显示系统环境变量

```bash
[environment]::GetEnvironmentvariable("Path", "Machine")
```

按行显示系统环境变量

```bash
([environment]::GetEnvironmentvariable("Path", "Machine")) -split ';'
```

### 设置环境变量

#### 临时

创建环境变量，只对当前会话有效

```bash
$env:Test1="sysin.org"
```

追加环境变量

```
$env:变量名称="$env:变量名称;变量值"
```

在 PATH 后面追加一条

```
$env:Path="$env:Path;C:\sysin"
```

#### 持久化

写入环境变量：

```bash
# 用户变量
[environment]::SetEnvironmentvariable("变量名称", "变量值", "User")

# 系统变量
[environment]::SetEnvironmentvariable("变量名称", "变量值", "Machine")

```

Powershell 实现如下：

```bash
[environment]::SetEnvironmentvariable("GOPATH", "$env:USERPROFILE\\gopath", "User")
#调用命令结果：$(命令)
#获取原有用户 PATH 变量：$([environment]::GetEnvironmentvariable("Path", "User"))
#注意 PATH 中条目以分号结尾
[environment]::SetEnvironmentvariable("PATH", "$([environment]::GetEnvironmentvariable("Path", "User"));%GOPATH%\\bin", "User")

[environment]::SetEnvironmentvariable("GOROOT", "C:\\go", "Machine")
#调用命令结果：$(命令)
#获取原有系统 PATH 变量：$([environment]::GetEnvironmentvariable("Path", "Machine"))
[environment]::SetEnvironmentvariable("PATH", "$([environment]::GetEnvironmentvariable("Path", "Machine"));%GOROOT%\\bin", "Machine")

```

### 删除环境变量

语法：`del env:变量名称`

```powershell
del env:windir
```

### 删除文件

递归删除

```powershell
Get-ChildItem -Path $pwd -Recurse -Include *.o,*.exe,*Sample | Remove-Item -force -recurse
```

### powershell 路径

```bash
C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe
```

### Powershell 7 PSReadLine 代码提示配置

powershell版本要大于5.1，windows自带5.1，查看软件版本：

```bash
$PSVersionTable
```

升级 powershell

```bash
winget search powershell
winget install Microsoft.PowerShell
```

[让你的windows shell更好用，打造类fish/zsh的powershell - 掘金](https://juejin.cn/post/6984620463917891614)

在非管理员运行的shell中安装scoop

先设置策略

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

安装

```bash
iwr -useb get.scoop.sh | iex
```

查看官方收录的桶

```bash
scoop bucket known
```

安装oh-my-posh

```bash
scoop install oh-my-posh3
```

[回到Windows，最全教程让你的Powershell更好看且好用(2021版)](https://amao.run/zh/posts/%E5%9B%9E%E5%88%B0windows%E6%9C%80%E5%85%A8%E6%95%99%E7%A8%8B%E8%AE%A9%E4%BD%A0%E7%9A%84powershell%E6%9B%B4%E5%A5%BD%E7%9C%8B%E4%B8%94%E5%A5%BD%E7%94%A82021%E7%89%88/)

[Oh My Posh：全平台终端提示符个性化工具 - 少数派](https://sspai.com/post/69911)

主题预览

[Themes | Oh My Posh](https://ohmyposh.dev/docs/themes)

主题路径

```bash
C:\\Users\\15497\\scoop\\apps\\oh-my-posh\\current\\themes
```

### PowerShell 策略

```bash
Set-ExecutionPolicy Unrestricted
```

```bash
Set-ExecutionPolicy bypass
```

```bash
set-executionpolicy RemoteSigned
```

```bash
get-ExecutionPolicy
```

 **Restricted** ：禁止运行任何脚本和配置文件。

**AllSigned** ：可以运行脚本，但要求所有脚本和配置文件由可信发布者签名，包括在本地计算机上编写的脚本。

**RemoteSigned** ：可以运行脚本，但要求从网络上下载的脚本和配置文件由可信发布者签名；       不要求对已经运行和已在本地计算机编写的脚本进行数字签名。

**Unrestricted** ：可以运行未签名脚本。（危险！）

### 访问 powershell 编码

```bash
$OutputEncoding
```

或者：

```powershell
[psobject].Assembly.GetTypes() | Where-Object { $_.Name -eq 'ClrFacade'} |
  ForEach-Object {
    $_.GetMethod('GetDefaultEncoding', [System.Reflection.BindingFlags]'nonpublic,static').Invoke($null, @())
  }
```

## windows 系统别名

[PowerShell设置命令别名Alias](https://segmentfault.com/a/1190000015928399)

查看别名

```docker
Get-Alias
```

添加别名

```docker
Set-Alias list get-childitem
```

注意使用该命令设定的别名只在目前的Windows PowerShell session中生效。也就是说在关闭此会话后这个别名将会失效。

创建永久的别名：

查看配置文件：

```docker
$profile
```

添加

```docker
Set-Alias ls getFileName
```

删除别名ls：

```docker
Remove-Item alias:\\ls
```

## texlive vscode

镜像地址：

[CTAN Sites](https://ctan.org/mirrors)

[Visual Studio Code (vscode)配置LaTeX](https://zhuanlan.zhihu.com/p/166523064)

## host 文件位置

```bash
C:\\WINDOWS\\system32\\drivers\\etc
```

## 注册表

### 修改注册表数值

```bash
REG add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\HRWSCCtrl" /v "Start" /t REG_DWORD /d "3" /f
REG add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\HipsDaemon" /v "Start" /t REG_DWORD /d "3" /f
```

### 设置自启动位置

```bash
Hkey_local_machine\\software\\wow6432node\\microsoft\\windows\\currentversion\\run
```

### 网络注册表位置

可将 wifi 后面的数字删除：

```bash
HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Profiles
```

目录下全部删掉。

References

[【已解决】如何删除Windows10系统中Wifi名称后边的数字._milaoshu1020的专栏-CSDN博客_win10wifi名称后面多了个2](https://blog.csdn.net/milaoshu1020/article/details/88547267)

## 彻底关闭hyper-v 虚拟化

关闭服务

```
bcdedit /set hypervisorlaunchtype off
```

开启服务

```
bcdedit /set hypervisorlaunchtype auto
```

打开开始菜单，Windows管理工具，系统信息。划到最下面。就可以查看是否开启hyper-v。

## 强制删除脚本

```bash
DEL /F /A /Q \\\\?\\%1  
RD /S /Q \\\\?\\%1
```

## 启动 文件夹 路径

```bash
C:\\Users\\15497\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup
```

## bat 管理员运行

```bash
@echo off
cd /d "%~dp0"
cacls.exe "%SystemDrive%\\System Volume Information" >nul 2>nul
if %errorlevel%==0 goto Admin
if exist "%temp%\\getadmin.vbs" del /f /q "%temp%\\getadmin.vbs"
echo Set RequestUAC = CreateObject^("Shell.Application"^)>"%temp%\\getadmin.vbs"
echo RequestUAC.ShellExecute "%~s0","","","runas",1 >>"%temp%\\getadmin.vbs"
echo WScript.Quit >>"%temp%\\getadmin.vbs"
"%temp%\\getadmin.vbs" /f
if exist "%temp%\\getadmin.vbs" del /f /q "%temp%\\getadmin.vbs"
exit

:Admin
```

## WSL 静态ip

```bash
wsl -d Ubuntu-20.04 -u root ip addr add 192.168.50.16/24 broadcast 192.168.50.255 dev eth0 label eth0:1
netsh interface ip add address "vEthernet (WSL)" 192.168.50.88 255.255.255.0
```

```bash
powershell.exe -Command 'netsh interface ip add address "vEthernet (WSL)" 192.168.50.88 255.255.255.0 > $null'
```

## WSL 安装问题

WslRegisterDistribution failed with error: 0x800701bc

[WSL2 Linux kernel update package for x64 machines (windows.net)](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)

WslRegisterDistribution failed with error: 0x80370102

控制面板→程序→虚拟机平台

## WSL ping 不通主机

```powershell
New-NetFirewallRule -DisplayName "WSL" -Direction Inbound  -InterfaceAlias "vEthernet (WSL)"  -Action Allow
```

## 软链接

创建软链接：

```bash
MKLINK [[/D] | [/H] | [/J]] Link Target
说明：
/D 创建目录符号链接而不是文件符号链接（默认为文件符号链接）
/H 创建硬链接而不是符号链接
/J 创建目录连接点
Link 指定新的符号链接名称
Target 指定新链接引用的路径（绝对路径或者相对路径均可）
```

例子：

```bash
mklink /d "D:\\OneDrive - nuaa.edu.cn\\我的坚果云" F:\\我的坚果云
```

[让Onedrive云盘同步本地任意一个文件夹（适用于Windows）_Caleb Sung的博客-CSDN博客_onedrive同步指定文件夹](https://blog.csdn.net/qq_41933331/article/details/86761373)

## rmdir 命令删除文件夹软链

```bash
删除一个目录。

RMDIR [/S] [/Q] [drive:]path
RD [/S] [/Q] [drive:]path

/S      除目录本身外，还将删除指定目录下的所有子目录和
            文件。用于删除目录树。

/Q      安静模式，带 /S 删除目录树时不要求确认
```

## 代理设置

```
localhost;127.*;10.*;172.16.*;172.17.*;172.18.*;172.19.*;172.20.*;172.21.*;172.22.*;172.23.*;172.24.*;172.25.*;172.26.*;172.27.*;172.28.*;172.29.*;172.30.*;172.31.*;192.168.*;117.21.200.166;pypi.tuna.tsinghua.edu.cn
```

## 文件树

```powershell
tree dirpath /F /A > log.txt
```

/F   显示每个文件夹中文件的名称。
/A   使用 ASCII 字符，而不使用扩展字符。

[【Windows 10】目录文件树_tiotdiz的博客-CSDN博客_文件树](https://blog.csdn.net/tiotdiz/article/details/83819305)

## 开始菜单路径

```
C:\\Users\\15497\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs
```

## Windows Terminal 路径

```bash
C:\\Program Files\\WindowsApps\\Microsoft.WindowsTerminal_1.12.10983.0_x64__8wekyb3d8bbwe\\wt.exe
```

## Win+X路径

```
C:\\Users\\15497\\AppData\\Local\\Microsoft\\Windows\\WinX\\Group3
```

## 查看本地端口使用情况

```bash
netstat -o
```

## 查看端口占用

```bash
netstat -aon
```

## 查找某个端口的使用情况

```bash
netstat -aon | findstr "8080"
```
