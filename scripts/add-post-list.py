# 获得当前文件夹下所有markdown文件的目录
# 用法：python getmdtoc.py
import os
import re
import markdown
os.system("clear")

def gettitle(text):
    regex = r"^#\s.*?$"
    matches = re.findall(regex, text, re.MULTILINE)[0]
    return matches[2:]

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
post_path = path + '/post/'
all_files = os.listdir(post_path)
md_files = []
md_files_path = []
for subdir in all_files:
    if os.path.isdir(post_path + f"{subdir}"):
        post_dir = os.listdir(post_path + f"{subdir}")
        if "index.md" in post_dir:
            md_files_path += ["./post/" + f"{subdir}/index.md"]
            print("=>", "./post/" + f"{subdir}/index.md")

# coding=utf8
# 上述标签定义了本文档的编码，与Python 2.x兼容。

import re

regex = r"##\s文章列表([.\n]*(-\s.*\n)*\n*)##"

test_str = ("# yym68686\n\n"
	"## 联系方式\n\n"
	"✈️ [Telegram](https://t.me/yym68686)\n\n"
	"🐦 [Twitter](https://twitter.com/yym68686)\n\n"
	"📖 [GitHub](https://github.com/yym68686)\n\n"
	"📮 Email: yym68686@outlook.com\n\n"
	"## 文章列表\n\n"
	"- [一个极简主义者的博客页面](./post/develop-purepage/index.md)\n"
	"- [Re-ID 综述论文分享](./post/reid-outlook-paper-share/index.md)\n\n"
	"## 关于我\n\n"
	"code is law.")

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    
    print ("在{start}-{end}找到匹配{matchNum}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("在{start}-{end}找到组{groupNum}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.

# with open("index.md", "r") as f:
#     md_content = f.read()
# title = "# 文章列表"
# index = md_content.find(title)
# new_content = ""
# for mdpath in md_files_path:
#     with open(mdpath, "r") as f:
#         post_content = f.read()
#     title = gettitle(post_content)
#     new_content += f"- [{title}]({mdpath})\n"
# md_content = md_content[:index + len(title) - 4] + new_content + "\n" + md_content[index + len(title) - 4:]
# with open("index.md", "w") as f:
#     f.write(md_content)

os.system(f'cd {path} && git add . && git commit -m "$(date)" && git push origin $(git name-rev --name-only HEAD)')