# 获得当前文件夹下所有markdown文件的目录
# 用法：python Deploy.py
import os
import re
from datetime import datetime
os.system("clear")

def generate_sitemap(url_list):
    print("generate sitemap...")
    # 定义网站 URL 和更新日期
    site_url = "https://yym68686.top/"
    lastmod = datetime.now().strftime('%Y-%m-%d')
    url_list = [""] + url_list
    urls = [site_url + item for item in url_list]

    # 生成 sitemap.xml 文件
    with open('sitemap.xml', 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in urls:
            print("=>", url)
            f.write('  <url>\n')
            f.write('    <loc>{}</loc>\n'.format(url))
            f.write('    <lastmod>{}</lastmod>\n'.format(lastmod))
            f.write('    <changefreq>daily</changefreq>\n')
            f.write('  </url>\n')
        f.write('</urlset>\n')

def gettitle(text):
    regex = r"^#\s.*?$"
    matches = re.findall(regex, text, re.MULTILINE)[0]
    return matches[2:]

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
post_path = path + '/post/'
all_files = os.listdir(post_path)
md_files = []
md_files_path = []
md_create_time = []
for subdir in all_files:
    if os.path.isdir(post_path + f"{subdir}"):
        post_dir = os.listdir(post_path + f"{subdir}")
        if "index.md" in post_dir:
            timestamp = os.path.getmtime(post_path + f"{subdir}/index.md")
            dt = datetime.fromtimestamp(timestamp)
            md_create_time += [dt.strftime("%Y-%m-%d")]
            md_files_path += ["./post/" + f"{subdir}/index.md"]
            print("=>", dt.strftime("%Y-%m-%d"), "./post/" + f"{subdir}/index.md")

post_list = list(zip(md_files_path, md_create_time))
post_sorted_list = sorted(post_list, key=lambda x: x[1], reverse=True)

regex = r"##\s文章列表\n(\n*(-\s.*\n)*\n*)##"
with open("index.md", "r") as f:
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
for mdpath, create_time in post_sorted_list:
    with open(mdpath, "r") as f:
        post_content = f.read()
    title = gettitle(post_content)
    new_content += f"- [{title}]({mdpath}) {create_time}\n"
md_content = md_content[:start] + "\n" + new_content + "\n" + md_content[end:]
with open("index.md", "w") as f:
    f.write(md_content)

md_files_path = ["/".join(url[2:].split("/")[:-1]) for url in md_files_path]
print(md_files_path)
generate_sitemap(md_files_path)

os.system(f'cd {path} && git add . && git commit -m "$(date)" && git push origin $(git name-rev --name-only HEAD)')