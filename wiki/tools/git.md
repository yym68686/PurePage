# Git

教程：https://town.korandoru.io/individuals/git-bootcamp

## 搜索

- 使用git log -S命令，它会返回所有添加或删除了指定字符串的commit。例如，git log -S ContentWrapper.
- 使用git log --grep命令，它会返回所有commit日志中包含指定字符串的commit^3^。例如，git log --grep "ContentWrapper"。
- 使用git rev-list和 grep命令，它们可以在指定的文件或者所有文件中搜索字符串。例如，git rev-list --all foo.rb | ( while read revision; do git grep -F 'bar' $revision foo.rb done )。

## 初始化

用户名

```bash
git config --global user.email "yym68686@outlook.com"
git config --global user.name "yym68686"
```

或者

```bash
git config --global user.name "dcdcvgroup"
git config --global user.email "dcdcvgroup1@163.com"
```

## 一键 push

```bash
cd ~/path
git add .
git commit -m "first"
git push origin $(git name-rev --name-only HEAD)
```

初始化并 push

```bash
git init
git remote add origin https://github.com/yym68686/Rust-play.git
git add .
git commit -m "first"
git push origin $(git name-rev --name-only HEAD)
```

## 代理

clash 虚拟机使用 socks5 代理（Mac 的 ip 为 10.211.55.2）

```bash
git config --global http.proxy socks5://10.211.55.2:7890
git config --global https.proxy socks5://10.211.55.2:7890
```

surge 使用 socks5 代理

```bash
git config --global http.proxy socks5://127.0.0.1:6153
git config --global https.proxy socks5://127.0.0.1:6153
```

使用 http 代理

```bash
git config --global http.proxy http://192.168.50.88:7890
git config --global https.proxy https://192.168.50.88:7890
```

取消全局代理

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
```

只对 github.com 代理，其他仓库不走代理

```bash
git config --global http.<https://github.com.proxy> socks5://127.0.0.1:10808
git config --global https.<https://github.com.proxy> socks5://127.0.0.1:10808
```

取消 github 代理

```bash
git config --global --unset http.<https://github.com.proxy>
git config --global --unset https.<https://github.com.proxy>
```

## 全局 gitignore

```bash
cat >> ~/.gitconfig <<EOF
[core]
	excludesfile = /Users/yanyuming/.gitignore_global
EOF
cat >> ~/.gitignore_global <<EOF
__pycache__/
.DS_Store
.vscode
EOF
```

## rebase

同一个问题提交了好几次，需要合并所有的重复 commit，使用 rebase 命令，合并最新 4 个 commit。

```bash
git rebase -i HEAD~4
```

在 vim 里面把不需要的 commit 的 pick 改为 s，接着退出

```bash
git rebase --continue
```

把不需要的 commit message 删掉，最后需要强制提交

```bash
git push -f origin $(git name-rev --name-only HEAD)
```

## 使用 --depth 1 时拉取其他分支

```bash
git clone --depth 1 https://github.com/dogescript/xxxxxxx.git
git remote set-branches origin 'remote_branch_name'
git fetch --depth 1 origin remote_branch_name
git checkout remote_branch_name
```

## .gitignore 规则

https://www.myfreax.com/gitignore-ignoring-files-in-git/

### 忽略以前提交的文件

```bash
git rm --cached filename
```

`--cached`选项告诉 git 不要从工作树中删除文件，而只是从索引中删除它。要递归删除目录，请使用`-r`选项：

```bash
git rm -r --cached dirname
```

### 显示所有被忽略的文件

```bash
git status --ignored
```

### 让修改的 .gitignore 生效

```bash
git rm -r --cached . > /dev/null
git add .
git commit -m "修改 readme，更新细节说明"
git push -u origin $(git name-rev --name-only HEAD)
```

## 增加远程仓库

```bash
git remote add origin https://github.com/yym68686/CSAPP-Lab.git
```

## 远程仓库地址 重置

```bash
git remote rm [repo-name]
git remote add [repo-name] [repo-url]
```

一步到位

```bash
git remote set-url origin https://github.com/username/repo.git
```

## 关闭 ssl 认证

```bash
git config --global http.sslVerify "false"
```

## 免密 push

### http

```bash
touch ~/.netrc
chmod 600 ~/.netrc
cat > ~/.netrc << EOF
machine github.com
login not-used
password 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
EOF
```

### SSH

生成新的公私钥

```bash
ssh-keygen -t rsa -b 4096 -C "label"
```

将公钥添加到 github 账号 ssh 设置里面。然后将私钥被添加到 SSH 代理，SSH 客户端可以自动使用这个代理中的私钥进行认证，无需用户手动指定私钥文件。

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/dcdcv
```

一键上传脚本

```bash
set -eu
git init
git add .
git commit -m "first"
git remote add origin git@github.com:dcdcvgroup/layout-diffusion-mindspore.git
git push -u origin main
```

[GitHub如何配置SSH Key_前端向朔-CSDN博客_github ssh](https://blog.csdn.net/u013778905/article/details/83501204)

## 修改上一次提交信息

```bash
git commit -v --amend
```

## 强制删除某次 commit

```go
git rebase -i commitID
```

把pick改为drop，然后：

```go
git push -f origin master
```

## 换行

Git 可以在你提交时自动地把回车（CR）和换行（LF）转换成换行（LF），而在检出代码时把换行（LF）转换成回车（CR）和换行（LF）。 你可以用 `git config --global core.autocrlf true` 来打开此项功能。 如果是在 Windows 系统上，把它设置成 true，这样在检出代码时，换行会被转换成回车和换行：

```bash
git config --global core.autocrlf true
```

[关于git提示&#34;warning: LF will be replaced by CRLF&#34;终极解答](https://www.jianshu.com/p/450cd21b36a4)

## push 文件大小

报错fatal: the remote end hung up unexpectedly

设置推送文件最大512MB

```bash
git config --local http.postBuffer 524288000
```

## 分支

### 切换分支

```bash
git checkout mybranch
```

### 创建并切换分支

```bash
git checkout -b mybranch
```

### 新建分支并切换到指定分支

```bash
git checkout -b dev origin/release/caigou_v1.0
```

### 回滚到上一个版本

#### git reset

```bash
git reset --hard HEAD^
git push --force origin
```

找回之前的提交记录

```bash
git reflog
git reset --hard HEAD@{n}
```

#### git revert

撤销最近的一次 commit，并自动创建一个新的 commit

```bash
git revert HEAD
```

撤销最近的一次 commit，不会自动创建一个新的 commit，而是将修改放到暂存区，您需要手动执行 git commit 来完成撤销

```
git revert -n HEAD
```

#### `git revert` 和 `git reset` 区别

"git revert" 和 "git reset" 都是 Git 中用于撤消更改的命令，但它们的作用不同。

- "git reset" 命令用于将分支指向之前的提交记录，从而撤消更改。这个命令会永久删除之前的提交记录，并且不能撤销。可以用来回退分支到之前的状态，但是会丢失之后的提交记录。
- "git revert" 命令用于创建一个新的提交记录，该记录撤消之前的提交记录。这个命令不会删除之前的提交记录，而是会创建一个新的提交记录，该记录包含了撤消更改的内容。可以用来撤消任何之前的提交记录，并且不会丢失之后的提交记录。

因此，如果您想要撤销之前的更改，并且不希望丢失之后的提交记录，那么 "git revert" 是更好的选择。如果您想要完全删除之前的提交记录并回退分支到之前的状态，那么 "git reset" 是更好的选择。

### 查看本地分支及其对应的远程分支

```bash
git branch -vv
```

查看远程分支和本地分支的对应关系

```python
git remote show origin
```

### 显示所有分支

```python
git branch -a
```

### 查看本地分支

```python
git branch -r
```

### 同步远程分支

```python
git fetch
```

### 拉取远程指定分支到本地

```bash
git fetch origin pa3
git checkout -b pa3 remotes/origin/pa3
```

同步别人新增到远程的分支

```python
# 查看本地分支
git branch
# 查看远程分支，对比远程存在哪些本地没有的新分支
git branch -a
# 将某个远程主机的更新，全部取回本地
git fetch
# 查看远程分支
git branch -a
# 拉取远程分支到本地
git checkout -b remotebranchname
```

### 删除本地分支

```python
git branch -d localbranchname
```

强制删除本地分支

```bash
git branch -D localbranchname
```

### 先删除远程分支再删除本地分支

```python
git push origin --delete master
```

清除远程已删除本地还在的多余分支

```python
git fetch -p
```

### 先删除本地分支再删除远程分支

```python
# 删除本地分支
git branch -d localbranchname
# 删除远程分支
git push origin -d remotebranchname
# 查看分支情况
git branch -a
```

### 显示当前分支

```bash
git name-rev --name-only HEAD
```

## 恢复文件

```bash
git checkout [log-id] [path/to/file]
```

## 查看全局设置

```bash
git config -l
```

## 显示提交历史记录

```bash
git reflog show
```

## git log 乱码

```bash
echo export LESSCHARSET=utf-8 >> ~/.bashrc
source ~/.bashrc

```

## git status乱码

```bash
git config --global core.quotepath false
```

## git push出现 `error: src refspec main does not match any`

```
git checkout -b main
```

References

[https://blog.csdn.net/bjbz_cxy/article/details/113931821](https://blog.csdn.net/bjbz_cxy/article/details/113931821)

## rejected non-fast-forward

```bash
git fetch --all
git pull $(git name-rev --name-only HEAD)
git add . && git commit -m "$1" && git push origin $(git name-rev --name-only HEAD)
```

## warning: LF will be replaced by CRLF in

```bash
git config core.autocrlf true
```

## 显示调试信息

```bash
export GIT_TRACE_PACKET=1
export GIT_TRACE=1
export GIT_CURL_VERBOSE=1
```

## 查看某次 commit 的修改内容

```c
git show commitId
```

查看某次 commit 中具体某个文件的修改：

```c
git show commitId fileName
```

## diff

### 比较两个分支之间最新 commit 某个文件的区别

```
git diff <branch1> <branch2> -- path/to/file
```

### 比较两次 commit 之间某个文件的区别

```c
git diff commitID commitID -- path/to/file
```

### 比较两次 commit 之间所有发生更改的文件名

```c
git diff commitID commitID --stat
```

## 回滚到某次 commit

```c
git reset --hard commit_id
```

## 回滚到上一个版本

```c
git reset --hard HEAD^
```

## 命令行快捷键

| 目的                                                                                                               | 快捷键    |
| ------------------------------------------------------------------------------------------------------------------ | --------- |
| 将光标后移一个字符                                                                                                 | Ctrl-B    |
| 左箭头                                                                                                             |           |
| 将光标前移一个字符                                                                                                 | Ctrl-F    |
| 右箭头                                                                                                             |           |
| 将光标后移一个词                                                                                                   | Esc-B     |
| 将光标前移一个词                                                                                                   | Esc-F     |
| 将光标移到行首                                                                                                     | Ctrl-A    |
| 将光标移到行尾                                                                                                     | Ctrl-E    |
| 删除从行首到光标处的命令行内容并将其保存到剪切缓冲区中。剪切缓冲区的作用类似于临时内存，在某些程序中类似于剪贴板。 | Ctrl-U    |
| 删除从光标到行尾的命令行内容并将其保存到剪切缓冲区中                                                               | Ctrl-K    |
| 删除从光标到下一个词尾的命令行内容并将其保存到剪切缓冲区中                                                         | Esc-D     |
| 删除光标前面的词并将其保存到剪切缓冲区中                                                                           | Ctrl-W    |
| 提取剪切缓冲区的内容并将其推送到光标处的命令行中                                                                   | Ctrl-Y    |
| 删除光标前面的字符                                                                                                 | Ctrl-H    |
|                                                                                                                    | Backspace |
| 删除光标处的字符                                                                                                   | Ctrl-D    |
| 清除行                                                                                                             | Ctrl-C    |
| 清除屏幕                                                                                                           | Ctrl-L    |
| 将命令行的当前内容替换为历史记录列表中的前一个条目。每按一次此快捷键，历史记录光标就会向前移动一个条目。           | Ctrl-P    |
|                                                                                                                    | Esc-P     |
| 上箭头                                                                                                             |           |
| 将命令行的当前内容替换为历史记录列表中的下一个条目。每按一次此快捷键，历史记录光标就会向后移动一个条目。           | Ctrl-N    |
|                                                                                                                    | Esc-N     |
| 下箭头                                                                                                             |           |
| 从当前编辑位置展开输入的部分命令或列出有效输入                                                                     | Tab       |
|                                                                                                                    | Ctrl-I    |
| 显示上下文相关帮助                                                                                                 | ?         |
| 对问号（“?”）字符的特殊映射进行转义。例如，要在命令的参数中输入问号，请依次按 Esc 和“?” 字符。                 | Esc-?     |
| 启动 TTY 输出                                                                                                      | Ctrl-Q    |
| 停止 TTY 输出                                                                                                      | Ctrl-S    |

## Go

设置代理：

```bash
go env -w GOPROXY=https://goproxy.cn
```

开启模块：

```bash
go env -w GO111MODULE=on
go mod init <dirname>
```

//初始化模块：
Go mod init <项目模块名称>

//依赖关系处理，清除这些未使用的依赖项,根据go.mod文件
Go mod tidy

//将依赖包复制到项目的vendor目录
Go mod vendor

//显示依赖关系
Go list -m all

//显示详细依赖关系
Go list -m -json all

//下载依赖
Go mod download [path@version]

[解决go: go.mod file not found in current directory or any parent directory； see &#39;go help modules&#39;_林猛男的博客-CSDN博客](https://blog.csdn.net/longgeaisisi/article/details/121288696)

## Java 多版本环境

```powershell
[environment]::SetEnvironmentvariable("JAVA_HOME", "%JAVA16_HOME%", "Machine")
[environment]::SetEnvironmentvariable("JAVA8_HOME", "D:\\java", "Machine")
[environment]::SetEnvironmentvariable("JAVA16_HOME", "D:\\java16", "Machine")
[environment]::SetEnvironmentvariable("JAVA17_HOME", "D:\\java17", "Machine")
[environment]::SetEnvironmentvariable("CLASSPATH", ".;%JAVA_HOME%\\lib\\dt.jar;%JAVA_HOME%\\lib\\tools.jar;", "Machine")
[environment]::SetEnvironmentvariable("PATH", "$([environment]::GetEnvironmentvariable("Path", "Machine"));%JAVA_HOME%\\bin", "Machine")
```
