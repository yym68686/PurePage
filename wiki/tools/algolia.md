# Algolia 自定义搜索

Algolia 官网：https://www.algolia.com/apps/EF9JOH8KCB/dashboard

官方文档：https://docsearch.algolia.com/docs/legacy/run-your-own/

下载 docker 镜像

```bash
docker pull algolia/docsearch-scraper
```

编写 .env 文件

```
APPLICATION_ID=EF9JOH8KCB
API_KEY=0d3b4b0263eecdd78e79ec766ccd9935
```

编写 config.json

```json
{
  "index_name": "yym68686",
  "start_urls": [
    "https://wiki.yym68686.top"
  ],
  "stop_urls": [],
  "maxDepth": 2,
  "aggregateContent": true,
  "selectors": {
    "lvl0": {
      "selector": "h1",
      "global": true,
      "default_value": "Documentation"
    },
    "lvl1": "h1",
    "lvl2": "h2",
    "lvl3": "h3",
    "lvl4": "h4",
    "lvl5": "h5",
    "text": "p, li, code"
  },
  "js_render": true,
  "js_wait": 4
}
```

参考配置：https://github.com/algolia/docsearch-configs/tree/master/configs

运行 docker 容器

```
docker run -it --env-file=~/Documents/algolia/.env -e "CONFIG=$(cat ~/Documents/algolia/config.json | jq -r tostring)" algolia/docsearch-scraper
```

References

https://juejin.cn/post/7030456110930722847

https://juejin.cn/post/7090866381712801828
