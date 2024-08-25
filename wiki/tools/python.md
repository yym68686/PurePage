# python tricks

## 获取所有环境变量的名字

```python
import os
for key in os.environ.keys():
    print(key)
```

## 获取指定名字的环境变量对应的值

```python
import os
#参数 'path' 可以换成任意存在的环境变量名
#如果不存在，则输出None
dir=os.environ.get('path')
print(dir)
```

## 设置环境变量

注意:当前设置的环境变量只是在本程序中生效，不是永久更新

```python
import os
dir="D:\\LearnTool"
os.environ['datapath']=dir
print(os.environ.get('datapath'))
```

## 控制鼠标和键盘

```python
import pyautogui
n = int(input())
for i in range(0,n):
    pyautogui.moveTo(500,500,.3)
    pyautogui.rightClick()
    pyautogui.moveTo(540,540,.1)
    pyautogui.moveTo(740,560,.1)
    pyautogui.click()
    pyautogui.moveTo(1080,240,.3)
    pyautogui.click()
    pyautogui.moveTo(740,570,.3)
    pyautogui.click()
    pyautogui.hotkey('ctrl','v')
    pyautogui.press('enter')
```

## 格式化输出

[python基础_格式化输出（%用法和format用法）](https://www.cnblogs.com/fat39/p/7159881.html)

## list 矩阵 数组 互换

[Python3 列表，数组，矩阵的相互转换_Chenyu_cook的博客-CSDN博客_python 列表转矩阵](https://blog.csdn.net/weixin_41947092/article/details/80182276)

## http.server 服务器

```bash
python -m http.server 8080
```

## python虚拟环境命令

```bash
virtualenv .
.\\Scripts\\activate
deactivate
```