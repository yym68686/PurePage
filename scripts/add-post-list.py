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

with open("index.md", "r") as f:
    md_content = f.read()
title = "# 文章列表"
index = md_content.find(title)
new_content = ""
for mdpath in md_files_path:
    with open(mdpath, "r") as f:
        post_content = f.read()
    title = gettitle(post_content)
    new_content += f"- [{title}]({mdpath})\n"
md_content = md_content[:index + len(title) - 4] + new_content + md_content[index + len(title) - 4:]
# print(md_content)
with open("index.md", "w") as f:
    f.write(md_content)