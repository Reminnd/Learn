# Bug Book（错题本 / 调试本）

## Active Mistakes（当前需要优先复习）

### BUG-20260819-01 — 混淆 Prompt 构造配置与运行时输入

- 日期：2026-08-19
- Stage / Chapter：stage-01 / 01
- 类型：Q&A
- 关联知识点：Prompt、Runnable、输入输出类型
- 状态：open

**错误 / 症状**

把 Prompt 描述为每次同时接收“提示词模板和输入内容”，并把输出笼统称为单个 Message。

**错误理解**

没有区分 Prompt 对象的构造阶段和 `invoke` 运行阶段。

**根因**

对链式调用的数据类型边界还不够精确。

**正确模型 / 修复**

模板在创建 `ChatPromptTemplate` 时保存；`prompt.invoke` 接收变量映射，输出包含格式化消息序列的 `ChatPromptValue`；模型接收提示值/消息并输出 `AIMessage`。

**如何避免再次发生**

阅读链时逐段标注 `组件：输入类型 → 输出类型`，并区分构造时配置与运行时参数。

**验证证据**

- 等待 Q2b 复检。

## Resolved（已解决）

暂无。

<!-- learn-agent:evidence:stage-01-ch01-Q2b-bug-verification:start -->
### BUG-20260819-01 验证更新

- 状态：improving
- 验证证据：Q2b 能准确写出变量映射 → ChatPromptValue → AIMessage，并区分构造阶段与运行阶段。
- 后续：在之后的无提示代码练习中再次验证，届时再标记 resolved。
<!-- learn-agent:evidence:stage-01-ch01-Q2b-bug-verification:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q3-context-policy-boundary:start -->
### BUG-20260819-02 — 把上下文策略误作固定的数据销毁或每轮 I/O

- 日期：2026-08-19
- Stage / Chapter：stage-01 / 01
- 类型：Trade-off
- 状态：open

**错误 / 症状**

认为滑动窗口必须在每次 append 后删除权威历史；认为归档检索需要每轮读取。

**错误模型与根因**

混淆了权威历史存储与单次模型调用的 Context View，也把条件检索误认为固定流水线步骤。

**正确模型 / 修复**

保留权威历史，为每次调用非破坏性地选择上下文；只有意图、缺失信息或策略条件命中时才检索。

**如何避免**

设计时分开标注 storage history、runtime state 和 model context，并为检索声明触发条件。

**验证证据**

等待 EX1 的非破坏性窗口实现验证。
<!-- learn-agent:evidence:stage-01-ch01-Q3-context-policy-boundary:end -->

<!-- learn-agent:evidence:stage-01-ch01-EX1-window-system-duplication:start -->
### BUG-20260820-01 — 窗口合并重复 System Message

- 日期：2026-08-20
- Stage / Chapter：stage-01 / 01
- 类型：Code / Debug
- 状态：open

**错误 / 症状**

短历史被窗口完整覆盖时，system 消息同时进入 system_messages 与 recent_messages，最终出现两次。

**错误模型与根因**

把“固定保留的消息”与“最近窗口消息”直接相加，但两个集合并非互斥。

**正确模型 / 修复**

让 recent_messages 排除 system 角色，或在合并时按身份/ID 去重。

**如何避免**

为上下文选择器测试：长历史、短历史、window_size 大于历史长度、多个 system 消息。

**验证证据**

当前边界测试 system_count=2；等待 EX1 attempt 2 修复。
<!-- learn-agent:evidence:stage-01-ch01-EX1-window-system-duplication:end -->

<!-- learn-agent:evidence:stage-01-ch01-EX1-context-view-verification:start -->
### BUG-20260819-02 验证更新

- 状态：improving
- 验证证据：EX1 attempt 1 的 select_context 返回新列表，运行前后原 history 均为 23 条。
- 后续：修复 system 重复边界后可将非破坏性窗口部分标记 resolved；按需检索仍待后续模块验证。
<!-- learn-agent:evidence:stage-01-ch01-EX1-context-view-verification:end -->

<!-- learn-agent:evidence:stage-01-ch01-EX1-window-system-duplication-resolved:start -->
### BUG-20260820-01 验证更新

- 状态：resolved
- 验证证据：EX1 attempt 2 在 23 条长历史上返回 5 条 context 且原历史不变；在 system + user 的短历史、window_size=4 边界下 short_system_count=1。
- 修复：recent_messages 从非 system 消息集合中选择最后 window_size 条。
<!-- learn-agent:evidence:stage-01-ch01-EX1-window-system-duplication-resolved:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-3-prompt-boundary-regression:start -->
### BUG-20260819-01 验证更新 2

- 状态：open
- 触发：EX1 框架映射填空把 prompt 输出写成 ChatPromptTemplate。
- 正确模型：ChatPromptTemplate 是组件/对象；ChatPromptValue 是该组件 invoke 后的运行数据；ChatModel 输出 AIMessage。
- 后续：用 Q2 attempt 4 同时填写组件类型与运行输出类型，避免只记顺序名词。
<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-3-prompt-boundary-regression:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-4-prompt-boundary-improving:start -->
### BUG-20260819-01 验证更新 3

- 状态：improving
- 验证证据：Q2 attempt 4 同时正确填写 ChatPromptTemplate、ChatPromptValue 与 AIMessage。当前不存在与核心模型冲突的陈述。
- 后续：在下一章或后续无提示代码中间隔复查；该复查不阻塞本章完成。
<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-4-prompt-boundary-improving:end -->

<!-- learn-agent:evidence:bug-structured-output-default-vs-include-raw:start -->
## Structured Output 默认输出与 include_raw 混淆

- 症状：曾认为 `structured_model.invoke(...)` 默认同时返回原始 AIMessage 和结构化结果。
- 错误模型：把 `include_raw=True` 的调试输出当成默认输出。
- 根因：没有区分 Runnable 的两种输出契约。
- 修复：默认 `with_structured_output(Review)` 返回 `Review`；设置 `include_raw=True` 后返回包含 `raw`、`parsed`、`parsing_error` 的字典。
- 避免：看到示例时先检查构造参数，再判断 `invoke()` 的返回类型。
- 状态：已于 Q2 attempt 2 复检解决。
<!-- learn-agent:evidence:bug-structured-output-default-vs-include-raw:end -->

<!-- learn-agent:evidence:bug-python-elif-chain-interrupted-by-assignment:start -->
## if/elif 链被普通语句打断

- 症状：`elif` 行触发 `SyntaxError: invalid syntax`。
- 错误模型：认为只要前一个 if 分支 return，就可以在赋值语句之后继续写 elif。
- 根因：Python 语法要求同一 if/elif/else 链连续；是否 return 不改变语法结构。
- 修复：失败检查改成多个独立 if + 提前 return；成功路径放在所有守卫之后。
- 避免：需要在条件之间计算新变量时，优先使用 guard clause。
- 状态：已于 execute_tool attempt 2 修复，三分支测试通过。
<!-- learn-agent:evidence:bug-python-elif-chain-interrupted-by-assignment:end -->

<!-- learn-agent:evidence:bug-tool-call-request-to-tool-message-gap:start -->
## 从 AIMessage.tool_calls 直接跳到 ToolMessage

- 症状：首次数据流遗漏 Harness 执行阶段。
- 错误模型：把模型提出调用请求与 Tool 执行结果视为自动连续步骤。
- 根因：遗漏 Tool Routing、args 校验、handler 执行和结果封装。
- 修复：显式写出 Harness 按 name 路由、校验 args、执行 handler，并用原 id 创建 ToolMessage。
- 避免：每次看到 tool_calls 都问“谁执行、在哪里校验、结果如何关联”。
- 状态：已于 Q2 attempt 2 复检解决。
<!-- learn-agent:evidence:bug-tool-call-request-to-tool-message-gap:end -->

<!-- learn-agent:evidence:bug-tool-decorated-function-name-vs-inner-handler:start -->
## @tool 默认名称与内部调用函数混淆

- 症状：`@tool def get_weather_tool(...)` 的 name 曾被写成 `get_weather`。
- 错误模型：认为 Tool name 来自函数体内部调用的 handler 名称。
- 根因：没有区分被装饰函数与其内部委托函数。
- 修复：默认 name 来自被 `@tool` 装饰的函数名，即 `get_weather_tool`；输入 `city: str` 生成参数 Schema，`-> str` 描述返回类型。
- 避免：检查装饰器紧接着定义的函数，而不是函数体调用了谁。
- 状态：已于 EX1 attempt 2 复检解决。
<!-- learn-agent:evidence:bug-tool-decorated-function-name-vs-inner-handler:end -->

<!-- learn-agent:evidence:bug-tool-binding-call-result-boundaries:start -->
## Tool 绑定、调用请求与执行结果边界混淆

- 症状：把 `bind_tools()` 的输出写成 Tool 对象；把 `AIMessage.tool_calls` 当成 LLM 的完整直接输出；把请求参数 `args` 写进 ToolMessage 标准结果。
- 错误模型：认为每一步都直接传递或返回 Tool 本身，没有区分配置对象、模型响应和执行结果消息。
- 根因：尚未按对象类型追踪 `bound model → AIMessage → ToolCall → ToolMessage`。
- 修复：`bind_tools` 返回绑定后的模型；模型调用返回 AIMessage；其中 ToolCall 含 name/args/id；执行后 ToolMessage 用 content/tool_call_id 回传并关联请求。
- 避免：对每条箭头都写出变量名、类型和最小字段，不只写动作名称。
- 状态：待 Q2 复检。
<!-- learn-agent:evidence:bug-tool-binding-call-result-boundaries:end -->

<!-- learn-agent:evidence:bug-tool-binding-call-result-boundaries-resolved:start -->
## Tool 绑定、调用请求与执行结果边界复检解决

- 症状：此前混淆 bound model、AIMessage、ToolCall 与 ToolMessage。
- 错误模型：认为 bind_tools 返回 Tool，结果消息继续携带请求 args。
- 根因：未逐箭头追踪变量类型。
- 修复：复检正确写出 `model.bind_tools(tools)`、`AIMessage.tool_calls[0]`、按 name/args 调用以及用 content/id 构造 ToolMessage。
- 避免：为 Agent 数据流中的每个变量标注类型和最小字段。
- 状态：已于 Chapter 04 Q2 attempt 3 解决。
<!-- learn-agent:evidence:bug-tool-binding-call-result-boundaries-resolved:end -->

<!-- learn-agent:evidence:bug-tool-name-conflict-vs-args-schema:start -->
## Tool name 冲突与 args Schema 校验层级混淆

- 症状：发现两个 Tool 同名后，提出通过 Schema 校验和确定性修复加入版本号。
- 错误模型：把 Tool 定义/注册阶段的 name 冲突当成调用阶段的 args 数据问题。
- 根因：未区分 Registry 校验 Tool 元数据与 Executor 校验 tool_call args。
- 修复：在 Tool 声明或注册配置中显式使用 `get_weather_v1` / `get_weather_v2`，或由 Registry 按既定策略拒绝/覆盖；参数 Schema 只校验 city、unit 等调用参数。
- 避免：先判断错误属于定义、注册、选择、参数还是执行层，再选择修复位置。
- 状态：待 Chapter 04 Q3 复检。
<!-- learn-agent:evidence:bug-tool-name-conflict-vs-args-schema:end -->

<!-- learn-agent:evidence:bug-tool-name-conflict-vs-args-schema-resolved:start -->
## Tool name 冲突与 args Schema 层级复检解决

- 症状：此前把版本号修复放入参数 Schema 或运行时确定性修复。
- 错误模型：混淆 Tool 定义/注册元数据与 Tool Call 参数。
- 根因：未先定位错误所在生命周期层。
- 修复：复检将版本化 name 放回原始 Tool 定义，并在重新注册和模型暴露后验证。
- 避免：进入 Registry 前冻结 Tool name；注册后不得让字典 key 与对象 name 分离。
- 状态：已于 Chapter 04 Q3 attempt 2 解决。
<!-- learn-agent:evidence:bug-tool-name-conflict-vs-args-schema-resolved:end -->
