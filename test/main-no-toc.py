import os
from fasthtml.common import *

hdrs = (
    KatexMarkdownJS(), HighlightJS(langs=['python', 'javascript', 'html', 'css']),
)
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

@app.get("/post/{post_name}")
def get(post_name:str):
    content, title = get_md_content(f"post/{post_name}", reset_image_path=True)
    return Titled(title, Div(content, cls="marked"))

@rt('/')
def get(req):
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