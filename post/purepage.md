# 一个极简主义者的博客页面

以前试过很多不同的博客系统，比如 Hexo，[Docusaurus 2](https://docusaurus.io/)，notion。我总是觉得太复杂，我希望有一个个人网站能同时满足高可定制，数据自主性，原生无依赖，没有冗余功能。一开始想的是用 Github page 做一个博客页面，但是 github 自有的 [GitHub Flavored Markdown](https://github.github.com/gfm/) 奇怪语法有限制。因此必须促使我从头开始设计一个博客页面，之所以它不叫博客系统，因为它足够简单，使用原生 HTML、JS 和 CSS 实现，但同时基本功能又足够用，包括支持 Latex 数学公式渲染，Mermaid 图表渲染，代码高亮，自适应界面。未来将加入搜索功能。

项目地址：https://github.com/yym68686/PurePage，目前已经 public，欢迎大家使用。项目的名字叫 PurePage，这个项目极为简单，可以说是一个玩具项目，但我是一个实用主义与极简主义者，我希望可以用最少的步骤解决简单的问题。

## TODO list

[x] 自动在首页生成文章列表
[x] 文章列表自动删除原来的列表，重新构建一个
[x] README 多语言支持
[x] 字体设置
[ ] 内建搜索功能
[ ] 每篇文章的目录生成
[ ] 生成 sitemap.xml 文件，优化 SEO