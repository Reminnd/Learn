<!-- learn-agent:evidence:stage-01-ch05-section01-loop-purpose:start -->
# Chapter 05：Agent Loop 智能体运行循环

## 5.1 为什么 Tool 执行后还要再次调用模型

一次模型调用只能产生两类关键结果：最终答案，或 Tool Call 请求。Tool Call 不是最终答案；Harness 执行 handler 得到的 observation 也只是外部事实或动作结果。必须把 AIMessage 和与 call id 匹配的 ToolMessage 追加到 messages，再次调用绑定工具后的模型，模型才能读取观察结果、判断是否还需调用其他 Tool，并最终组织面向用户的答案。

最小循环：初始化 messages → 调用 model_with_tools → 追加 AIMessage → 若没有 tool_calls 则返回最终 content → 若有则逐个通过 Registry/Executor 执行 → 追加 ToolMessage → 回到模型。终止条件至少包括模型不再请求 Tool 和 max_turns；生产系统还要限制 max_tool_calls、总超时、token/费用、重复调用与副作用。

手写版 `while/for` 负责循环控制；LangChain `create_agent` 封装模型节点、工具节点与终止路由，并运行在 LangGraph Runtime 上；LangGraph 自定义实现用 model node、tool node、conditional edge 与 END 表达同一循环。

失败边界：如果 Tool 执行后直接把原始 result 返回用户，模型没有机会解释或综合结果；如果无条件继续调用模型，则模型持续重复 Tool Call 时会形成死循环和成本失控。
<!-- learn-agent:evidence:stage-01-ch05-section01-loop-purpose:end -->

<!-- learn-agent:evidence:stage-01-ch05-Q1-pass-and-section02:start -->
## Q1 通过：observation 回传与循环失败边界

作答准确说明只有模型能够解释工具结果、判断是否继续调用其他 Tool、综合多个结果并判断任务完成。失败案例指出：ToolMessage `content=上海: sunny` 只是 observation，若不回传模型就缺少最终解释与综合；模型持续重复 Tool Call 则会造成死循环、token/费用失控和重复副作用。Q1 的因果关系与失败边界均满足。补充：Tool result 即使表面上像用户答案，也不能被 Harness 普遍假定为最终答案。

## 5.2 手写循环 → LangChain Agent → LangGraph execution

### 真实问题与最小手写实现

一次 `model.invoke()` 不能完成工具型任务：模型先请求 Tool，Harness 执行后还要把 observation 写回消息，再让模型继续决策。最小原理就是一个保存 messages、分支和终止条件的循环。

```python
from dataclasses import dataclass, field

@dataclass
class AIMessage:
    content: str = ""
    tool_calls: list[dict] = field(default_factory=list)

@dataclass
class ToolMessage:
    content: str
    tool_call_id: str

class FakeModelWithTools:
    def invoke(self, messages):
        tool_results = [m for m in messages if isinstance(m, ToolMessage)]
        if not tool_results:
            return AIMessage(tool_calls=[{
                "name": "get_weather",
                "args": {"city": "上海"},
                "id": "call_001",
            }])
        return AIMessage(content=f"最终回答：{tool_results[-1].content}")

def run_agent(model_with_tools, registry, user_text, max_turns=3):
    messages = [{"role": "user", "content": user_text}]
    for turn in range(max_turns):
        ai_message = model_with_tools.invoke(messages)
        messages.append(ai_message)
        if not ai_message.tool_calls:
            return {"output": ai_message.content, "messages": messages}
        for call in ai_message.tool_calls:
            handler = registry[call["name"]]
            observation = handler(**call["args"])
            messages.append(ToolMessage(
                content=str(observation),
                tool_call_id=call["id"],
            ))
    raise RuntimeError("max_turns_exceeded")

registry = {"get_weather": lambda city: f"{city}: sunny"}
result = run_agent(FakeModelWithTools(), registry, "上海天气怎么样？")
print(result["output"])
```

### 构造阶段

- `registry`：长期存在的 Tool name → handler/Tool 映射；在 run 前完成注册。
- `model_with_tools`：已经知道可用 Tool Schema 的模型对象；在 run 间可以复用。
- `run_agent(...)`：Harness 的循环函数；定义控制策略，但此时尚未产生 AIMessage 或 ToolMessage。
- LangChain `create_agent(model, tools)`：把模型、Tools、消息状态和路由构造成可调用的图式 Agent；构造时不执行用户请求。

### 运行阶段与每条箭头

1. 输入 `user_text/messages`，创建本次 run 的消息状态。
2. model node 接收完整 messages，输出 AIMessage，并把它追加到状态。
3. conditional edge 读取最新 AIMessage 的 `tool_calls`：为空则 END；非空则进入 tools node。
4. tools node 接收 ToolCall `{name,args,id}`，按 name 查找 Tool，用 args 执行，输出 `ToolMessage{content,tool_call_id}`。
5. ToolMessage 写回 messages；固定回边把状态送回 model node。
6. 最终没有 tool_calls 的 AIMessage 进入 END，Agent 返回更新后的状态；最终文本通常取最后一条 AIMessage.content。

### 对象、类型与生命周期映射

| 手写对象 | LangChain/LangGraph 对象 | 生命周期与责任 |
|---|---|---|
| `messages: list` | `MessagesState["messages"]` / Agent state | 单次 run 内持续增长，可由持久化扩展到跨 run |
| `model_with_tools.invoke(messages)` | model node | 每轮读取状态并产生 AIMessage |
| `AIMessage.tool_calls` 检查 | conditional edge / routing function | 每轮决定 tools 或 END |
| Registry + Executor | tools node / `ToolNode` | 按 name 查找、传 args、产生 ToolMessage |
| `messages.append(ToolMessage)` | node 返回消息状态更新 | observation 进入下一轮模型上下文 |
| `continue` | tools → model 回边 | 调度下一轮 |
| `return` | `END` | 终止本次 run |
| 整个 while/for | `create_agent` 的图式运行时 | 反复调度模型和工具节点 |

### 最小 LangChain 框架代码

```python
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """查询指定城市的天气。"""
    return f"{city}: sunny"

# 构造阶段：model 是已经初始化的 ChatModel。
agent = create_agent(model=model, tools=[get_weather])

# 运行阶段：输入 Agent state，框架内部循环，输出更新后的 state。
state = agent.invoke({
    "messages": [
        {"role": "user", "content": "上海天气怎么样？"}
    ]
})
print(state["messages"][-1].content)
```

内部行为不是 `create_agent` 自动替模型执行一次函数，而是：调用 model node → 发现 Tool Call → tools node 执行 → ToolMessage 写回 → 再调用 model node → 满足终止条件后返回。

### LangGraph 显式结构

```text
START → model_node
          ├─ latest_ai.tool_calls 非空 → ToolNode → model_node
          └─ latest_ai.tool_calls 为空 → END
```

手写 `if` 变成 conditional edge，手写 `continue` 变成回边，手写 `messages.append` 变成节点状态更新，手写 `return` 变成 END。

### 框架封装与 Harness 责任

框架封装：消息状态传递、模型/工具节点调度、Tool Call 与 ToolMessage 关联、条件路由以及基础循环。Harness 仍负责：允许暴露哪些 Tool、权限与审批、args 和业务校验、max model/tool calls、总超时、token/费用、幂等与副作用、重复调用检测、审计、stop_reason 和最终输出验证。

失败边界与 Trade-off：手写循环透明且容易定制，但容易漏掉消息顺序、id 关联、终止和并行调用；`create_agent` 开发快且采用预构建运行时，但精细控制需 middleware 或自定义 LangGraph。`max_turns` 通常按模型轮次计数；LangGraph `recursion_limit` 按 super-step 计数，二者不能机械等同。
<!-- learn-agent:evidence:stage-01-ch05-Q1-pass-and-section02:end -->
