<!-- learn-agent:evidence:stage-01-ch01-relearn-lesson-1-1:start -->
# Chapter 01：LLM、Message、Prompt 与 LangChain

```yaml
schema_version: 2
stage_id: stage-01
chapter_id: 01-llm-message-prompt-langchain
lifecycle_status: active
learning_status: learning
last_updated: 2026-09-07
```

## 重学说明

从 Chapter 01 非破坏性重学。旧状态曾摘要记录 Chapter 01～04 mastered、Chapter 05 Q1 passed，但对应领域证据在工作区迁移后缺失；这些摘要不再作为当前 mastery 证据，旧文件不删除。

## 1.1 LLM 应用的最小数据流

```text
user input (str)
  -> prompt construction
  -> messages (structured records)
  -> model invocation
  -> assistant message
  -> application consumes content and metadata
```

- Prompt 是构造模型输入的规则或模板，不等同于一次对话消息。
- Message 是带 role、content 及可选 metadata 的结构化记录。
- Chat model 接收消息序列，返回下一条 assistant message；它不自动等于完整 Agent。
- 应用负责构造上下文、调用模型、处理输出并决定下一步。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Message:
    role: str
    content: str

def build_messages(user_input: str) -> list[Message]:
    return [
        Message(role="system", content="Answer briefly."),
        Message(role="user", content=user_input),
    ]

def fake_model(messages: list[Message]) -> Message:
    user_message = messages[-1]
    return Message(role="assistant", content=f"Received: {user_message.content}")

messages = build_messages("What is an Agent?")
response = fake_model(messages)
print(response.content)
```

关键边界：真实模型输出具有概率性；即使输入结构正确，也不能仅凭一次自然语言输出断言业务结果正确。
<!-- learn-agent:evidence:stage-01-ch01-relearn-lesson-1-1:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-1-attempt-1:start -->
## L1-CHECK-1 / attempt 1

状态：needs_review，不计入正式 mastery。

- 已正确：Message 是包含 role、content 与可选 metadata 的结构化消息。
- 待修正：Prompt 不只是说明用户输入是什么；它是将规则、模板、变量和示例等组织成模型输入的构造机制。
- 待修正：Chat Model 不生成供另一个 model 使用的输入。它就是模型调用接口，接收 Messages，返回 Assistant Message。

```text
user input / variables
  -> prompt construction
  -> Messages
  -> Chat Model
  -> Assistant Message
  -> application
```
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-1-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-1-attempt-2:start -->
## L1-CHECK-1 / attempt 2

状态：passed。本结果只完成 1.1 学习检查，不等于 Chapter 01 mastered。

用户已正确给出核心方向：Prompt builder 产生 Message，Chat Model 接收 Message 并返回 Assistant Message。精确类型为：

```text
Prompt builder: user input + template variables -> list[Message]
Chat Model: list[Message] -> Assistant Message
```

## 1.2 为什么不能只保存字符串

若只保存 `str`，系统无法可靠区分谁说了什么，也难以保留工具调用、响应 ID、token usage 等元数据。结构化 Message 把消息内容与语义身份一起保存。

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Message:
    role: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)

messages = [
    Message(role="system", content="Answer briefly."),
    Message(role="user", content="What is an Agent?"),
    Message(
        role="assistant",
        content="An Agent selects actions to pursue a goal.",
        metadata={"response_id": "resp_001"},
    ),
]
```

关键点：列表保存顺序，Message 保存每一项的 role、content 和 metadata；两者职责不同。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-1-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-2-attempt-1:start -->
## L1-CHECK-2 / attempt 1

状态：needs_review，不计入正式 mastery。

- 已正确：知道应把对话项改写为带 role 和 content 的 Message；额外改写第三项不影响结论。
- 缺失证据：没有说明 `list[str]` 至少丢失哪两类语义。
- 语法问题：第一项出现重复双引号，并使用全角右括号 `）`，Python 无法解析。

正确的结构形式：

```python
history = [
    Message(role="system", content="Answer briefly."),
    Message(role="user", content="What is an Agent?"),
    Message(
        role="assistant",
        content="An Agent selects actions...",
    ),
]
```
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-2-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-2-attempt-2:start -->
## L1-CHECK-2 / attempt 2

状态：passed。本结果只完成 1.2 学习检查，不等于 Chapter 01 mastered。

用户正确指出 `list[str]` 丢失说话者身份与结构化元数据，并提交了语法合法的 Message 列表。额外改写第三条 assistant 消息不影响通过。

## 1.3 Prompt 是输入转换

Prompt 不应只理解为一段固定字符串。更稳定的心智模型是：Prompt builder 是一个可复用的输入转换器。

```text
user input + template variables -> Prompt builder -> list[Message]
```

```python
def build_messages(topic: str, language: str) -> list[Message]:
    return [
        Message(
            role="system",
            content="Explain concepts accurately and briefly.",
        ),
        Message(
            role="user",
            content=f"Explain {topic} in {language}.",
        ),
    ]

first_messages = build_messages("Agent", "Chinese")
second_messages = build_messages("RAG", "English")
```

构造阶段定义 `build_messages` 的规则；运行阶段传入本次 `topic` 和 `language`，每次产生新的 `list[Message]`。固定规则可复用，运行变量和输出消息随调用变化。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-2-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-3-attempt-1:start -->
## L1-CHECK-3 / attempt 1

状态：passed。用户正确区分定义函数与调用函数，并指出返回值为 list[Message]。

教学精度补充：执行 def 创建函数对象，不执行函数体；每次调用时才计算 f-string、创建 Message 和列表并执行 return。类型注解描述预期类型，不是返回值本身。本次为局部检查通过，不代表整章 mastered。

下一步：预测 first_messages[1].content 与 second_messages[1].content，检查模板变量替换。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-3-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-4-attempt-1:start -->
## L1-CHECK-4 / attempt 1

状态：passed。用户正确预测两次 Prompt builder 调用产生的 user message 内容：`Explain Agent in Chinese` 与 `Explain RAG in English`。标点省略不影响数据流结论。本结果为局部检查通过，不等于 Chapter 01 mastered。

## 1.4 对话历史由应用传入

一次 Chat Model 调用只看到本次传入的 Messages。若下一次调用需要参考上一轮，应用必须保存并重新传入 history。

```python
def run_turn(
    model,
    history: list[Message],
    user_input: str,
) -> tuple[Message, list[Message]]:
    request_messages = [
        *history,
        Message(role="user", content=user_input),
    ]

    assistant_message = model(request_messages)
    new_history = [*request_messages, assistant_message]

    return assistant_message, new_history
```

`[*history, new_message]` 创建新列表，保留旧消息顺序。模型读取 `request_messages`；应用接收 `new_history` 并在下一轮再次传入。若每轮都传空列表，模型看不到此前对话。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-4-attempt-1:end -->

<!-- learn-agent:evidence:sync-checkpoint-20260907T001500+0800:start -->
## 同步 checkpoint

- 时间：2026-09-07T00:15:00+08:00
- 方向：local_workspace → Google Drive sync target
- 教学位置保持：1.4 对话历史由应用传入
- 待继续：L1-CHECK-5 / attempt 1
<!-- learn-agent:evidence:sync-checkpoint-20260907T001500+0800:end -->

<!-- learn-agent:evidence:github-sync-checkpoint-20260907:start -->
## GitHub 同步检查点

- 日期：2026-09-07
- 当前位置：Chapter 01 / 1.4 对话历史由应用传入
- 下一活动：L1-CHECK-5 / attempt 1
- 恢复依据：state.current 与本笔记中的 evidence；聊天历史不作为状态真相源。
<!-- learn-agent:evidence:github-sync-checkpoint-20260907:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-5-attempt-1:start -->
## L1-CHECK-5 / attempt 1

状态：passed。用户正确指出：第一轮对话由应用侧的 `history` 保存；第二次调用 `run_turn` 时必须继续传入更新后的 `history`，模型才有机会看到第一轮内容。

教学精度补充：`history` 是应用持有并在轮次之间更新的状态变量；Chat Model 本身不会因为前一次调用发生过，就自动拥有那次调用的消息。若应用不把旧消息重新放入下一次请求，模型看不到此前对话。

本结果为局部检查通过，不等于 Chapter 01 mastered。

下一步：L1-CHECK-6 / attempt 1，检查当第二轮显式传入空列表 `[]` 时模型可见上下文发生什么变化。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-5-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-6-attempt-1:start -->
## L1-CHECK-6 / attempt 1

状态：passed。用户正确判断第二次调用传入空列表 `[]` 后，模型没有机会知道第一轮里的名字 `Lin`，因为旧的 `history` 没有被传入本次调用。

教学精度补充：`run_turn` 会基于传入的 `history` 构造 `request_messages`。当 `history=[]` 时，本轮 `request_messages` 只包含新加入的 user message，因此此前的 user/assistant 消息都不在模型本次可见输入里。

本结果为局部检查通过，不等于 Chapter 01 mastered。

下一步：L1-CHECK-7 / attempt 1，沿 `run_turn` 说明 `request_messages`、`assistant_message`、`new_history` 三个变量分别是什么以及如何流动。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-6-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-7-attempt-1:start -->
## L1-CHECK-7 / attempt 1

状态：passed。用户正确说明：`request_messages` 把既有 `history` 与当前 `user_input` 组合成发送给 model 的本轮消息列表；`assistant_message` 是 model 根据 `request_messages` 返回的 assistant 消息；`new_history` 再把 `request_messages` 与 `assistant_message` 合并，作为下一轮应继续保存和传入的历史。

数据流可写成：

```text
history + user_input
→ request_messages
→ model
→ assistant_message
→ new_history
→ 下一轮再次作为 history 传入
```

本结果为局部检查通过，不等于 Chapter 01 mastered。

下一步：进入 1.5 LangChain Messages 映射，理解手写 `Message(role=...)` 与 `HumanMessage` / `AIMessage` 的对应关系。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-7-attempt-1:end -->
