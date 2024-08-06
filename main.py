import os
from fasthtml.common import *

def slugify(text):
    # 将文本转换为小写，并替换非字母数字字符为连字符
    return re.sub(r'[^\w]+', '-', text.lower()).strip('-')

def sidebar(headings):
    def sidebar_item(level, text, slug):
        return Div(A(text, href=f"#{slug}"), cls=f"sidebar-item level-{level}")

    return Div(*(sidebar_item(level, text, slug) for level, text, slug in headings), cls="sidebar")

import re
def extract_headings(content):
    headings = []
    in_code_block = False
    for line in content.split('\n'):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
        if not in_code_block and line.startswith('#'):
            level = len(line.split()[0])
            text = line.strip('#').strip()
            slug = slugify(text)
            headings.append((level, text, slug))
    return headings

def add_heading_ids(content):
    lines = content.split('\n')
    in_code_block = False
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
        if not in_code_block and line.startswith('#'):
            level = len(line.split()[0])
            text = line.strip('#').strip()
            slug = slugify(text)
            lines[i] = f'<h{level} id="{slug}">{text}</h{level}>'
    return '\n'.join(lines)


hdrs = [
    KatexMarkdownJS(),
    HighlightJS(langs=['python', 'javascript', 'html', 'css']),
    Style('''
        .layout { display: flex; }
        .sidebar {
            # width: 250px;
            padding: 20px;
        }
        .main-content {
            flex: 1;
            padding: 20px;
        }
        .sidebar-item { margin-bottom: 10px; }
        .level-1 { font-weight: bold; }
        .level-2 { margin-left: 10px; }
        .level-3 { margin-left: 20px; }
    ''')
]
app, rt = fast_app(hdrs=hdrs)

def get_md_content(directory, reset_image_path=False):
    # 查找所有的 .md 文件
    file_path = os.path.join(directory, "index.md")
    content = ""
    title = ""
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

@app.get("/post/{post_name}/index.md")
def get(post_name:str):
    return RedirectResponse(url=f"/post/{post_name}")

@app.get('/post/{post_name}')
def get(post_name: str):
    content, title = get_md_content(f"post/{post_name}", reset_image_path=True)
    headings = extract_headings(content)
    content_with_ids = add_heading_ids(content)

    layout = Div(
        sidebar(headings),
        Div(Div(content_with_ids, cls="marked"), cls="main-content"),
        # cls="layout"
    )

    return Titled(title, layout)

@rt('/')
def get():
    content, title = get_md_content(".")
    return Titled(title, Div(content, cls="marked"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=5001,
        reload=True,
    )