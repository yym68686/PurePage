# 一个极简主义者的博客页面

以前试过很多不同的博客系统，比如 Hexo，[Docusaurus 2](https://docusaurus.io/)，notion。我总是觉得太复杂，所以我想到了完全用 Github page 做一个博客页面，之所以它不叫博客系统，因为它足够简单，甚至 markdown 渲染用的完全是 github 自有的 [GitHub Flavored Markdown](https://github.github.com/gfm/)。首先我对这个项目的想象就是满足简单的搜索功能。目前已经有的功能是自动生成文章列表，以后有空自己想重新造一个 markdown 语法解析器。

项目地址：https://github.com/yym68686/PurePage，目前还处于开发 Private 阶段，后面大致开发完了会 public。项目的名字叫 PurePage，这是我让 ChatGPT 给我想的名字。首先这个项目极为简单，可以说是一个玩具项目，但我是一个实用主义与极简主义者，我希望可以用最少的步骤解决简单的问题。

## TODO list

- [x] 自动在首页生成文章列表
- [x] 文章列表自动删除原来的列表，重新构建一个
- [x] 自动 git 推送
- [ ] Deploy.py 终端 log 颜色优化
- [ ] README 多语言支持
- [x] 内建搜索功能
- [ ] markdown 语法解析器
- [ ] 字体设置
- [x] 每篇文章的目录生成
- [x] 生成 sitemap.xml 文件，优化 SEO



使用 Apple scripts 执行自动 push 脚本

```bash
cd /Users/yanyuming/Downloads/GitHub/PurePage && git add . && git commit -m "$(date)" && git push origin $(git name-rev --name-only HEAD)
```