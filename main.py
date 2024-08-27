import os
from fasthtml.common import *
from urllib.parse import unquote

from typing import List, Dict, Optional
import pypinyin

Matrix = List[List[int]]
SourceMappingData = Dict[str, any]

def extract_boundary_mapping_with_preset_pinyin(original_string: str) -> SourceMappingData:
    pinyin_list = pypinyin.lazy_pinyin(original_string, style=pypinyin.NORMAL)
    pinyin_string = ''
    boundary = []
    original_indices = []

    current_index = 0
    for i, (char, pinyin) in enumerate(zip(original_string, pinyin_list)):
        if char.isascii():
            pinyin_string += char.lower()
            boundary.append([current_index, current_index])
            original_indices.append(i)
            current_index += 1
        else:
            pinyin_string += pinyin
            boundary.append([current_index, current_index + len(pinyin) - 1])
            original_indices.extend([i] * len(pinyin))
            current_index += len(pinyin)

    return {
        'originalString': original_string,
        'pinyinString': pinyin_string,
        'boundary': boundary,
        'originalLength': len(original_string),
        'originalIndices': original_indices
    }

def search_by_boundary_mapping(data: SourceMappingData, target: str, start_index: int, end_index: int) -> Optional[Matrix]:
    original_string = data['originalString'][start_index:end_index+1]
    pinyin_string = data['pinyinString']
    boundary = data['boundary']
    original_indices = data['originalIndices']

    target = target.lower().replace(' ', '')
    target_pinyin = ''.join(pypinyin.lazy_pinyin(target, style=pypinyin.NORMAL))

    pinyin_length = len(pinyin_string)
    target_length = len(target_pinyin)

    if not data or not target or pinyin_length < target_length or not len(original_string):
        return None

    # 检查索引是否在有效范围内
    if start_index < 0 or end_index >= len(boundary) or start_index > end_index:
        return None

    start_boundary = boundary[start_index][0]
    end_boundary = boundary[min(end_index, len(boundary) - 1)][1]

    match_positions = [-1] * target_length
    match_index = 0
    for i in range(pinyin_length):
        if match_index < target_length and pinyin_string[i] == target_pinyin[match_index]:
            match_positions[match_index] = i
            match_index += 1

    if match_index < target_length:
        return None

    dp_table = [[[0, 0, -1, -1] for _ in range(target_length + 1)] for _ in range(pinyin_length + 1)]
    dp_scores = [0] * (pinyin_length + 1)
    dp_match_path = [[None for _ in range(target_length)] for _ in range(pinyin_length + 1)]

    for match_index in range(target_length):
        matched_pinyin_index = match_positions[match_index] + 1

        current_dp_table_item = dp_table[matched_pinyin_index - 1][match_index]
        current_score = dp_scores[matched_pinyin_index - 1]
        dp_scores[matched_pinyin_index - 1] = 0
        dp_table[matched_pinyin_index - 1][match_index] = [0, 0, -1, -1]

        for matched_pinyin_index in range(matched_pinyin_index, pinyin_length + 1):
            prev_score = current_score
            prev_matched_characters, prev_matched_letters, prev_boundary_start, prev_boundary_end = current_dp_table_item

            current_dp_table_item = dp_table[matched_pinyin_index][match_index]
            current_score = dp_scores[matched_pinyin_index]

            is_new_word = (matched_pinyin_index - 1 < len(boundary) and
                           matched_pinyin_index - 1 == boundary[matched_pinyin_index - 1][1] - end_boundary and
                           prev_boundary_start != boundary[matched_pinyin_index - 1][0] - start_boundary)

            is_continuation = (prev_matched_characters > 0 and
                               matched_pinyin_index - 1 < len(boundary) and
                               prev_boundary_end == boundary[matched_pinyin_index - 1][1] - end_boundary and
                               matched_pinyin_index > 1 and
                               pinyin_string[matched_pinyin_index - 2] == target_pinyin[match_index - 1])

            is_equal = matched_pinyin_index <= pinyin_length and pinyin_string[matched_pinyin_index - 1] == target_pinyin[match_index]

            if is_equal and (is_new_word or is_continuation) and (match_index == 0 or prev_score > 0):
                prev_score += prev_matched_letters * 2 + 1
                matched_letters_count = prev_matched_letters + 1

                if prev_score >= dp_scores[matched_pinyin_index - 1]:
                    dp_scores[matched_pinyin_index] = prev_score
                    dp_table[matched_pinyin_index][match_index] = [
                        prev_matched_characters + int(is_new_word),
                        matched_letters_count,
                        boundary[min(matched_pinyin_index - 1, len(boundary) - 1)][0] - start_boundary,
                        boundary[min(matched_pinyin_index - 1, len(boundary) - 1)][1] - end_boundary
                    ]

                    original_string_index = boundary[min(matched_pinyin_index - 1, len(boundary) - 1)][0] - start_boundary
                    new_matched = prev_score > dp_scores[matched_pinyin_index - 1]
                    dp_match_path[matched_pinyin_index][match_index] = (
                        [original_string_index - prev_matched_characters + int(not is_new_word),
                         original_string_index, matched_letters_count]
                        if new_matched else dp_match_path[matched_pinyin_index - 1][match_index]
                    )
                    continue

            dp_scores[matched_pinyin_index] = dp_scores[matched_pinyin_index - 1]
            dp_match_path[matched_pinyin_index][match_index] = dp_match_path[matched_pinyin_index - 1][match_index]

            if matched_pinyin_index - 1 < len(boundary):
                gap = boundary[matched_pinyin_index - 1][0] - start_boundary - dp_table[matched_pinyin_index - 1][match_index][2]
                is_same_word = lambda: (matched_pinyin_index < len(boundary) and
                                        boundary[matched_pinyin_index - 1][0] == boundary[min(matched_pinyin_index, len(boundary) - 1)][0])
                is_within_range = matched_pinyin_index < pinyin_length

                dp_table[matched_pinyin_index][match_index] = (
                    dp_table[matched_pinyin_index - 1][match_index]
                    if gap == 0 or (is_within_range and gap == 1 and is_same_word())
                    else [0, 0, -1, -1]
                )

    if dp_match_path[pinyin_length][target_length - 1] is None:
        return None

    hit_indices = []
    g_index = pinyin_length
    rest_matched = target_length - 1

    while rest_matched >= 0:
        if dp_match_path[g_index][rest_matched] is None:
            return None
        start, end, matched_letters = dp_match_path[g_index][rest_matched]
        hit_indices.insert(0, [start + start_index, end + start_index])
        g_index = original_indices[min(start + start_index, len(original_indices) - 1)] - original_indices[start_index] - 1
        rest_matched -= matched_letters

    return hit_indices

def search_with_indexof(source: str, target: str) -> Optional[Matrix]:
    start_index = source.lower().find(target.lower())
    return [[start_index, start_index + len(target) - 1]] if start_index != -1 else None

def search_sentence_by_boundary_mapping(boundary_mapping: SourceMappingData, sentence: str) -> Optional[Matrix]:
    if not sentence:
        return None

    hit_ranges_by_index_of = search_with_indexof(boundary_mapping['originalString'], sentence)
    if hit_ranges_by_index_of:
        return hit_ranges_by_index_of

    return search_by_boundary_mapping(boundary_mapping, sentence, 0, len(boundary_mapping['originalString']) - 1)

def search_entry(source: str, target: str) -> Optional[Matrix]:
    boundary_mapping = extract_boundary_mapping_with_preset_pinyin(source)
    return search_sentence_by_boundary_mapping(boundary_mapping, target)

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

def navbar():
    return Div(
        Div(
            A("yym68686", href="/", cls="tw-text-xl tw-font-bold tw-text-white tw-hover:text-gray-200"),
            Div(
                Input(
                    type="text",
                    placeholder="搜索...",
                    cls="tw-bg-gray-700 tw-bg-opacity-50 tw-text-white tw-placeholder-gray-400 tw-rounded-full tw-px-3 tw-w-64 tw-focus:outline-none tw-focus:ring-2 tw-focus:ring-blue-400 tw-transition-all tw-duration-300 tw-ease-in-out tw-text-sm",
                    style="height: 28px; line-height: 28px; padding-top: 0; padding-bottom: 0;",
                    hx_get="/search",
                    hx_trigger="keyup changed delay:500ms",
                    hx_target="#search-results",
                    name="query"
                ),
                Div(
                    id="search-results",
                    cls="tw-absolute tw-mt-1 tw-w-64 tw-bg-white tw-bg-opacity-90 tw-backdrop-filter tw-backdrop-blur-lg tw-rounded-lg tw-shadow-lg tw-overflow-hidden tw-transition-all tw-duration-300 tw-ease-in-out tw-max-h-0 group-focus-within:tw-max-h-40",
                    style="top: 30px;"
                ),
                cls="tw-relative tw-group",
                style="height: 30px;"
            ),
            Div(
                A("Home", href="/", cls="tw-text-white tw-hover:text-gray-200"),
                A("Wiki", href="/wiki", cls="tw-text-white tw-hover:text-gray-200"),
                cls="tw-space-x-4"
            ),
            cls="tw-container tw-mx-auto tw-px-4 tw-py-2 tw-flex tw-justify-between tw-items-center"
        ),
        cls="tw-bg-gray-800 tw-bg-opacity-10 tw-backdrop-filter tw-backdrop-blur-lg tw-shadow-lg tw-fixed tw-top-0 tw-left-0 tw-right-0 tw-z-50"
    )

hdrs = [
    KatexMarkdownJS(),
    HighlightJS(langs=['python', 'javascript', 'html', 'css']),
    Link(href="/static/tailwind.css", rel="stylesheet"),
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
    '''),
]
app, rt = fast_app(hdrs=hdrs)

# 假设 search_entry 函数已经定义
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
all_documents = get_all_md_documents()

@rt("/search")
def get(query: str):
    if not query:
        return ""

    data_source = [item["content"] for item in all_documents]

    results = []
    for index, item in enumerate(data_source):
        match = search_entry(item, query)
        print("match", all_documents[index]["title"], match)
        if match:
            results.append([index, item, match])

    return search_results_template(results, query)

def search_results_template(results: List[tuple], query: str):
    if not results:
        return Div("没有找到相关结果", cls="tw-p-4 tw-text-gray-200 tw-text-center tw-italic")

    result_items = []
    for (index, item, match) in results:
        document = all_documents[index]
        result_items.append(
            Div(
                A(
                    highlight_text(item, match),
                    href=f"/{document['type']}/{document['path']}?highlight={query}",
                    cls="tw-block tw-w-full tw-h-full"
                ),
                cls="tw-p-3 tw-border-b tw-border-gray-600 tw-border-opacity-20 hover:tw-bg-white hover:tw-bg-opacity-10 tw-transition-colors tw-duration-200 tw-ease-in-out tw-rounded-lg tw-mb-2"
            )
        )

    return Div(
        Div(
            Div(
                *result_items,
                cls="tw-rounded-lg tw-overflow-hidden tw-divide-y tw-divide-gray-600 tw-divide-opacity-20"
            ),
            cls="tw-p-4 tw-bg-gray-800 tw-bg-opacity-10 tw-backdrop-filter tw-backdrop-blur-lg tw-rounded-xl tw-max-h-80 tw-overflow-y-auto tw-scrollbar-thin tw-scrollbar-thumb-gray-400 tw-scrollbar-track-transparent tw-shadow-lg"
        ),
        id="search-results",
        hx_swap_oob="outerHTML",
    )

def highlight_text(text: str, matches: List[List[int]]):
    highlighted = []
    last_end = 0
    for start, end in matches:
        if start > last_end:
            highlighted.append(text[start-30:start])
        highlighted.append(Span(text[start:end+1], cls="tw-bg-yellow-300 tw-bg-opacity-50 tw-rounded-md tw-px-1 highlight"))
        last_end = end + 1
    if last_end < len(text):
        highlighted.append(text[last_end:last_end+30])
    return Div(*highlighted, cls="tw-text-white tw-text-opacity-90 tw-leading-relaxed")

def get_post_md_content(directory, reset_image_path=False):
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
    content, title = get_post_md_content(f"post/{post_name}", reset_image_path=True)
    headings = extract_headings(content)
    content_with_ids = add_heading_ids(content)

    layout = Div(
        navbar(),  # 添加导航栏
        Div(
            sidebar(headings),
            Div(Div(content_with_ids, cls="marked"), cls="main-content"),
        )
    )

    return Div(Titled(title, layout), cls="tw-mt-16")

def get_wiki_md_content(directory, reset_image_path=False):
    # 查找所有的 .md 文件
    file_path = directory
    file_path = os.path.join(os.getcwd(), file_path)
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

@app.get("/wiki/index.md")
def get():
    return RedirectResponse(url="/wiki")

@app.get('/wiki/{post_name:path}')
def get(post_name: str):
    decoded_post_name = unquote(post_name)
    content, title = get_wiki_md_content(f"wiki/{decoded_post_name}", reset_image_path=False)
    headings = extract_headings(content)

    layout = Div(
        navbar(),  # 添加导航栏
        Div(
            sidebar(headings),
            Div(Div(content, cls="marked"), cls="main-content"),
        )
    )

    return Div(Titled(title, layout), cls="tw-mt-16")

@app.get('/wiki')
def get():
    content, title = get_post_md_content("wiki")
    return Div(Titled(title, Div(navbar(), Div(content, cls="marked"))), cls="tw-mt-16")

@rt('/')
def get():
    content, title = get_post_md_content(".")
    return Div(Titled(title, Div(navbar(), Div(content, cls="marked"))), cls="tw-mt-16")  # 添加导航栏

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )