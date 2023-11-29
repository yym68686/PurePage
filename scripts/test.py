import os
import time

# 设置文件名，请自行修改
file_path = '/Users/yanyuming/Downloads/GitHub/PurePage/post/HSTL/index.md'

# 获取文件的创建时间
timestamp = os.stat(file_path)
# timestamp = os.path.getctime(file_path)
# time_readable = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
for i in timestamp:
    if(len(str(i))==10):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)))
print('创建时间：', timestamp)
# print('创建时间：' + time_readable)