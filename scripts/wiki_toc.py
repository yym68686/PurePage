# 获得当前文件夹下所有markdown文件的目录
# 用法：python Deploy.py
import os
import re
from datetime import datetime
os.system("clear")

def gettitle(text):
    regex = r"^#\s.*?$"
    matches = re.findall(regex, text, re.MULTILINE)[0]
    return matches[2:]

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
post_path = path + '/wiki/'
all_files = os.listdir(post_path)
print(all_files)
# exit(0)

import os
import json
from datetime import datetime

def get_markdown_files(root_dir):
    markdown_files = {}

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                timestamp = os.path.getmtime(file_path)
                dt = datetime.fromtimestamp(timestamp)
                create_time = dt.strftime("%Y-%m-%d")
                # creation_time = os.path.getctime(file_path)
                # create_time = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
                relative_path = os.path.relpath(file_path, path)
                markdown_files[relative_path] = create_time

    return markdown_files

# 指定要搜索的根目录
root_directory = post_path  # 请替换为您的实际目录路径

# 获取所有Markdown文件及其创建时间
md_files = get_markdown_files(root_directory)
print(json.dumps(md_files, indent=4, ensure_ascii=False))
# exit(0)
# post_sorted_list = sorted(post_list, key=lambda x: x[1], reverse=True)

regex = r"##\s文章列表\n(\n*(-\s.*\n)*\n*)##"
md_content = ""
with open(os.path.join(post_path, "index.md"), "r") as f:
    md_content = f.read()
matches = re.finditer(regex, md_content, re.MULTILINE)
start = 0
end = 0
for matchNum, match in enumerate(matches, start=1):
    start = match.start(1)
    end = match.end(1)
    print ("在{start}-{end}找到组{groupNum}: {group}".format(groupNum = 1, start = match.start(1), end = match.end(1), group = match.group(1)))
    break

new_content = ""
for mdpath, create_time in md_files.items():
    with open(os.path.join(path, mdpath), "r") as f:
        post_content = f.read()
    title = gettitle(post_content)
    new_content += f"- [{title}]({mdpath})\n"
md_content = md_content[:start] + "\n" + new_content + "\n" + md_content[end:]
with open(os.path.join(post_path, "index.md"), "w") as f:
    f.write(md_content)