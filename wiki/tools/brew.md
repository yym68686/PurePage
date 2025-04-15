# Mac 命令

## brew 重置默认源

### 重置 brew.git

```bash
cd "$(brew --repo)"
git remote set-url origin https://github.com/Homebrew/brew.git
```

### 重置核心软件仓库

```bash
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://github.com/Homebrew/homebrew-core.git
```

### 重置 Homebrew cask 软件仓库

```bash
cd "$(brew --repo)"/Library/Taps/homebrew/homebrew-cask
git remote set-url origin https://github.com/Homebrew/homebrew-cask
```

### 重置 Homebrew Bottles 源

注释掉bash配置文件里的有关Homebrew Bottles即可恢复官方源。 重启bash或让bash重读配置文件。

## 更改包内容

```bash
brew edit package
```

## 打开窗口内部拖动功能

```bash
defaults write -g NSWindowShouldDragOnGesture -bool true
```

注销或重新登录

## 关闭窗口内部拖动功能

```bash
defaults delete -g NSWindowShouldDragOnGesture
```

## 关机

- Ctrl + 关机：弹出关机提示
- Ctrl + Option + 关机 ： 正常关机快捷键
- Command + Option + 关机 ：进入休眠状态
- Ctrl + Command + 关机：重启机器

