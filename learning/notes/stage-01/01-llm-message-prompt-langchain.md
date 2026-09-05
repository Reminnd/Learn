# LLM、Message、Prompt、Runnable 与 LangChain 心智模型 — 课程笔记

## Metadata

- stage_id: `stage-01`
- chapter_id: `01`
- schema_version: `2`
- lifecycle_status: consolidated
- learning_status: mastered
- schema_migration_evidence_id: `schema-v2-note-metadata`
- last_updated: 2026-08-21

## 1. 本章目标

- 理解 LLM 应用最基本的数据流。
- 区分字符串与 Message。
- 后续掌握 Prompt、Chat Model 与 Runnable 的映射。

## 2. 核心概念

### 2.1 LLM 最小数据流

最小聊天调用可抽象为：`消息列表 → Chat Model → AI Message`。

模型不负责长期记忆。多轮对话之所以连贯，是应用在下一次调用时重新提交必要的历史消息。

### 2.2 Message 不只是字符串

Message（消息）至少表达：

- `role`：角色，例如 system、user、assistant。
- `content`：内容。
- `metadata`：元数据，例如 token usage、finish reason、tool calls、trace id。

纯字符串只保存文字，容易丢失角色边界、工具调用和可观测信息。

严格来说，字符串可以承载序列化后的数据，但若把工具过程直接拼成普通对话文本，就会丢失或模糊类型、角色、tool call id（工具调用编号）和请求—响应关联，难以可靠校验、恢复和追踪。

### 2.3 Prompt 与 Runnable

Prompt（提示模板）负责把业务输入转换成模型需要的消息。它解决“发给模型什么”的问题。

Prompt 的模板是在构造 `ChatPromptTemplate` 时保存的配置；调用 `prompt.invoke(...)` 时传入的是变量映射，而不是再次传入模板本身。其精确输出通常是 `ChatPromptValue`（聊天提示值），内部包含格式化后的消息序列。

Runnable（可运行组件）是一种统一调用协议：组件接收输入、产生输出，并可按顺序组合。它解决“组件如何被调用和连接”的问题。

二者不是同一层：Prompt 可以是一个 Runnable，但 Runnable 也可以是模型、解析器、检索器或自定义函数。

## 3. Harness 中的位置

Harness（智能体运行支架）负责在用户、模型和工具之间组织消息、保留必要元数据，并控制上下文增长。

## 4. 最小原理实现

```python
messages = [
    {"role": "system", "content": "你是一个 Python 助教"},
    {"role": "user", "content": "解释列表推导式"},
]

response = model.invoke(messages)
messages.append(response)
```

关键点：下一轮调用需要由应用决定把哪些历史消息再次传给模型。

Prompt 的最小原理只是一个确定的转换函数：

```python
def build_messages(topic: str) -> list[dict]:
    return [
        {"role": "system", "content": "你是 Python 助教"},
        {"role": "user", "content": f"请解释：{topic}"},
    ]

messages = build_messages("列表推导式")
response = model.invoke(messages)
```

顺序执行 `build_messages → model.invoke` 就是最小的组件组合。Runnable 将这种“输入 → 输出”接口标准化。

## 5. LangChain / LangGraph 框架实现

LangChain 用 `SystemMessage`、`HumanMessage`、`AIMessage` 表达不同角色的消息；`ChatModel.invoke(messages)` 对应一次模型调用。LangGraph 后续会把消息作为 State（状态）的一部分在节点之间传递。

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是 Python 助教"),
    ("human", "请解释：{topic}"),
])

chain = prompt | model
response = chain.invoke({"topic": "列表推导式"})
```

这里 `|` 表示组合：前一个 Runnable 的输出成为后一个 Runnable 的输入。

## 6. 手写版 vs 框架版

- 手写字典：直观、依赖少，但需自行统一角色、响应字段和不同模型供应商差异。
- Message 对象：多一层抽象，但更容易保留工具调用、token 用量和其他元数据。
- 手写函数组合：简单透明，但随着步骤增多，需要自行统一调用、错误处理和追踪。
- Runnable 组合：接口统一、便于替换和观测，但必须理解各组件的输入输出类型，不能把 `|` 当作魔法。

## 7. 工程问题与解决方案

问题：历史消息不断增长，会推高延迟、费用，并可能超过 Context Window（上下文窗口）。

策略：先保留结构化 Message；后续再按预算做截断、摘要或压缩。过早把消息拼成字符串会破坏角色和元数据，使治理更困难。

## 10. 关键英文术语

- LLM（Large Language Model）：大语言模型。
- Message：消息。
- role：角色。
- metadata：元数据，即描述数据的数据。
- token usage：Token 使用量。
- Context Window：上下文窗口，单次调用可处理的信息范围。
- Harness：智能体运行支架，组织模型、工具、状态和策略的运行层。
- Prompt：提示模板，把业务变量转换成模型消息。
- Runnable：可运行组件，遵循统一的输入输出调用协议。
- chain：链，由多个可运行组件依次组合形成的处理流程。

## 12. Q&A 掌握记录

- Q1 已通过：能指出工具/MCP 过程与 token 等模型调用元数据需要结构化保存。
- 精确补充：问题不在于字符串物理上不能存数据，而在于普通文本会破坏结构语义和关联关系。
- Q2 待回答：Prompt 与 Runnable 分别解决什么问题？
- Q2 首答部分正确：识别出 Prompt → Message → Model → AIMessage 的总体方向；需修正为“模板在构造阶段保存，运行时只传变量映射”，并把 Prompt 输出精确表达为包含消息序列的 `ChatPromptValue`。
- Q2b 待复检：区分构造阶段数据与运行时数据。

## 13. 易错点 / 薄弱点

- 容易把 Prompt 的模板配置误认为 `invoke` 时的运行时输入。
- 容易把 `ChatPromptValue` 简化成单个 Message。

## 15. 下一步

评阅 Q2b；通过后进入框架组合与工程问题。

<!-- learn-agent:evidence:stage-01-ch01-Q2b-attempt-2:start -->
### Q2b 复检与工程推进

Q2b 通过：运行时变量映射 → Prompt → ChatPromptValue（包含格式化消息序列）→ Chat Model → AIMessage。已能区分 Prompt 构造阶段的模板配置与 invoke 运行阶段的数据。

不同模型供应商的请求字段和原始响应结构可能不同。LangChain ChatModel 提供统一 invoke 接口与 AIMessage 表达；Harness 仍需保留 response_metadata、usage_metadata、tool_calls 等结构化字段，不能只取 content。

消息历史每轮追加会导致 Token、延迟和费用随轮数增长，并最终触及 Context Window。常见方案包括滑动窗口、摘要压缩和把旧消息归档后按需检索：滑动窗口简单但会遗忘早期事实；摘要节省上下文但可能失真；检索更灵活但增加存储与召回质量问题。

Q3 待回答：面对长对话即将超过上下文窗口，如何排查并选择处理策略？
<!-- learn-agent:evidence:stage-01-ch01-Q2b-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q3-attempt-1:start -->
### Q3 长对话治理结论与 EX1

Q3 通过：能按早期消息与当前任务的依赖强度，在滑动窗口、摘要压缩、归档检索之间分流，并说明遗忘、摘要失真、额外 Token、存储和读取成本。

排查不只看 messages 数量，还应看实际/估算 Token、各角色占比、System 约束、Tool Call 与 Tool Message 配对、必须保留的事实、延迟和费用。

工程边界修正：滑动窗口通常为本次调用构造新的 context view（上下文视图），不必从权威历史中破坏性删除旧消息；归档检索应按需触发，不必每轮读取。若当前任务对早期事实依赖极强，应优先固定关键事实或结构化 State，并可组合“近期窗口 + 摘要 + 按需检索”，而不是只依赖可能漏召回的检索。

EX1 必做练习：提交可运行代码或可执行伪代码，同时展示最小消息数据流、Message 历史增长、非破坏性窗口处理，以及原生调用到 LangChain ChatModel/Runnable 的框架映射。
<!-- learn-agent:evidence:stage-01-ch01-Q3-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch01-EX1-syntax-hint-1:start -->
### EX1 语法脚手架

Python 最小语法：消息用 list[dict]；函数使用 def、参数和 return；列表追加使用 append；负数切片 history[-window_size:] 取得最近项目；复制列表可使用 list(history) 或 history[:]，用于避免修改原始历史。

非破坏性函数应创建并返回新列表，不在函数内对传入 history 执行 del、pop 或重新切片赋值。

LangChain 当前框架语法：ChatPromptTemplate.from_messages([...]) 构造模板，prompt | model 形成 Runnable 链，chain.invoke({变量名: 值}) 执行。运行数据流为变量映射 → ChatPromptValue → ChatModel → AIMessage。

本提示只提供语法骨架；EX1 的 TODO 逻辑仍由学习者完成。
<!-- learn-agent:evidence:stage-01-ch01-EX1-syntax-hint-1:end -->

<!-- learn-agent:evidence:stage-01-ch01-EX1-attempt-1:start -->
### EX1 attempt 1 — 部分通过

实际运行证据：最小原理版成功生成 system、user、assistant 共 3 条消息；模拟 10 轮后 history 从 3 增长到 23；select_context 返回 5 条上下文且原 history 保持 23 条，证明主路径为非破坏性。

边界测试发现：短历史只有 system + user 且 window_size=4 时，system_messages 与 recent_messages 都包含 system，组合后 system_count=2。修复方向是 recent_messages 只选择非 system 的最近消息，或在合并时去重。

框架部分首先因当前运行环境未安装 langchain_core 而出现 ModuleNotFoundError；即使安装依赖，model=None 也不是 Runnable/ChatModel，不能执行 prompt | model。当前练习允许可执行伪代码，因此无需安装或配置 API，但必须明确 model 是已初始化的 LangChain ChatModel 占位，并补全变量字典 → ChatPromptValue → ChatModel → AIMessage。

验收结果：最小数据流通过；Message 历史增长通过；原生调用到 LangChain ChatModel 的框架映射尚未通过；EX1 required_exercises_passed 仍为 false。
<!-- learn-agent:evidence:stage-01-ch01-EX1-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch01-EX1-attempt-2:start -->
### EX1 attempt 2 — 窗口修复通过，框架类型待补

运行结果：history_size=23，context_size=5，history_unchanged=True；短历史边界 short_system_count=1。recent_messages 先排除 system 再取最后 window_size 条，成功避免固定消息与窗口消息重复，并保持非破坏性。

LangChain 部分已正确标为当前环境不执行的框架伪代码，且 model 被描述为已初始化的 ChatModel；但变量字典经过 prompt 的输出类型、以及 model 的输出类型仍保留 TODO，因此框架映射 acceptance 尚未在本次练习中完整呈现。EX1 仍为部分通过。
<!-- learn-agent:evidence:stage-01-ch01-EX1-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-3:start -->
### Q2 attempt 3 — 需要复习

作答把 prompt 后的数据类型写为 ChatPromptTemplate，并正确写出模型输出 AIMessage。

边界校准：ChatPromptTemplate 是 prompt 组件/对象的类型，保存消息模板并执行格式化；ChatPromptValue 是调用 prompt 后产生的运行时输出，内部包含格式化消息序列，随后作为数据传给 ChatModel。箭头后的空格要求填写流动的数据类型，而不是执行该步骤的组件类型。

结论：AIMessage 已通过；Prompt 组件与 Prompt 输出的区分需要再次复检。EX1 框架映射尚未通过。
<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-3:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-4-and-mastery:start -->
### Q2 attempt 4、EX1 完成与章节验收

Q2 attempt 4 通过：prompt 对象类型为 ChatPromptTemplate；prompt 运行输出类型为 ChatPromptValue；model 运行输出类型为 AIMessage。已能同时区分执行转换的组件与沿 Runnable 链流动的数据。

EX1 验收通过：可运行原理版展示消息构造、模型调用与 AI 消息；运行证据展示 history 从 3 增长至 23；非破坏性 select_context 在长历史与短历史边界均通过；框架伪代码明确原生函数调用到 ChatPromptTemplate / ChatModel / AIMessage 的对应关系。

Mastery 评分（总分 82/100）：概念理解 22/25；因果与数据流解释 18/20；应用与框架映射 16/20；调试与故障排查 13/20；迁移、边界与 Trade-off 13/15。五维均达到 60% floor。Q1 由结构化 Message 因果与失败边界证据满足；Q2 最近有效 attempt 4 通过；Q3 通过；EX1 通过；当前无未纠正的关键误解；integrity healthy；章节验收契约有效。因此本章 mastered=true。

#### 复习卡片

1. 模型不会自动记住历史；应用必须为每次调用重新组织必要 Message。
2. ChatPromptTemplate 是组件，ChatPromptValue 是它运行后产生并传给模型的数据。
3. Runnable 数据流：变量字典 → ChatPromptValue → ChatModel → AIMessage。
4. 权威 history 与单次 model context 必须分离；窗口函数应返回新视图而不是破坏历史。
5. AIMessage 不只看 content，还要保留 usage、response metadata 和 tool calls 等结构化信息。
<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-4-and-mastery:end -->

<!-- learn-agent:evidence:stage-01-ch01-invoke-message-toolcalls-supplement-1:start -->
### 第一节补充：从 `invoke` 到 Agent 工具调用链

#### 1. `model.invoke(messages)` 到底做了什么

`invoke(input)` 是 LangChain Runnable 的统一单次执行接口：给可运行组件一份输入，执行一次，得到一次输出。对 Chat Model 而言，`model.invoke(messages)` 的输入是本次调用要提交的消息序列，输出通常是一个 `AIMessage`，而不是普通字符串。只看正文时可以读取 `response.content`，但保存历史时应保留完整的 `response`。

```python
messages = [
    SystemMessage(content="你是一个 Python 助教"),
    HumanMessage(content="解释列表推导式"),
]

response = model.invoke(messages)   # messages -> Chat Model -> AIMessage
print(response.content)             # 只读取正文
messages.append(response)           # 把完整 AIMessage 加入权威历史
```

模型不会因为调用过一次 `invoke` 就自动拥有长期记忆。下一轮通常先追加新的 `HumanMessage`，再把所需历史重新传入：

```python
messages.append(HumanMessage(content="给我举个例子"))
response = model.invoke(messages)
```

因此，多轮连贯的机制是“应用保存并再次提交历史”，不是 `invoke()` 自己记住了上一轮。`chain.invoke(...)`、`tool.invoke(...)`、`graph.invoke(...)` 也遵循同一个抽象：输入 -> 执行 -> 输出，但各自的输入输出类型不同。

#### 2. 三类 Message 的角色与结构

- `SystemMessage`：系统级指令和行为约束，回答“模型应以什么身份、遵守什么规则工作”。
- `HumanMessage`：用户输入，回答“用户提出了什么问题或要求”。
- `AIMessage`：模型输出，既可能含回答正文，也可能含工具调用与调用元数据。

Message 的心智模型是 `role/type + content + structured fields`。类型让程序可靠区分消息来源；`content` 是正文或多模态内容；结构化字段则保存程序后续还要判断、关联和观测的数据。

#### 3. `metadata`、`response_metadata`、`usage_metadata` 与 `tool_calls`

`metadata` 是“描述消息的附加数据”的总称，不代表所有信息都一定放在同一个名为 `metadata` 的字典里。LangChain 的 `AIMessage` 常见字段包括：

- `response_metadata`：模型供应商或本次响应的附加信息，例如模型标识、停止原因、请求或追踪信息；具体键因供应商而异。
- `usage_metadata`：较标准化的用量信息，例如输入、输出与总 Token；是否完整取决于模型和集成。
- `tool_calls`：模型请求程序执行的结构化工具调用列表；通常包含 `name`、`args` 和用于关联结果的 `id`。没有工具调用时通常为空。

过早只保存 `response.content` 会让正文仍在，却可能丢失角色、Token 成本、停止原因、追踪信息、工具名与参数、tool call id，以及工具请求和结果之间的关联。正确边界是：展示层可以只渲染正文，Harness 的权威历史、执行层和可观测层应尽量保留完整结构；之后再依据上下文预算做有规则的裁剪、摘要或归档。

#### 4. `AIMessage.tool_calls` 如何进入 Agent 循环

`tool_calls` 不是“模型已经执行了工具”，而是“模型生成了一个结构化执行请求”。最小工具调用链是：

```text
HumanMessage
  -> model.invoke(messages)
  -> AIMessage(tool_calls=[{name, args, id}])
  -> Harness 校验参数并按 name 找到工具
  -> tool.invoke(args)
  -> ToolMessage(content=result, tool_call_id=同一个 id)
  -> 再次 model.invoke(包含 AIMessage 与 ToolMessage 的历史)
  -> AIMessage(content=最终回答，或继续产生 tool_calls)
```

Agent/Harness 的职责是检查 `response.tool_calls`，决定结束还是进入工具节点，执行被允许的工具，并用匹配的 `tool_call_id` 把结果作为 `ToolMessage` 回填。模型负责提出调用意图；程序负责校验、授权、真正执行与回传结果。这个结构化闭环正是后续 Tool Calling、Agent 和 LangGraph 条件路由的基础。

> 复习句：`AIMessage.content` 面向回答内容，`AIMessage.tool_calls` 面向程序动作；丢掉后者，Agent 就只能从自然语言猜动作，难以可靠执行和追踪。
<!-- learn-agent:evidence:stage-01-ch01-invoke-message-toolcalls-supplement-1:end -->
