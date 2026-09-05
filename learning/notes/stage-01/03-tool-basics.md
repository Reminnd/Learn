<!-- learn-agent:evidence:stage-01-ch03-section01-tool-contract:start -->
# Tool 基础与 LangChain @tool — 课程笔记

## Metadata

- stage_id: `stage-01`
- chapter_id: `03-tool-basics`
- schema_version: `2`
- lifecycle_status: consolidated
- learning_status: mastered
- last_updated: `2026-08-21`

## 1. 为什么模型需要 Tool

模型本身主要负责生成和推理，不能因为输出一句“我查询了数据库”就真的完成外部操作。Tool 把外部能力声明成可验证、可执行的契约；模型只提出调用请求，Agent Harness 才负责校验参数、执行 Python handler、记录结果并把结果交回模型。

## 2. Tool 的四个最小组成部分

- `name`：稳定且唯一的机器标识，用于把模型请求路由到正确 handler。
- `description`：告诉模型何时使用、何时不要使用；含糊会导致选错工具。
- `parameters`：参数 Schema，声明字段名、类型、必填项和约束；用于模型生成参数和运行前校验。
- `handler`：真正执行副作用或查询的 Python 函数；模型不能替代 handler 执行。

## 3. 最小手写数据流

```text
用户请求
→ 模型产生 tool_call {name, args, id}
→ Harness 按 name 找到 Tool
→ 根据 parameters 校验 args
→ handler(**args)
→ 结果包装为 ToolMessage，tool_call_id 与请求 id 对应
→ 模型读取结果并生成后续回答
```

关键边界：`AIMessage.tool_calls` 是执行请求，不是执行结果。若模型请求了多个 Tool Call，每一个 id 都应有对应的 ToolMessage，否则消息链不完整。

## 4. 普通函数到 LangChain @tool

```python
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气；不要用于历史天气。"""
    return f"{city}: sunny"
```

映射关系：函数名默认成为 `name`；docstring 成为 `description`；类型标注生成参数 Schema；函数体是 handler。`model.bind_tools([get_weather])` 把 Tool Schema 提供给模型，但不会自动替独立调用的模型执行 handler；手写循环仍要读取 `AIMessage.tool_calls`、执行 Tool 并把结果返回模型。

## 5. 异常处理强化计划

后续参数错误练习中，处理层优先返回机器可判断动作，如 `retry_model`、`repair_then_validate`、`fail_fast`，同时把人类提示作为单独字段或日志信息。重点区分参数生成错误、Schema 校验错误、handler 业务错误、外部服务瞬时错误和不可重试错误。

## Q1 待回答

为什么一个 Tool 不能只有 Python 函数体，而需要 name、description、parameters、handler 四部分？请说明至少一个缺失或设计不当时的失败案例。
<!-- learn-agent:evidence:stage-01-ch03-section01-tool-contract:end -->

<!-- learn-agent:evidence:stage-01-ch03-Q1-pass-and-minimal-executor:start -->
## Q1 通过：四要素的因果与失败边界

作答完整说明了四部分的工程作用：缺少 name 时 Harness 无法路由；description 含糊会导致模型漏选、错选或重复选择；parameters 缺失会让模型缺少参数生成契约，也让 Harness 无法在执行前校验；handler 缺失或错误会使请求无法执行，或产生错误结果与副作用。满足核心因果与失败条件要求。

边界校准：handler 负责确定性执行和明确输出；Tool 结果如何参与后续推理通常由 Agent Loop 与模型负责，不应把所有后续业务决策都塞进 handler。

## 3.2 最小手写 Tool 执行器

```python
def get_weather(city: str) -> str:
    return f"{city}: sunny"

weather_tool = {
    "name": "get_weather",
    "description": "查询指定城市的当前天气",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string"},
        },
        "required": ["city"],
        "additionalProperties": False,
    },
    "handler": get_weather,
}
```

执行器的职责不是直接信任模型参数，而是依次完成 name 路由、参数存在性与类型校验、handler 调用、结果或错误动作封装。建议返回机器可判断结构：

```python
{"ok": True, "action": "success", "output": result}
{"ok": False, "action": "retry_model", "error": {...}}
{"ok": False, "action": "fail_fast", "error": {...}}
```

最小控制规则：未知 Tool name 属于路由/策略错误，通常 `fail_fast`；缺少或类型错误的模型参数通常返回结构化错误并 `retry_model`；可以无歧义规范化的参数才使用 `repair_then_validate`，修复后必须重新校验；handler 的业务异常和外部服务异常需要分开分类，后续专门练习。

下一步练习：补全 `execute_tool(tool, tool_call)`，完成 name 校验、city 参数校验、handler 执行和结构化动作返回。
<!-- learn-agent:evidence:stage-01-ch03-Q1-pass-and-minimal-executor:end -->

<!-- learn-agent:evidence:stage-01-ch03-executor-attempt1-elif-syntax:start -->
## execute_tool attempt 1：业务分支正确，控制流语法待修复

提交已正确实现三种动作语义：未知 name → `fail_fast/unknown_tool`；city 缺失或类型错误 → `retry_model/invalid_arguments`；校验通过 → handler 执行并返回 `success`。

还原聊天转义后执行 `python -m py_compile`，在 `elif "city" not in args ...` 处得到 `SyntaxError: invalid syntax`。原因是 `if` 与 `elif` 之间插入了 `args = ...` 赋值语句；Python 的同一条 `if/elif/else` 链必须连续。

这里适合使用 guard clause（守卫式提前返回）：每个失败条件使用独立 `if` 并立即 return；所有失败检查通过后自然落到成功路径，不需要再写 `elif tool_call["name"] == tool["name"]`。

```python
if tool_call.get("name") != tool["name"]:
    return fail_fast_result

args = tool_call.get("args", {})

if "city" not in args or not isinstance(args["city"], str):
    return retry_model_result

result = tool["handler"](**args)
return success_result
```

补充边界：使用 `tool_call.get("name")` 可把 name 缺失统一归入未知 Tool，而不是意外抛出 KeyError；额外参数和 handler 异常将在后续参数校验课程处理。练习状态：待修改后复检。
<!-- learn-agent:evidence:stage-01-ch03-executor-attempt1-elif-syntax:end -->

<!-- learn-agent:evidence:stage-01-ch03-executor-attempt2-pass-and-tool-map:start -->
## execute_tool attempt 2 通过

还原聊天转义后实际运行成功，三个测试依次返回：

1. 正确 name + 合法 city → `ok=True, action=success`，handler 输出写入 output。
2. 未知 name → `ok=False, action=fail_fast, code=unknown_tool`。
3. city 缺失 → `ok=False, action=retry_model, code=invalid_arguments`。

说明已掌握 guard clause：失败条件分别使用独立 if 并提前 return，所有校验通过后自然进入 handler 成功路径。PowerShell 输出中的中文乱码属于终端编码显示，不影响 Python 返回结构。

遗留边界：条件使用 `tool_call.get("name")`，但错误消息仍读取 `tool_call['name']`；当 name 完全缺失时仍会 KeyError。更稳健的写法是先保存 `requested_name = tool_call.get("name")`，条件和消息统一使用该变量。

## 3.3 普通函数到 LangChain @tool

```python
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气。"""
    return f"{city}: sunny"
```

映射关系：函数名或装饰器配置 → name；docstring → description；类型标注或 args_schema → parameters；函数体 → handler。`@tool` 把普通函数包装为带 Schema 的 Tool 对象，可以直接 `get_weather.invoke({"city": "上海"})`。

```text
手写 Tool dict + execute_tool
              ↓ 框架映射
@tool 生成 Tool 对象 + tool.invoke(args)
```

`model.bind_tools([get_weather])` 只是把 Tool Schema 提供给模型。模型返回 `AIMessage.tool_calls`，其中包含 name、args、id；Harness 执行 Tool 后产生与 id 对应的 ToolMessage，再交回模型。独立使用绑定模型时，bind_tools 本身不等于执行 Tool。

Q2 待回答：普通 Python 函数映射到 @tool 后，四个组成部分分别来自哪里？用户输入到 ToolMessage 的关键数据流是什么？
<!-- learn-agent:evidence:stage-01-ch03-executor-attempt2-pass-and-tool-map:end -->

<!-- learn-agent:evidence:stage-01-ch03-Q2-attempt1-dataflow-gap:start -->
## Q2 attempt 1：对象映射通过，执行数据流待补全

四要素映射正确：函数名 → name；docstring → description；参数类型标注 → parameters Schema；函数体 → handler。

作答的数据流写成“用户输入 → AIMessage.tool_calls → ToolMessage”，遗漏了 Harness 的实际执行阶段。`AIMessage.tool_calls` 只是模型提出的结构化请求，不会自动变成执行结果。完整链路至少是：

```text
用户输入
→ 绑定 Tool Schema 的模型生成 AIMessage.tool_calls{name, args, id}
→ Harness 根据 name 路由 Tool
→ 根据 parameters 校验 args
→ handler(**args) 执行
→ Harness 将结果包装为 ToolMessage(content=result, tool_call_id=id)
```

`tool_call_id` 必须对应原 Tool Call 的 id，使模型能把结果与请求关联。Q2 状态：对象映射通过；输入、执行、输出关键数据流待针对性复检。
<!-- learn-agent:evidence:stage-01-ch03-Q2-attempt1-dataflow-gap:end -->

<!-- learn-agent:evidence:stage-01-ch03-Q2-pass-and-parameter-errors:start -->
## Q2 attempt 2 通过

复检完整写出：用户输入 → AIMessage.tool_calls{name,args,id} → Harness 按 name 路由并根据 parameters 校验 args → handler(**args) → ToolMessage{content,tool_call_id}，且明确 `tool_call_id = tool_call["id"]`。对象映射与关键数据流均通过。

### 用户输入如何变成 AIMessage.tool_calls

`model.bind_tools(tools)` 把 Tool Schema 转换为供应商支持的工具定义并随模型请求提供。LLM 同时读取对话消息与可用 Tool 定义，可能直接回答，也可能生成结构化 Tool Call。LangChain 将供应商返回规范化为 `AIMessage.tool_calls`，常见字段是 name、args、id。name 和 args 是模型根据上下文与 Schema 选择/生成的；id 通常由供应商响应提供，用于请求—结果关联，不是 handler 的业务参数。到这一步仍没有执行 Tool。

```text
用户消息 + Tool Schemas
→ 调用 LLM
→ LLM 决定直接回答或请求 Tool
→ LangChain 规范化为 AIMessage.tool_calls
→ Harness 才开始校验与执行
```

## 3.4 参数错误的分层排查

1. 调用信封：name、args、id 是否存在，args 是否为对象。
2. Schema：必填字段、类型、枚举、范围、额外字段是否符合 parameters。
3. 业务规则：类型正确但内容是否合理，例如 city 为空字符串或不在服务范围。
4. handler/外部依赖：业务异常、超时、限流、权限错误；这不是模型参数 Schema 错误。

处理动作应区分来源：模型生成的可修正参数错误可返回 `retry_model` 并提供精简校验反馈；无歧义规范化可 `repair_then_validate`，修复后必须重新校验；未知/未授权工具通常 `fail_fast`；handler 的瞬时外部错误更适合 `retry_tool`，不要无意义地重新调用模型。

Trade-off：retry_model 提高恢复率但增加 token、延迟和费用；自动修复减少调用成本但可能掩盖模型或上游质量问题；严格失败保护正确性但降低可用性。

Q3 待回答：遇到 Tool 参数错误时，给出可执行排查顺序，并说明至少一个策略 Trade-off。
<!-- learn-agent:evidence:stage-01-ch03-Q2-pass-and-parameter-errors:end -->

<!-- learn-agent:evidence:stage-01-ch03-Q3-pass-and-EX1-start:start -->
## Q3 通过：参数错误排查与重试权衡

作答按调用信封 → Schema 的顺序排查，确认 name、args、id 和 args 容器正常后，在 Schema 层准确识别 city 类型错误与额外字段 unit，并在已定位问题时停止继续排查 handler。选择 `retry_model`，能够说明重新调用 LLM 会增加 token 消耗，满足排查顺序与 Trade-off 验收要求。

生产级补充：重试不能原样重复，应把字段位置、预期类型和额外字段等精简校验反馈交给模型；必须设置最大重试次数。若重复出现相同问题，应检查用户输入、Tool Schema、description、模型/供应商 Tool Calling 兼容性，而不只归因于输入。若存在明确的受控兼容策略，可以删除 unit 后 `repair_then_validate`，但自动修复会掩盖上游质量漂移，修复后必须重新校验。

## 3.5 EX1 入口

必做练习要求在无第三方依赖条件下完成一个 Tool：声明 name、description、parameters、handler；手写执行器复现 name 缺失、city 类型错误、额外字段和 handler 异常；返回机器动作；最后用 `@tool` 可执行伪代码说明框架映射。

验收重点：普通函数到 Tool 契约的映射、参数错误的可执行处理、Tool Call 请求与 ToolMessage 结果边界。
<!-- learn-agent:evidence:stage-01-ch03-Q3-pass-and-EX1-start:end -->

<!-- learn-agent:evidence:stage-01-ch03-EX1-attempt1-runtime-pass-map-followup:start -->
## EX1 attempt 1：运行分支通过，框架映射待复检

还原聊天转义后实际运行成功：call_001 对 city 执行 strip 后返回 success；call_002 因 city 类型错误在额外字段检查前返回 retry_model；call_003 捕获 TimeoutError 并返回 retry_tool。代码实现了 Tool 四要素、调用信封/参数校验、确定性修复、handler 异常分类和机器动作。

`retry_count` 不应由单次 `execute_tool` 自己增加，因为该函数只负责校验和执行一次 Tool Call；外层 Agent/Harness 重试循环在收到 `action=retry_model` 后增加计数、携带校验反馈重新调用 LLM，再把新的 Tool Call 传回执行器。若 `max_retries=2`，retry_count 可表示已经执行的重试次数：0 初次、1 第一次重试后、2 第二次重试后；无效参数且 count>=2 时 fail_fast/retry_exhausted。

框架映射待修正：

```python
@tool
def get_weather_tool(city: str) -> str:
    """查询指定城市的当前天气。"""
    return get_weather(city)
```

默认 Tool name 来自被装饰函数名 `get_weather_tool`，不是函数体内部调用的 `get_weather`。输入标注 `city: str` 生成 parameters Schema；`-> str` 是 handler/Tool 的返回类型说明，不属于输入参数 Schema。若希望 Tool name 是 `get_weather`，可显式配置装饰器名称或直接装饰同名函数。

EX1 状态：参数错误与异常处理 acceptance 通过；普通函数到 @tool 的名称映射待针对性复检。
<!-- learn-agent:evidence:stage-01-ch03-EX1-attempt1-runtime-pass-map-followup:end -->

<!-- learn-agent:evidence:stage-01-ch03-EX1-pass-and-mastery:start -->
## EX1 复检通过与 Chapter 03 掌握判定

EX1 复检正确指出：默认 Tool name 为被装饰函数 `get_weather_tool`；输入标注 `city: str` 生成 parameters Schema；`-> str` 描述 Tool 返回类型。结合 attempt 1 的实际运行证据，EX1 三项 acceptance 全部通过：四要素契约完整；参数与 handler 异常得到复现和机器动作分类；普通函数到 @tool 的映射得到验证。

### 掌握评分（87/100）

- 概念理解：23/25。能解释 name、description、parameters、handler 的职责和失败边界。
- 因果与数据流解释：17/20。最终能完整描述用户输入、AIMessage.tool_calls、Harness 执行、ToolMessage 关联；首次遗漏经复检修正。
- 应用与框架映射：17/20。能映射普通函数到 @tool，并区分被装饰函数名、参数 Schema 和返回标注；名称来源曾需提示复检。
- 调试与故障排查：18/20。实际修复 if/elif 语法错误，运行 success/fail_fast/retry_model/retry_tool 分支，并按层定位参数错误。
- 迁移、边界与 Trade-off：12/15。能区分 retry_model、retry_tool、repair_then_validate、fail_fast，并说明 token 成本和重试边界。

五个维度均达到 60% 下限；Q1、Q2 两道关键题最近有效作答通过；Q3 通过；EX1 通过；未解决关键误解为 0；完整性为 healthy；章节验收契约合法。因此 `mastered=true`。

后续强化：从完整脚手架过渡到无提示 Tool 实现；让所有 retry_model 分支共享最大重试策略；继续练 Tool Registry、超时、副作用与 ToolMessage 大小控制。
<!-- learn-agent:evidence:stage-01-ch03-EX1-pass-and-mastery:end -->

<!-- learn-agent:evidence:stage-01-ch03-repair-then-validate-window-consolidation:start -->
## 3.4.1 Tool 参数错误动作与 `repair_then_validate` 边界

### 四类机器动作

- `success`：调用信封、Schema 与业务前置条件均通过，handler 已成功执行。
- `fail_fast`：错误不可通过重试安全恢复，例如未知或未授权 Tool、重试次数耗尽；立即停止，避免放大错误或副作用。
- `retry_model`：Tool Call 是模型生成的，但参数缺失、类型错误或违反 Schema，且需要模型基于精简校验反馈重新生成；会增加 token、延迟和费用，外层 Harness 必须设置最大次数，不能原样无限重试。
- `retry_tool`：参数已经正确，失败来自 handler 或外部依赖的瞬时问题，例如超时、限流或短暂网络故障；应在幂等性、退避和最大次数约束下重试 Tool，不应无意义地重新调用模型。

### `repair_then_validate` 的严格定义

`repair_then_validate` 表示：**不重新调用 LLM，先按明确规则对参数做确定性修复，然后必须重新执行完整 Schema 校验；只有复检通过才允许调用 handler。**

```text
原始 args
→ 调用信封 / Schema 检查
→ 仅执行无歧义的确定性 repair
→ 重新执行完整 Schema 校验
→ 通过：handler(**args)
→ 仍失败：retry_model 或 fail_fast
```

适用条件必须同时满足：

1. 修复规则由系统明确规定，输出唯一、可预测，不需要猜测用户意图。
2. 修复不创造新的业务信息，也不改变参数语义。
3. 规则有白名单、可测试、可审计；不能用宽泛的自动类型强转掩盖模型或上游质量问题。
4. 修复后重新检查必填、类型、枚举、范围与 `additionalProperties` 等完整 Schema，而不是修完就直接执行。

例如去掉城市字符串首尾的无意义空格，或按系统明确映射把 `celsius` 规范化为 `C`，可能属于受控 repair。缺少城市时默认填“北京”、把数字城市猜成某个真实城市，都是在创造业务信息，不属于 repair。

核心边界：**能转换 ≠ 应该转换。** `str(123)` 虽然能得到 `"123"`，但类型转换成功不能证明它是有效城市，也不能证明符合用户原意，因此 `city=123` 不应自动转成字符串。

### Q3 示例的排查与决策

```python
{
    "name": "get_weather",
    "args": {
        "city": 123,
        "unit": "celsius",
    },
    "id": "call_002",
}
```

按“调用信封 → Schema → 业务规则 → handler/外部依赖”的顺序：`name`、`args`、`id` 与 args 容器先通过；Schema 层发现 `city` 应为字符串却收到整数，以及 `unit` 在 `additionalProperties: false` 下是额外字段。既然 Schema 已失败，就不应继续调用 handler。

- `city=123`：不能无歧义修复，更适合 `retry_model`；把它强转为 `"123"` 违反“能转换 ≠ 应该转换”。
- 额外 `unit`：默认按 Schema 错误反馈给模型并 `retry_model`。只有系统存在明确、受控且已审计的兼容策略时，才可删除该字段或做白名单映射，再进入 `repair_then_validate`；不能删除后跳过复检。
- 若修复或模型重试后参数合法，而 handler 随后发生瞬时超时，动作才转为 `retry_tool`。

这组判定延续最小 Harness 的 guard clause：每一层失败立即返回结构化动作；只有全部守卫通过才进入 handler。
<!-- learn-agent:evidence:stage-01-ch03-repair-then-validate-window-consolidation:end -->

<!-- learn-agent:evidence:stage-01-ch03-handler-object-and-call-boundary:start -->
## 3.7 handler 函数对象与调用边界

在前面四要素的基础上，需要进一步区分“保存可执行能力”和“立即执行函数”：

```python
tool = {
    "name": "get_weather",
    "description": "查询指定城市的当前天气",
    "parameters": {
        "city": {"type": "string"},
    },
    "handler": get_weather,
}
```

`"handler": get_weather` 保存的是函数对象本身，供 Harness 稍后调用；如果写成 `"handler": get_weather()`，会在创建 Tool 时立刻执行函数，并把返回值保存进去，既缺少当次 Tool Call 的参数，也失去了后续可调用能力。真正执行发生在 Harness 收到请求以后：

```python
handler = tool["handler"]
result = handler(**tool_call["args"])
```

职责可分成两个边界：模型主要读取由 `name`、`description`、`parameters` 构成的 Tool Schema，用它选择工具并生成 `name`、`args`、`id`；`handler` 属于程序执行侧，由 Harness 按 `name` 找到 Tool、根据 Schema 校验 `args`，再执行 `handler(**args)`。因此，Tool Call 表达“模型请求调用什么”，handler 定义“程序具体怎么做”。

完整消息对应关系是：模型返回的 `AIMessage.tool_calls` 可以包含一个或多个 `{name, args, id}` 请求；Harness 对每个请求执行并产生一个 `ToolMessage(content=result, tool_call_id=id)`。`tool_call_id` 必须等于原 Tool Call 的 `id`，用于把执行结果准确关联回对应请求。

`model.bind_tools(tools)` 只把 Tool 定义绑定到模型调用，使模型具备生成 Tool Call 的条件；独立调用这个绑定后的模型时，它不会因此自动执行 handler。自动执行必须由外层 Harness / Agent Loop（或具备相应执行节点的 Agent 框架）完成。
<!-- learn-agent:evidence:stage-01-ch03-handler-object-and-call-boundary:end -->
