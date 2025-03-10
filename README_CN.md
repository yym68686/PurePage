# PurePage

[英文](README.md) | [中文](README_CN.md)

PurePage 是一个极简主义的博客页面，完全基于原生 HTML、JS 和 CSS 实现，主要功能是渲染 Markdown 文章内容，支持渲染 Latex 数学公式，让你专注于写作，而不必担心复杂的博客系统设置和维护。PurePage 注重本地化和数据自主性，确保你的内容始终在你的控制之下。支持部署在 GitHub Pages，vercel 和 Cloudflare Pages。坚持本地优化，不依赖任何第三方服务。

我开发 PurePage 是因为我尝试过许多不同的博客系统，比如 Hexo, Docusaurus 2 和 Notion，依赖了太多没有必要的东西，要么难以定制自己想要的功能，要么数据难以迁移，难以使用。我希望有一个简单高效的博客页面，让写作变得更轻松。

PurePage 的特点是非常简单，没有多余的设置和复杂的功能，只有一个简单的搜索功能和自动生成的文章列表。同时，PurePage 的渲染效果非常好，使你的文章看起来更加美观和专业。

如果你是一位极简主义的博主，正在寻找一个简单高效、注重数据自主性和本地化的博客页面，那么 PurePage 绝对是一个不错的选择。欢迎你尝试并提出反馈和建议。

## ✨ 特性

- 原生 HTML、JS 和 CSS 实现

- 支持 Markdown 渲染

- 支持 Latex 数学公式渲染

- 支持 Mermaid 图表渲染

- 支持代码高亮

- 自适应界面

## 🚀 网页版部署

1. 你可以一键将 PurePage 部署到 Vercel：

[![使用 Vercel 部署](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyym68686%2FPurePage)

2. 你可以部署到 Cloudflare Pages：

```bash
# 安装 Wrangler CLI
npm install -g wrangler

# 登录 Cloudflare
wrangler login

# 部署到 Cloudflare Pages（带 SSL 配置）
wrangler pages deploy . --project-name purepage --branch main
```

3. 你也可以部署到 GitHub Pages：

```bash
# Fork 这个仓库
# 然后进入你的仓库的 Settings -> Pages
# 在"构建和部署"部分：
# - 将"Source"选择为"Deploy from a branch"
# - 选择你的分支（main/master）和根目录（/）
# - 点击保存
```

## 使用指南

运行 `generate-sidebar-structure.js` 生成侧边栏文件列表

```bash
node generate-sidebar-structure.js
```

运行 `init.py` 生成首页目录

```bash
python init.py
```