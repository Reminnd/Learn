<!-- learn-agent:evidence:stage-01-ch04-section01-registry-boundary:start -->
# Chapter 04：Tool Registry 与工具工程化

## 4.1 统一注册、唯一性与职责边界

当系统只有一个 Tool 时，可以直接调用 handler；当 Tool 数量增长后，各调用点散落的 `if/elif` 或临时字典会造成重复名称静默覆盖、Schema 与执行策略不一致、权限和审计难以集中管理。最小 Tool Registry 负责统一注册、名称唯一性校验、按名称查找以及对模型暴露可用 Tool 的公开规格。

职责分层：Registry 管 Tool 定义的注册与发现；Policy 决定某次请求是否允许调用、风险、审批、超时与重试；Executor 校验 args、执行 handler、分类异常并包装结果。模型只应看到经过过滤的 name、description、parameters，不应直接得到 handler 或内部敏感元数据。

生命周期：声明 Tool → 注册并校验唯一性 → 按身份和上下文过滤 → 向模型暴露 Schema → LLM 生成 Tool Call → Registry 查找 → Policy 检查 → 参数校验 → handler 执行 → 结果限长与审计 → ToolMessage 回传。

危险写法 `{tool["name"]: tool for tool in tools}` 遇到重名时会保留后一个值，静默丢失前一个 Tool。生产级 Registry 应在 register 阶段显式拒绝重名，使配置错误在模型调用前 fail fast。

LangGraph 官方 quickstart 使用 `tools_by_name = {tool.name: tool for tool in tools}` 完成名称查找，`model.bind_tools(tools)` 向模型暴露工具，执行节点再用 name 查找并调用 Tool，最后按 `tool_call_id` 生成 ToolMessage。该字典是最小 Registry 映射；生产系统还需补唯一性、过滤、策略、审计和生命周期能力。
<!-- learn-agent:evidence:stage-01-ch04-section01-registry-boundary:end -->

<!-- learn-agent:evidence:stage-01-ch04-Q1-pass-and-section02:start -->
## Q1 通过：统一管理边界与重名失败链

作答准确指出 Registry 是 Tool 的统一管理边界：内部可以使用字典，但通过 `register()` 控制允许进入的对象，通过 `get()` 控制安全查找，通过 `list_specs()` 控制暴露给 LLM 的信息。生产级能力还包括名称唯一性、生命周期、权限、审计、元数据、版本与启用/禁用；这些横切能力若散落在调用点的 `if/elif` 或临时字典中，会难以维护并产生策略不一致。

失败案例完整：当 `weather_tool_v1` 与 `weather_tool_v2` 同名时，字典推导式只保留 v2，v1 被静默覆盖。因配置阶段没有报错，后续模型可能调用到错误版本，形成难以及时定位的运行时错误。Q1 的核心因果关系与失败条件均满足。

## 4.2 ALL_TOOLS dict → Registry → ToolNode

原理侧最小对象是 `ALL_TOOLS: dict[str, Tool]`，输入是一组 Tool 定义，输出是按唯一 name 索引的 Tool 集合。生产级 Registry 在字典外增加注册校验、过滤和查询接口。

框架侧：LangChain `@tool` 产生带 name、description、args schema 与 invoke 能力的 Tool 对象；`model.bind_tools(tools)` 把公开工具 Schema 提供给 LLM；LLM 输出 `AIMessage.tool_calls`；LangGraph 的 `ToolNode` 或自定义工具节点根据 name 查找 Tool、传入 args 执行，并按 id 返回 `ToolMessage`。

关键边界：`bind_tools` 是向模型暴露工具能力，Registry 是 Harness 内部的可信查找与治理边界，`ToolNode` 是执行节点。三者不能因为都接触 tools 就视为同一个职责。
<!-- learn-agent:evidence:stage-01-ch04-Q1-pass-and-section02:end -->

<!-- learn-agent:evidence:stage-01-ch04-section02-io-boundary-correction:start -->
### 4.2 输入输出、对象类型与执行边界

#### Registry / Policy / Executor 三层职责

| 层 | 核心问题 | 输入 | 输出 | 不负责 |
|---|---|---|---|---|
| Registry | 系统注册了什么 Tool，如何唯一查找 | 完整 Tool 定义，或 Tool name | 注册状态、Tool 对象、公开 specs | 不决定本次请求能否调用；不执行 handler |
| Policy | 当前身份和上下文允许调用什么、按什么约束调用 | 用户身份、请求上下文、Tool 元数据与风险策略 | 允许/拒绝、可见 Tool 集合、审批/超时/重试等约束 | 不保存 Tool handler；不直接产生工具结果 |
| Executor / ToolNode | 怎样安全执行已经获准的 Tool Call | ToolCall、Registry 查到的 Tool、Policy 约束 | ToolMessage 或受控错误结果 | 不替 LLM 决定是否调用 Tool |

典型顺序是：Registry 注册并保证定义唯一 → Policy 按本次请求筛选 → `bind_tools` 只把允许暴露的 Schema 交给模型 → LLM 决策 → Executor / ToolNode 执行。三层可以在最小示例中写得很近，但职责不能混合。

#### 调用链中的输入、输出与对象类型

| 环节 | 输入 | 输出 | 类型边界 |
|---|---|---|---|
| `Registry.register(tool)` | 完整 Tool 对象：`name`、`description`、参数 Schema、`handler` 等 | Registry 内部状态更新；重名时直接抛错 | 输入不是只有 name；成功结果主要是副作用，不是模型消息 |
| `Registry.list_specs()` / Policy 筛选 | Registry 中的已注册 Tool；需要时加身份、权限、运行上下文 | 允许给本次 LLM 看到的公开 Tool specs | 只保留 `name`、`description`、参数 Schema 等公开信息，不暴露 `handler` |
| `model.bind_tools(tools_or_specs)` | Tool 列表或框架可转换的工具定义 | 绑定工具能力后的模型对象，例如 `model_with_tools` | 这里只配置工具 Schema；不会调用 handler，也不会产生 ToolMessage |
| `model_with_tools.invoke(messages)` | 消息列表；绑定模型同时携带可选工具 Schema | `AIMessage` | `AIMessage` 是 LLM 的直接输出对象，不是 ToolCall，也不是 ToolMessage |
| `AIMessage.tool_calls` | 无需额外调用；它是 `AIMessage` 的属性 | `list[ToolCall]`，可能为空 | 模型可选择直接回答，因此不能假定一定存在第 0 项 |
| 单个 `ToolCall` | 来自 `AIMessage.tool_calls` 列表 | `name`、`args`、`id` | `name` 用于查找 Tool，`args` 是 handler 参数，`id` 用于关联返回结果 |
| `ToolNode` / Executor | 一个或多个 ToolCall；按 `name` 从 Registry 查找 Tool，以 `args` 调用 | 一个或多个 `ToolMessage` | 执行发生在这里，而不是 `bind_tools` 或 LLM 内部 |
| `ToolMessage` | handler 的结果与原 `ToolCall.id` | 追加回 messages 的工具观察结果 | 关键字段是 `content` 与 `tool_call_id`；`tool_call_id == ToolCall.id` |

安全分支必须先检查列表：

```python
ai_message = model_with_tools.invoke(messages)

if not ai_message.tool_calls:
    return ai_message.content

for tool_call in ai_message.tool_calls:
    # ToolCall: {"name": ..., "args": ..., "id": ...}
    tool_message = executor.execute(tool_call)
    messages.append(tool_message)
```

不能直接写 `ai_message.tool_calls[0]`：当模型认为无需工具时，`tool_calls == []`，此时正确结果就是 `AIMessage.content`，盲目访问 `[0]` 会触发越界错误。即使列表非空，也可能一次包含多个 ToolCall，因此执行侧要明确支持多个调用或显式限制并报错。

#### 从一次调用到 Agent Loop

一次 Tool 执行不是流程终点。Executor 产生的 `ToolMessage` 要追加回消息历史，再次调用 LLM：

```text
messages → LLM → AIMessage
                  ├─ tool_calls 为空 → 使用 content，结束
                  └─ tool_calls 非空 → Executor / ToolNode
                                         ↓
                                   ToolMessage 追加回 messages
                                         ↓
                                      再次调用 LLM
```

每一轮得到的都是新的 `AIMessage`，所以循环必须每轮重新读取并检查当前 `ai_message.tool_calls`，不能沿用上一轮判断。模型可能在看到第一次工具结果后继续发出第二轮、第三轮 Tool Call，直到某轮 `tool_calls` 为空并在 `content` 中给出最终回答。生产实现还必须配置轮数、工具调用数、时间与成本等终止预算，防止无限循环。
<!-- learn-agent:evidence:stage-01-ch04-section02-io-boundary-correction:end -->

<!-- learn-agent:evidence:stage-01-ch04-Q2-pass-and-section03:start -->
## Q2 复检通过：对象类型链

复检代码正确形成：`tools list → bound model → AIMessage → ToolCall → Tool result → ToolMessage`。类型边界明确：`model_with_tools` 是绑定工具后的模型；`ai_message` 是 AIMessage 对象；`ai_message.tool_calls` 是列表；其中单个 `tool_call` 是字典式 ToolCall，包含 name、args、id；result 是工具返回值；tool_message 是 ToolMessage 对象，以 content 和 tool_call_id 关联执行结果与原请求。此前边界误解已解决。

## 4.3 工具冲突：排查顺序与方案权衡

可执行排查顺序：1. 在构造 dict 前枚举所有原始 Tool，统计 name；2. 按 name 分组定位重复来源；3. 比较重复项的 description、Schema、handler、版本、来源和启用状态；4. 判断是配置重复、兼容版本共存还是插件覆盖；5. 选择冲突策略并重新注册；6. 测试 Registry 结果、模型可见 specs、实际 handler 与审计日志。不要先查看最终 dict，因为静默覆盖后已经丢失被覆盖项。

常见策略及 Trade-off：默认 fail-fast 拒绝重名最安全，能把错误阻断在启动/注册阶段，但不支持隐式热替换；显式版本名或命名空间允许多版本共存，但会增加模型可选工具数量、提示 token 和误选概率；受控 override 适合插件或灰度替换，但必须显式声明优先级、记录旧新来源并审计，否则会重新引入静默覆盖。
<!-- learn-agent:evidence:stage-01-ch04-Q2-pass-and-section03:end -->

<!-- learn-agent:evidence:stage-01-ch04-Q3-pass-and-EX1-start:start -->
## Q3 复检通过：分层排查与版本化位置

复检给出可执行顺序：打印原始 Tool 列表；按 name 定位重名来源并比较 Tool 其他字段；在原始 Tool 定义中显式修改 name；重新注册后打印 Registry 和模型暴露结果验证。结合 attempt 1 已说明的 tools 列表冗长、新旧版本共存代价，以及教学补充的 token、误选与维护成本，Q3 的排查顺序和 Trade-off 均满足。

重要边界：版本号应在 Tool 定义或注册配置进入 Registry 之前确定；注册后直接修改 Registry 内部 Tool 的 name，会造成字典键仍是旧 name、Tool 自身却是新 name 的索引不一致。参数 Schema 只校验 city、unit 等 args，不负责修改 Tool name。

## 4.4 EX1：最小 Tool Registry

必做练习需要产出可运行 Python：实现统一注册、拒绝同名、按 name 查找、列出模型可见 specs；注册两个正常 Tool；复现同名冲突；最后用注释或可执行伪代码说明 `ALL_TOOLS dict → Registry`、`bind_tools`、`AIMessage.tool_calls` 与 `ToolNode/Executor` 的对应关系。
<!-- learn-agent:evidence:stage-01-ch04-Q3-pass-and-EX1-start:end -->

<!-- learn-agent:evidence:stage-01-ch04-EX1-pass-and-mastery:start -->
## EX1 运行通过与 Chapter 04 掌握判定

用户完成可运行的 `ToolRegistry`：`register()` 按 name 统一注册并拒绝重复；`get()` 对未知 name 抛出 LookupError；`list_specs()` 只暴露 name、description、parameters，不暴露 handler。实际运行证据：Registry keys 为 get_weather、search_city；天气 Tool 返回 `上海: sunny`；公开 specs 的 `HANDLER_EXPOSED=False`；重复注册 get_weather 被 ValueError 捕获。框架注释正确表达 `ALL_TOOLS dict → ToolRegistry` 与 `tools → bind_tools → AIMessage.tool_calls → ToolNode/Executor → ToolMessage`。EX1 三项 acceptance 全部通过。

### 掌握评分（85/100）

- 概念理解：22/25。能说明 Registry 统一管理边界、唯一性和公开规格。
- 因果与数据流解释：17/20。能追踪 bound model、AIMessage、ToolCall、执行结果与 ToolMessage；类型边界经复检稳定。
- 应用与框架映射：16/20。最小 Registry 运行通过，并能映射到 bind_tools 与 ToolNode；实现使用完整脚手架。
- 调试与故障排查：17/20。能在原始 Tool 列表定位重名、比较差异、在定义层修复并重新验证。
- 迁移、边界与 Trade-off：13/15。能区分注册 name 与 args Schema，说明版本化的工具膨胀、新旧共存、token、误选和维护代价。

五个维度均达到 60% 下限；关键题 Q1、Q2 最近有效作答通过；Q3 通过；必做 EX1 通过；未解决关键误解为 0；完整性 healthy；章节验收契约合法。因此 `mastered=true`。

后续强化：register 入口还可校验 Tool 结构并复制/冻结定义，避免注册后外部修改；生产 Registry 还需增加 enabled、version、risk、timeout、retry、权限、审计与结果大小策略。这些会在后续 Harness/Reliability/Security 单元继续展开。
<!-- learn-agent:evidence:stage-01-ch04-EX1-pass-and-mastery:end -->

<!-- learn-agent:evidence:stage-01-ch04-session-summary-20260822:start -->
## 2026-08-22 学习收尾

本次完成 Chapter 04 Tool Registry Engineering，掌握评分 85/100。核心链路已经贯通：Tool 定义 → Registry 注册与唯一性校验 → Policy 筛选 → `bind_tools` 暴露 Schema → LLM 输出 `AIMessage.tool_calls{name,args,id}` → Registry 查找 → Executor/ToolNode 执行 → `ToolMessage{content,tool_call_id}`。

已验证的代码能力：实现 `register()`、`get()`、`list_specs()`；公开 specs 不暴露 handler；正常 Tool 可查找执行；同名 Tool 在注册阶段 fail fast。已解决的边界误解：`bind_tools` 返回绑定后的模型而非 Tool；AIMessage、ToolCall、ToolMessage 是不同对象；Tool name 冲突属于定义/注册层，不属于 args Schema；注册后不得直接修改 Tool name 造成 Registry key/name 不一致。

课程大纲已加入生产级 Tool Registry 强化路线：Tool 结构校验、定义冻结、权限、风险等级、超时、重试、审计和结果限长。后续按模块深化：结果限长 → Context Engineering；超时与重试 → Planning/Reliability；审计 → Observability；权限与风险 → Security。

下次从 Chapter 05 Agent Loop 开始，把 LLM 决策、Registry 查找、Tool 执行、ToolMessage 回传和模型再次调用连接成循环。
<!-- learn-agent:evidence:stage-01-ch04-session-summary-20260822:end -->

<!-- learn-agent:evidence:stage-01-ch04-registry-rename-consistency:start -->
## 补充：Registry 改名一致性与封装边界

前文 4.1～4.2 已说明 Registry 负责 Tool 定义的统一注册、唯一查找和公开规格，而 Policy 决定能否调用、Executor/ToolNode 负责执行。本节只补充 Registry 自身必须长期维护的不变量：

```text
Registry 的索引 key == 该索引指向的 Tool.name
```

注册后若外部直接执行 `tool["name"] = "get_weather_v2"`，字典中仍可能保存旧 key `get_weather`，Tool 内部却已变成新 name。此时 `list_specs()` 若从 Tool 读取 name，会向 LLM 暴露 `get_weather_v2`；LLM 随后生成 name 为 `get_weather_v2` 的 Tool Call；Executor 调用 `registry.get("get_weather_v2")` 时却只能按 Registry key 查找，因此得到 unknown tool。故障链是：旧 key 与新 `Tool.name` 失配 → specs 暴露新名 → LLM 使用新名 → Registry 查找失败。

改名必须经过 Registry 的专门接口，在同一个受控操作中检查旧名存在、拒绝新名冲突、移除旧 key、更新 `Tool.name`、写入新 key，并在操作结束后重新验证 `new_key == Tool.name`：

```python
def rename(self, old_name, new_name):
    if old_name not in self._tools:
        raise LookupError(f"未知工具：{old_name}")
    if new_name in self._tools:
        raise ValueError(f"工具名称已存在：{new_name}")

    tool = self._tools.pop(old_name)
    tool["name"] = new_name
    self._tools[new_name] = tool
```

这里的“原子”首先表示调用者只观察到一次完整的逻辑改名，不应自行分步修改索引和 Tool；若 Registry 会被多线程并发访问，还需在该临界区加锁，并在中途失败时回滚，避免其他线程观察到半更新状态。

`_tools` 的下划线表示它是内部实现细节，不是外部可随意改写的公共 API。调用方应通过 `register()`、`get()`、`list_specs()`、`rename()` 等接口操作，让 Registry 有机会统一执行唯一性检查、封装公开字段、维持 key/name 不变量，并在生产系统中接入审计或并发保护。
<!-- learn-agent:evidence:stage-01-ch04-registry-rename-consistency:end -->

<!-- learn-agent:evidence:stage-01-ch04-registry-mechanics-and-framework-mapping:start -->
## 4.1 补充：`tools_by_name` 的构造原理与 Registry 边界

### 从 `list[Tool]` 到 `dict[name, Tool]`

假设 `tools` 是 Tool 对象列表：

```python
tools = [weather_tool, search_tool]
tools_by_name = {tool.name: tool for tool in tools}
```

字典推导式会依次取出列表中的每个 `tool`：用 `tool.name` 计算字典键，用 `tool` 对象本身作为字典值。等价的展开写法是：

```python
tools_by_name = {}
for tool in tools:
    tools_by_name[tool.name] = tool
```

因此它完成的是一个索引转换，而不是创建新的 Tool：

```text
[weather_tool, search_tool]
        ↓ 按每个 Tool 的 name 建索引
{
    "get_weather": weather_tool,
    "search_city": search_tool,
}
```

列表适合按顺序遍历或整体传给 `model.bind_tools(tools)`；字典适合执行阶段根据模型给出的 `tool_call["name"]` 快速找到对应 Tool。这个 `name → Tool` 索引把 Chapter 03 的 Tool Call 接到了 Chapter 04 的查找与治理边界。

### 手写 Tool 与 LangChain Tool 的一一映射

手写版把 Tool 表示为字典：

```python
tool = {
    "name": "get_weather",
    "handler": get_weather,
}

handler = tool["handler"]
result = handler(**tool_call["args"])
```

`tool["handler"]` 取得函数对象；`**args` 把 `{"city": "上海"}` 解包成 `city="上海"`，最终等价于 `get_weather(city="上海")`。

LangChain Tool 把同样的概念封装成对象属性与统一执行接口：

```python
tool = tools_by_name[tool_call["name"]]
result = tool.invoke(tool_call["args"])
```

对应关系如下：

| 最小手写版 | LangChain Tool | 含义 |
|---|---|---|
| `tool["name"]` | `tool.name` | Tool 的唯一查找名称 |
| `tool["handler"]` | Tool 对象内部封装的执行函数 | 真正完成业务动作的 callable |
| `handler(**args)` | `tool.invoke(args)` | 用模型生成并已校验的参数执行 Tool |
| 手写 `parameters` | `tool.args_schema` / Tool Schema | 告诉模型参数结构并支持校验 |

两者本质流程相同：`name` 定位定义，`args` 进入执行入口，得到 result。区别是 LangChain Tool 把 Schema、调用协议、错误处理与框架集成封装到了 Tool 对象和 `invoke()` 中。

### 为什么 `tools_by_name` 只是最小版 Registry

`tools_by_name` 只解决“按 name 查找 Tool”这一件事。它没有管理 Tool 如何进入索引、哪些定义能向模型公开、发生冲突时如何失败，也没有稳定的公共接口。因此它是 Registry 的最小内部索引，而不是生产级 Registry 本身。

尤其是同名 Tool 会被静默覆盖：

```python
weather_v1.name = "get_weather"
weather_v2.name = "get_weather"

tools_by_name = {tool.name: tool for tool in [weather_v1, weather_v2]}
assert tools_by_name["get_weather"] is weather_v2
```

构造过程先写入 v1，随后同一个键被 v2 覆盖；字典不会主动报错，最终只剩 v2。配置问题因此被推迟到运行阶段，可能执行错误版本且难以排查。

生产级 Registry 用受控接口划分管理边界：

- `register(tool)`：校验 Tool 结构与名称唯一性，再写入内部索引；发现重名立即抛错，实现 fail fast（尽早失败）。
- `get(name)`：按名称安全查找；未知名称明确报错，不把内部字典直接暴露给调用方。
- `list_specs(context)`：只返回允许向模型公开的 name、description、parameters 等规格；可结合身份、权限、启用状态和 Policy 过滤，不能泄露 handler。

名称唯一性必须在 `register()` 阶段检查，而不是先用字典推导式覆盖后再检查，因为覆盖发生后被替换的原对象已经从最终字典中消失。

结论：`Registry ≠ dict`。Registry 是注册、查询、公开规格与不变量校验的管理抽象；`dict[str, Tool]` 只是它可以选择的一种内部索引数据结构。以后即使内部改成数据库、插件目录或远程服务，`register/get/list_specs` 的治理边界仍然成立。

### 与 Chapter 01–03 的必要衔接

- Chapter 01：模型通过消息产生 `AIMessage`，Tool Calling 仍属于消息驱动的数据流。
- Chapter 02：`args` 是结构化输出，必须满足 Tool Schema；Schema 负责参数形状，不负责解决 Tool 名称冲突。
- Chapter 03：`AIMessage.tool_calls` 提供 `name`、`args`、`id`；Executor 执行 Tool 并用 `tool_call_id` 生成 `ToolMessage`。
- Chapter 04：Registry 接住其中的 `name`，稳定地找到正确 Tool，并在执行前提供唯一性、公开范围与治理边界。
<!-- learn-agent:evidence:stage-01-ch04-registry-mechanics-and-framework-mapping:end -->

<!-- learn-agent:evidence:stage-01-ch04-registry-dict-semantics-20260822:start -->
## 4.5 Python 代码阅读补充：Registry 字典与公开 specs

### `self._tools[name] = tool`：按名称保存完整 Tool

Python 字典赋值的通式是 `字典[key] = value`。因此在 `self._tools[name] = tool` 中，`self._tools` 是 Registry 内部字典，`name` 是索引键，`tool` 是包含 `name`、`description`、`parameters`、`handler` 等字段的完整 Tool。若 `name == "get_weather"`，这句就等价于 `self._tools["get_weather"] = tool`。之后执行阶段可以用 Tool Call 的名称直接查找对应 Tool，而不必维护不断增长的 `if/elif`。

这句赋值本身允许覆盖旧值，所以必须在它之前执行重名检查：

```python
if name in self._tools:
    raise ValueError(f"工具名称重复：{name}")
self._tools[name] = tool
```

这样，字典负责 O(1) 平均复杂度的按名索引，`register()` 则额外负责唯一性规则；外部代码不应直接修改 `_tools`，否则会绕过这些检查。

### `.keys()`、`.values()`、`.items()` 的选择

对形如 `{"get_weather": weather_tool}` 的 Registry 字典：

| 写法 | 每次迭代得到 | 适用场景 |
|---|---|---|
| `self._tools.keys()` | Tool 名称，也就是 key | 只需要名称 |
| `self._tools.values()` | 完整 Tool，也就是 value | 需要读取 Tool 的 description、parameters 等字段 |
| `self._tools.items()` | `(name, tool)` 键值对 | 同时需要名称和完整 Tool |

所以 `for tool in self._tools.values():` 的意思是：逐个取出 Registry 中保存的完整 Tool，并在每轮把当前对象命名为 `tool`。如果改用 `.keys()`，循环变量只是字符串名称；还要再通过 `self._tools[name]` 查一次才能读取 Tool 字段。

### `list_specs()` 列表推导式的等价展开

紧凑写法：

```python
def list_specs(self):
    return [
        {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["parameters"],
        }
        for tool in self._tools.values()
    ]
```

等价于普通循环：

```python
def list_specs(self):
    result = []

    for tool in self._tools.values():
        spec = {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["parameters"],
        }
        result.append(spec)

    return result
```

执行顺序是：遍历完整 Tool → 从当前 Tool 投影出公开字段 → 把新 spec 追加到 `result` → 返回 specs 列表。这里的列表推导式不是直接返回内部 Tool，而是在构造新的公开字典。

### 为什么公开 Tool spec 不包含 `handler`

`name`、`description`、`parameters` 构成模型的调用说明：告诉 LLM 有哪些工具、何时使用以及参数应是什么形状。`handler` 则是 Harness 内部的执行引用：告诉 Python 在工具被批准调用后真正运行哪个函数。两者属于不同信任边界。

`list_specs()` 排除 `handler` 有四个直接作用：

1. 保持最小公开接口，模型只接收做调用决策所必需的信息。
2. 避免把 Python 函数对象交给需要 JSON/Schema 序列化的模型接口。
3. 防止模型侧数据与 Harness 的执行实现强耦合，也减少无关上下文。
4. 保留执行控制权：模型只能提出 `{name, args}`，Registry、Policy 与 Executor 决定查找、授权、校验和执行。

因此内部 Tool 与公开 spec 是同一工具的两个视图：内部对象包含执行能力，公开 spec 只描述可调用契约。隐藏 `handler` 本身不是完整的安全机制；真正的安全仍依赖权限、参数校验、审批、超时和审计。
<!-- learn-agent:evidence:stage-01-ch04-registry-dict-semantics-20260822:end -->
