# [网鼎杯 2020 半决赛]AliceWebsite

#PHP代码审计 #文件包含

打开网页，下载给出的源代码，发现一段 PHP 代码

```php
<?php
$action = (isset($_GET['action']) ? $_GET['action'] : 'home.php');
if (file_exists($action)) {
    include $action;
} else {
    echo "File not found!";
}
?>
```

发现文件包含命令，尝试 /flag，得到flag。