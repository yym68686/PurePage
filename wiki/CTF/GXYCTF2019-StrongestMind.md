# [GXYCTF2019]StrongestMind

#爬虫脚本

打开网站显示一个文本框，随便输入一个数字，拦截请求，每次都 post 一个 answer 数据，注意每次响应都是下一次要计算的值，而不是重新 Get 一次，这样的数字是错的。编写代码：

```python
import re
import time
from requests import *
url = "http://6be211d9-59f2-4654-a5c2-a4a8cb95a80c.node4.buuoj.cn:81"
s = session()
r = s.get(url).text
for _ in range(1001):
    time.sleep(0.1)
    expression = re.findall(r"\d+\s\D\s\d+", r)[0]
    data = {"answer": eval(expression)}
    r = s.post(url, data=data).text
    try:
        flag = re.findall("flag{.+}", r)[0]
        print("\r" + flag)
        break
    except:
        if ("bingo" in r):
            print("\r" + str(_), end="")
        else:
            print(req.content.decode('utf-8'))
            break
```

运行后得到 flag。

References

[[GXYCTF2019]StrongestMind_succ3的博客-CSDN博客](https://blog.csdn.net/shinygod/article/details/124141957)

https://blog.csdn.net/qq_46263951/article/details/118914287