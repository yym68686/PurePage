# PurePage

[英文](README.md) | [中文](README_CN.md)

PurePage 是一个极简主义的博客页面，完全基于 FastHTML，并可以使用内置的 Markdown 来渲染文章内容，支持渲染数学公式，让你专注于写作，而不必担心复杂的博客系统设置和维护。PurePage 注重本地化和数据自主性，确保你的内容始终在你的控制之下。

我开发 PurePage 是因为我尝试过许多不同的博客系统，比如 Hexo, Docusaurus 2 和 Notion，但总觉得它们太复杂，难以使用。最近出现了 FastHTML 让我能够通过仅编写 python 代码就能完成网站的开发。因此，我想到了使用 FastHTML 来创建一个简单的博客页面，让写作变得更轻松。

PurePage 的特点是非常简单，没有多余的设置和复杂的功能，只有一个简单的搜索功能和自动生成的文章列表。同时，PurePage 的渲染效果非常好，使你的文章看起来更加美观和专业。

如果你是一位极简主义的博主，正在寻找一个简单高效、注重数据自主性和本地化的博客页面，那么 PurePage 绝对是一个不错的选择。欢迎你尝试并提出反馈和建议。

## ✨ 特性

- 前后端完全使用 python 编写，前端使用 FastHTML 和 tailwind.css 实现

- markdown 渲染

- 自适应界面

## 使用指南

运行 `scripts/Deploy.py` 生成首页目录

```bash
python scripts/Deploy.py
```

获取自定义样式列表

```bash
python test/te_re.py
```

生成自定义样式

```bash
npx tailwindcss -o ./static/tailwind.css --config tailwind.config.js
```