import os

# ... 现有代码 ...
def get_post_md_content(directory, reset_image_path=False):
    # 查找所有的 .md 文件
    file_path = os.path.join(directory, "index.md")
    content = ""
    title = ""
    print(file_path)
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        title = content.split("\n")[0].replace("#", "").strip()
        content = content.replace(title, "", 1)

        # 使用正则表达式替换图片路径
        if reset_image_path:
            def replace_path(match):
                return f'![{match.group(1)}]({os.path.join(directory.split("/")[-1], match.group(1).lstrip("./"))})'

            import re
            pattern = r'!\[.*?\]\((\.?\/assets\/.*?\.png)\)'
            modified_content = re.sub(pattern, replace_path, content)
            content = modified_content
    return content, title

def get_wiki_md_content(directory, reset_image_path=False):
    # 查找所有的 .md 文件
    file_path = directory
    content = ""
    title = ""
    print(file_path)
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        title = content.split("\n")[0].replace("#", "").strip()
        content = content.replace(title, "", 1)

        # 使用正则表达式替换图片路径
        if reset_image_path:
            def replace_path(match):
                return f'![{match.group(1)}]({os.path.join(directory.split("/")[-1], match.group(1).lstrip("./"))})'

            import re
            pattern = r'!\[.*?\]\((\.?\/assets\/.*?\.png)\)'
            modified_content = re.sub(pattern, replace_path, content)
            content = modified_content
    return content, title

def get_all_md_documents():
    documents = []

    # 读取post文件夹下的文档
    post_dir = "post"
    for post_name in os.listdir(post_dir):
        post_path = os.path.join(post_dir, post_name)
        if os.path.isdir(post_path):
            content, title = get_post_md_content(post_path, reset_image_path=True)
            documents.append({"title": title, "content": content, "type": "post", "path": post_name})

    # 读取wiki文件夹下的文档
    wiki_dir = "wiki"
    for root, dirs, files in os.walk(wiki_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                content, title = get_wiki_md_content(file_path, reset_image_path=False)
                relative_path = os.path.relpath(file_path, wiki_dir)
                documents.append({"title": title, "content": content, "type": "wiki", "path": relative_path})

    return documents

# ... 现有代码 ...

# 在需要使用所有文档的地方调用这个函数
all_documents = get_all_md_documents()

print(all_documents)