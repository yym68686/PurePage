# [开源] Architext: 定义上下文工程新范式——像架构师一样思考你的 Prompt

项目地址，欢迎 star 或者提出改进意见：

https://github.com/yym68686/architext

**Architext** (源自 "Architecture" + "Text") 是一个为大语言模型（LLM）应用设计的、专注于**上下文工程 (Context Engineering)** 的 Python 库。它提供了一套优雅、强大且面向对象的工具，让您能够像软件工程师设计架构一样，精确、动态地构建和重组 LLM 的输入上下文。

告别散乱的字符串拼接和复杂的构建逻辑，进入一个将上下文视为**可操作、可组合、可演进的工程化实体**的新时代。

## 🤔 什么是上下文工程 (Context Engineering)？

在构建复杂的 AI Agent 时，提供给 LLM 的上下文（即 `messages` 列表）的**质量和结构**直接决定了其性能的上限。上下文工程是一门新兴的学科，它关注于：

*   **结构化（Structuring）**: 如何将来自不同数据源（文件、代码、数据库、API）的信息，组织成 LLM 最易于理解的结构？
*   **动态化（Dynamism）**: 如何根据对话的进展，实时地添加、移除或重排上下文内容，以保持其相关性和时效性？
*   **优化（Optimization）**: 如何在有限的上下文窗口内，智能地筛选和呈现最高价值的信息，以最大化性能并最小化成本？

`Architext` 正是为解决这些工程化挑战而生。

随着 Agent 上下文越来越庞大，管理上下文变得越来越困难。下面我们通过几个场景来说明 Architext 如何解决这些痛点。

## 场景1

有时候agent在windows电脑上运行后，跑到 mac 上面跑，但是系统里面里面已经初始化好了一开始是在Windows上跑的，此时想要修改系统提示很麻烦，开发者需要自己去历史记录里面的字符串手动修改。但是 Architext 可以简化这一切：

```python
import json
import time
import asyncio
import platform
from datetime import datetime
from architext import Messages, SystemMessage, Texts

async def example_1():
    messages = Messages(
        SystemMessage(f"You are a helpful assistant that can help with code. OS: {Texts(lambda: platform.platform())}, Time: {Texts(lambda: datetime.now().isoformat())}")
    )

    new_messages = await messages.render_latest()
    print(json.dumps(new_messages, indent=4, ensure_ascii=False))

    time.sleep(1)

    # 假设换了系统继续跑
    new_messages = await messages.render_latest()
    print(json.dumps(new_messages, indent=4, ensure_ascii=False))

asyncio.run(example_1())

# 运行结果
# [
#     {
#         "role": "system",
#         "content": "You are a helpful assistant that can help with code. OS: macOS-15.6.1-arm64-arm-64bit, Time: 2025-09-01T21:18:51.572491"
#     }
# ]
# [
#     {
#         "role": "system",
#         "content": "You are a helpful assistant that can help with code. OS: win-10-10.0.22621-amd64-x86_64, Time: 2025-09-01T21:18:52.573421"
#     }
# ]
```

看到了吗？无需任何手动干预，`platform.platform()` 和 `datetime.now()` 就像被赋予了生命，在每次渲染时都动态地提供最新信息。这正是 Architext F-String 的魔力所在：**它将静态的、命令式的字符串拼接，彻底革命为动态的、声明式的上下文构建。** 你不再需要编写繁琐的更新逻辑，只需在字符串中声明“这里需要什么信息”，Architext 就会在运行时为你精准地注入最新状态。这是一个真正的“杀手级”功能，它将开发者从繁重的上下文管理中解放出来，回归到业务逻辑本身。

## 场景2

如果agent读了很多文件，你不得不维护一个列表来记录读了哪些文件，然后为了节省上下文，你不得不放在系统提示里面，而每次请求API都需要将最新的文件内容拼接到系统提示里面。Architext 解决了这个痛点：

```python
import json
import asyncio
from architext import Messages, UserMessage, Files, SystemMessage

async def example_2():
    messages = Messages(
        SystemMessage("You are a helpful assistant that can help with code.", Files()),
        UserMessage("hi")
    )

    # 此时读取了某个文件
    messages.provider("files").update("main.py")
    new_messages = await messages.render_latest()
    print(json.dumps(new_messages, indent=4, ensure_ascii=False))

asyncio.run(example_2())

# 运行结果
# [
#     {
#         "role": "system",
#         "content": "You are a helpful assistant that can help with code.<latest_file_content><file><file_path>main.py</file_path><file_content>print('hello')</file_content></file>\n</latest_file_content>"
#     },
#     {
#         "role": "user",
#         "content": "hi"
#     }
# ]
```

Architext 另外一个很强大的功能就是，人会在agent运行期间修改文件内容，大多数 agent 并不知道，这会导致无法及时获得最新的文件内容，但是 messages.render_latest() 确保每次都能获得最新的文件内容。

## 场景3

有时我想将系统提示里面的文件内容放在第一个 user 消息里面，传统方法先从系统提示里面通过正则匹配文件所在的块，然后删除，转移到第一个user消息，此时开发者的心智负担很重，需要操作各种列表，content 字段有时还有列表或者字符串等情况，甚至content里面还有图片，要考虑的情况非常多，开发者无法专注于业务逻辑的开发，被各种边缘情况无限内耗。但是 Architext 实现这个需求将非常简单，只需要两行代码，并且能自动处理有图片内容的情况：

```python
import json
import asyncio
from architext import Messages, UserMessage, Files, SystemMessage, Images

async def example_3():
    messages = Messages(
        SystemMessage("You are a helpful assistant that can help with code.", Files()),
        UserMessage("hi", Images("image.png"))
    )

    # 此时读取了某个文件
    messages.provider("files").update("main.py")

    new_messages = await messages.render_latest()
    print(json.dumps(new_messages, indent=4, ensure_ascii=False))

    # 转移整个文件块到user message中
    files = messages.pop("files")
    messages[1].append(files)

    new_messages = await messages.render_latest()
    print(json.dumps(new_messages, indent=4, ensure_ascii=False))

asyncio.run(example_3())

# 运行结果
# [
#     {
#         "role": "system",
#         "content": "You are a helpful assistant that can help with code.<latest_file_content><file><file_path>main.py</file_path><file_content>print('hello')</file_content></file>\n</latest_file_content>"
#     },
#     {
#         "role": "user",
#         "content": [
#             {
#                 "type": "text",
#                 "text": "hi"
#             },
#             {
#                 "type": "image_url",
#                 "image_url": {
#                     "url": "data:image/png;base64,VGhpcyBpcyBhIGR1bW15IGltYWdlIGZpbGUu"
#                 }
#             }
#         ]
#     }
# ]
# [
#     {
#         "role": "system",
#         "content": "You are a helpful assistant that can help with code."
#     },
#     {
#         "role": "user",
#         "content": [
#             {
#                 "type": "text",
#                 "text": "hi"
#             },
#             {
#                 "type": "image_url",
#                 "image_url": {
#                     "url": "data:image/png;base64,VGhpcyBpcyBhIGR1bW15IGltYWdlIGZpbGUu"
#                 }
#             },
#             {
#                 "type": "text",
#                 "text": "<latest_file_content><file><file_path>main.py</file_path><file_content>print('hello')</file_content></file>\n</latest_file_content>"
#             }
#         ]
#     }
# ]
```

当然如果你想添加到第一个消息前面只需要 `messages[1] = files + messages[1]`可以说非常直观。你可能注意到 files = messages.pop("files") 开发者并不需要知道files文本块在哪里，这是 Architext 最强大的地方，就是无论该名字的块在 messages 数组的任何地方都能直接pop出来。

## 场景4

前段时间 gemini 免费 key 总是截断，很多人想了很多办法防截断，对于agent应用来说，截断是致命的，因为很可能一个tool use还没闭合就结束了，导致 llm 觉得自己已经调用过工具的幻觉。我本人利用 Architext 完美解决了截断问题，在我的解决方案里面，一个很重要的需求就是我只需要最后一个消息显示防截断提示词：`Your message **must** end with [done] to signify the end of your output.` 示例代码：

```python
import json
import asyncio
from architext import Messages, SystemMessage, Texts, UserMessage, AssistantMessage

async def example_4():
    messages = Messages(
        SystemMessage(f"You are a helpful assistant that can help with code."),
        UserMessage("hi", Texts("\n\nYour message **must** end with [done] to signify the end of your output.", name="done")),
        AssistantMessage("hello"),
        UserMessage("hi again", Texts("\n\nYour message **must** end with [done] to signify the end of your output.", name="done")),
    )

    messages.provider("done").visible = False
    messages.provider("done")[-1].visible = True

    new_messages = await messages.render_latest()
    print(json.dumps(new_messages, indent=4, ensure_ascii=False))

asyncio.run(example_4())

# 运行结果
# [
#     {
#         "role": "system",
#         "content": "You are a helpful assistant that can help with code."
#     },
#     {
#         "role": "user",
#         "content": "hi"
#     },
#     {
#         "role": "assistant",
#         "content": "hello"
#     },
#     {
#         "role": "user",
#         "content": "hi again\n\nYour message **must** end with [done] to signify the end of your output."
#     }
# ]
```

只需要对所有的相同字符串取一样的名字，然后只需要一行就能隐藏所有名字一样的字符串，并通过所有指定只有最后一行才显示防截断字符串。

## 远不止于此

通过以上场景，我们仅仅揭开了 `Architext` 能力的冰山一角。它代表了一种全新的、将上下文视为**可操作、可组合、可演进的工程化实体**的思维方式。

除了上述功能，`Architext` 还提供了更多强大的特性等待你去探索：

*   **智能消息合并**：当你 `append` 一个与上一条消息角色相同的消息时，`Architext` 会自动将它们合并。这彻底解决了许多 API 不允许连续发送相同角色消息的格式规范问题。
*   **完整的工具使用支持**：通过 `ToolCalls` 和 `ToolResults`，优雅地处理现代 Agent 的工具调用与结果返回流程。
*   **会话持久化**：使用 `messages.save()` 和 `Messages.load()`，轻松实现 Agent 状态的保存和恢复，构建健壮、可中断的长时间任务。
*   **Pythonic 的接口**：享受自然的编码体验，比如用 `+` 拼接消息，用切片 (`messages[1:3]`) 操作消息列表。
*   **智能缓存**：内置的缓存机制只在数据源变化时才刷新内容，兼顾了性能与数据的实时性。

我们相信，通过将软件工程的架构思维引入到 Prompt 构建中，可以极大地解放生产力，让开发者专注于真正重要的业务逻辑。

**立即开始你的上下文工程之旅吧！**

我们诚挚地邀请你访问我们的 [GitHub 仓库](https://github.com/yym68686/architext)，深入了解 `Architext`，给我们一个 Star，或者提出宝贵的改进意见。让我们共同构建更智能、更可靠的 AI Agent！