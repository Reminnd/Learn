# Stage 01 — Q&A Ledger

只记录值得跨窗口检索的重要问题。完整解释归入对应课程笔记。

## Q-20260819-structured-message

- chapter_id: `01`
- topic: `Message 与字符串的边界`
- question: 为什么生产系统通常保留结构化 Message，而不是只保存对话文本字符串？
- conclusion: 结构化 Message 能保留角色、工具调用关联和模型元数据，便于校验、追踪与恢复。
- disposition: `notes`
- promoted_to: `learning/notes/stage-01/01-llm-message-prompt-langchain.md#12-qa-掌握记录`
- mastery_effect: `reinforced`
- status: `verified`

## Q-20260819-prompt-runtime-boundary

- chapter_id: `01`
- topic: `Prompt 构造配置与运行时输入`
- question: 在 `prompt | model` 中，各组件的精确输入和输出是什么？
- conclusion: Prompt 模板在构造阶段保存，运行时接收变量映射并输出包含消息序列的 ChatPromptValue；模型接收该提示值/消息并输出 AIMessage。
- disposition: `bug-book`
- promoted_to: `learning/notes/stage-01/01-llm-message-prompt-langchain.md#12-qa-掌握记录`
- mastery_effect: `needs_review`
- status: `open`

<!-- learn-agent:evidence:stage-01-ch01-Q2b-attempt-2:start -->
## stage-01-ch01-Q2b-attempt-2

- chapter_id: `01-llm-message-prompt-langchain`
- question_id: `Q2`
- attempt: `2`
- topic: `Prompt 与 Chat Model 输入输出数据流`
- conclusion: 能准确表达运行时变量映射 → ChatPromptValue → AIMessage，并区分构造配置与运行时输入。
- dimensions: `概念理解 通过；因果与数据流解释 通过；应用与框架映射 通过`
- acceptance: `原理侧与框架侧对象明确；输入、输出与关键数据流明确`
- mastery_effect: `reinforced`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch01-Q2b-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q3-attempt-1:start -->
## stage-01-ch01-Q3-attempt-1

- chapter_id: `01-llm-message-prompt-langchain`
- question_id: `Q3`
- attempt: `1`
- topic: `Message 历史增长的定位与方案权衡`
- conclusion: 能按历史依赖强度选择窗口、摘要或检索，并说明每种方案的主要代价；需校准非破坏性窗口与按需检索边界。
- dimensions: `因果与数据流解释 通过；调试与故障排查 通过；迁移、边界与 Trade-off 通过`
- acceptance: `给出可执行排查分流；说明多个方案 Trade-off`
- mastery_effect: `reinforced`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch01-Q3-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-3:start -->
## stage-01-ch01-Q2-attempt-3

- chapter_id: `01-llm-message-prompt-langchain`
- question_id: `Q2`
- attempt: `3`
- topic: `Prompt 组件类型与运行输出类型`
- conclusion: 正确识别 AIMessage，但把 ChatPromptTemplate 组件类型误作 prompt 运行输出；需复检 ChatPromptValue。
- dimensions: `概念理解 需复习；因果与数据流解释 需复习；应用与框架映射 需复习`
- acceptance: `输入输出数据流尚未完整通过`
- mastery_effect: `needs_review`
- status: `open`
<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-3:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-4:start -->
## stage-01-ch01-Q2-attempt-4

- chapter_id: `01-llm-message-prompt-langchain`
- question_id: `Q2`
- attempt: `4`
- topic: `Prompt 组件类型与运行输出类型`
- conclusion: 正确区分 ChatPromptTemplate 组件、ChatPromptValue 运行输出与 AIMessage 模型输出。
- dimensions: `概念理解 通过；因果与数据流解释 通过；应用与框架映射 通过`
- acceptance: `原理与框架对象明确；输入、输出及关键数据流明确`
- mastery_effect: `reinforced`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-4:end -->

<!-- learn-agent:evidence:stage-01-ch02-Q1-attempt-1:start -->
## stage-01-ch02-Q1-attempt-1

- chapter_id: `02-structured-output`
- question_id: `Q1`
- attempt: `1`
- topic: `JSON 语法合法与业务数据合法的边界`
- conclusion: json.loads 只保证语法可解析，字段类型和业务内容仍可能不符合下游要求。
- dimensions: `概念理解 通过；因果与数据流解释 通过`
- acceptance: `给出核心因果；指出类型与内容不匹配的失败条件`
- mastery_effect: `reinforced`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch02-Q1-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch02-Q2-attempt-1:start -->
## stage-01-ch02-Q2-attempt-1

- chapter_id: `02-structured-output`
- question_id: `Q2`
- attempt: `1`
- conclusion: `原理侧与框架侧映射正确，输入判断正确；默认输出与 include_raw=True 输出混淆。`
- dimensions: `对象映射通过；数据流基本通过；输出契约待复检`
- acceptance: `未完全满足：需分别说清两种配置的正常输出`
- mastery_effect: `none`
- status: `needs_followup`
<!-- learn-agent:evidence:stage-01-ch02-Q2-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch02-Q2-attempt-2:start -->
## stage-01-ch02-Q2-attempt-2

- chapter_id: `02-structured-output`
- question_id: `Q2`
- attempt: `2`
- conclusion: `默认输出为 Review；include_raw=True 输出为含 raw/parsed/parsing_error 的字典。`
- dimensions: `对象映射通过；输入输出通过；关键数据流通过`
- acceptance: `完全满足`
- mastery_effect: `critical_question_passed`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch02-Q2-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch02-Q3-attempt-1:start -->
## stage-01-ch02-Q3-attempt-1

- chapter_id: `02-structured-output`
- question_id: `Q3`
- attempt: `1`
- conclusion: `通过 errors() 分类定位 missing 等错误，回看输入后选择重试，并指出 token、延迟和费用代价。`
- dimensions: `调试与故障排查通过；边界与 Trade-off 通过`
- acceptance: `完全满足`
- mastery_effect: `reinforced`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch02-Q3-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch02-EX1-attempt-1:start -->
## stage-01-ch02-EX1-attempt-1

- chapter_id: `02-structured-output`
- exercise_id: `EX1`
- attempt: `1`
- syntax_check: `py_compile passed after removing chat escape characters`
- runtime_check: `blocked at import because current Python lacks pydantic; not a learner-code failure`
- acceptance_1: `passed — natural-language output triggers JSONDecodeError path`
- acceptance_2: `passed — missing/literal_error/less_than_equal Schema failures reproduced and classified`
- acceptance_3: `passed — json.loads/Pydantic chain mapped to with_structured_output(Review)`
- result: `passed`
- note_pointer: `stage-01/02-structured-output.md`
<!-- learn-agent:evidence:stage-01-ch02-EX1-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch03-Q1-attempt-1:start -->
## stage-01-ch03-Q1-attempt-1

- chapter_id: `03-tool-basics`
- question_id: `Q1`
- attempt: `1`
- conclusion: `四要素分别承担路由、模型选择提示、参数契约和实际执行；缺失或设计不当会导致不可路由、错选、参数错误或执行错误。`
- dimensions: `概念理解通过；因果与失败边界通过`
- acceptance: `完全满足`
- mastery_effect: `critical_question_passed`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch03-Q1-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch03-Q2-attempt-1:start -->
## stage-01-ch03-Q2-attempt-1

- chapter_id: `03-tool-basics`
- question_id: `Q2`
- attempt: `1`
- conclusion: `四要素映射正确；数据流遗漏 Harness 参数校验、handler 执行和 tool_call_id 关联。`
- dimensions: `对象映射通过；输入输出与关键数据流待复检`
- acceptance: `未完全满足`
- mastery_effect: `none`
- status: `needs_followup`
<!-- learn-agent:evidence:stage-01-ch03-Q2-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch03-Q2-attempt-2:start -->
## stage-01-ch03-Q2-attempt-2

- chapter_id: `03-tool-basics`
- question_id: `Q2`
- attempt: `2`
- conclusion: `完整写出 Tool Call 到 Harness 校验/handler 执行再到 ToolMessage，并正确关联 tool_call_id。`
- dimensions: `对象映射通过；输入输出通过；关键数据流通过`
- acceptance: `完全满足`
- mastery_effect: `critical_question_passed`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch03-Q2-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch03-Q3-attempt-1:start -->
## stage-01-ch03-Q3-attempt-1

- chapter_id: `03-tool-basics`
- question_id: `Q3`
- attempt: `1`
- conclusion: `按信封和 Schema 顺序定位 city 类型错误及额外字段，选择 retry_model 并指出 token 代价。`
- dimensions: `调试与故障排查通过；边界与 Trade-off 通过`
- acceptance: `完全满足`
- mastery_effect: `reinforced`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch03-Q3-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch03-EX1-attempt-1:start -->
## stage-01-ch03-EX1-attempt-1

- chapter_id: `03-tool-basics`
- exercise_id: `EX1`
- attempt: `1`
- runtime: `passed — success/retry_model/retry_tool`
- acceptance_1: `passed — name/description/parameters/handler 均存在并被使用`
- acceptance_2: `passed — 类型、额外字段、空值和 handler 异常有具体分析与代码`
- acceptance_3: `needs_followup — 默认 Tool name 错认成内部 get_weather，而非被装饰函数 get_weather_tool`
- status: `needs_followup`
<!-- learn-agent:evidence:stage-01-ch03-EX1-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch03-EX1-attempt-2:start -->
## stage-01-ch03-EX1-attempt-2

- chapter_id: `03-tool-basics`
- exercise_id: `EX1`
- attempt: `2`
- conclusion: `默认 Tool name=get_weather_tool；city: str 生成参数 Schema；-> str 描述返回类型。`
- acceptance_1: `passed — 四要素在运行代码中存在并使用`
- acceptance_2: `passed — 参数错误和 handler 异常有运行证据`
- acceptance_3: `passed — 普通函数到 @tool 映射复检正确`
- result: `passed`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch03-EX1-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch04-Q1-attempt-1:start -->
## stage-01-ch04-Q1-attempt-1

- chapter_id: `04-tool-registry-engineering`
- question_id: `Q1`
- attempt: `1`
- conclusion: `Registry 统一控制注册、查找与模型暴露，集中承载唯一性和治理能力；临时字典会让同名 Tool 被静默覆盖。`
- causal_chain: `工具增多 → 分散管理和策略不一致 → 统一 Registry；同名 key → 后项覆盖前项 → 错误版本进入运行期。`
- failure_boundary: `缺少 name 唯一性检查时，dict comprehension 不会主动报告冲突。`
- acceptance: `完全满足`
- result: `passed`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch04-Q1-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch04-Q2-attempt-1:start -->
## stage-01-ch04-Q2-attempt-1

- chapter_id: `04-tool-registry-engineering`
- question_id: `Q2`
- attempt: `1`
- correct: `流程顺序正确：Registry 注册和 Policy 筛选 → bind_tools → LLM → AIMessage.tool_calls → ToolNode/Executor → ToolMessage。Registry、bind_tools 与 ToolNode 的职责区分正确。`
- missing_evidence: `尚未逐步明确各层的具体输入与输出，例如 bind_tools 返回绑定工具后的模型、tool_call 包含 name/args/id、ToolMessage 包含 content/tool_call_id。`
- acceptance_1_objects: `passed`
- acceptance_2_io_dataflow: `needs_followup`
- result: `incomplete`
- status: `followup_required`
<!-- learn-agent:evidence:stage-01-ch04-Q2-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch04-Q2-attempt-2:start -->
## stage-01-ch04-Q2-attempt-2

- chapter_id: `04-tool-registry-engineering`
- question_id: `Q2`
- attempt: `2`
- correct: `register 的 Tool 输入、重名报错、LLM 输出 Tool Call、Executor 输出 ToolMessage 的大方向正确。`
- corrections: `list_specs 不是接收新 Tool；bind_tools 返回绑定后的模型而非 Tool；LLM 的直接输出是 AIMessage；ToolMessage 不把请求 args 作为标准结果字段。`
- acceptance_1_objects: `needs_correction`
- acceptance_2_io_dataflow: `needs_correction`
- result: `incorrect`
- status: `recheck_required`
<!-- learn-agent:evidence:stage-01-ch04-Q2-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch04-Q2-attempt-3:start -->
## stage-01-ch04-Q2-attempt-3

- chapter_id: `04-tool-registry-engineering`
- question_id: `Q2`
- attempt: `3`
- conclusion: `正确补全 tools → bound model → AIMessage → ToolCall → result → ToolMessage，并使用正确属性与字段。`
- type_refinement: `AIMessage 是对象；tool_calls 是列表；单个 ToolCall 是字典式对象。`
- acceptance_1_objects: `passed`
- acceptance_2_io_dataflow: `passed`
- result: `passed`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch04-Q2-attempt-3:end -->

<!-- learn-agent:evidence:stage-01-ch04-Q3-attempt-1:start -->
## stage-01-ch04-Q3-attempt-1

- chapter_id: `04-tool-registry-engineering`
- question_id: `Q3`
- attempt: `1`
- correct: `先检查 raw_tools 的 name 并定位重名；选择版本化名称；指出新旧版本共存会使 tools 列表冗长。`
- missing_evidence: `排查顺序只有一步，尚未比较重名 Tool 的来源、Schema、handler、版本和最终暴露结果，也未说明修复后的验证。`
- correction: `Tool name 冲突属于定义/注册层配置问题；版本号应显式写入 Tool name 或 Registry 元数据，不属于 args Schema 校验，也不应靠运行时确定性修复。`
- acceptance_debug_order: `needs_followup`
- acceptance_tradeoff: `partially_passed`
- result: `incomplete`
- status: `followup_required`
<!-- learn-agent:evidence:stage-01-ch04-Q3-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch04-Q3-attempt-2:start -->
## stage-01-ch04-Q3-attempt-2

- chapter_id: `04-tool-registry-engineering`
- question_id: `Q3`
- attempt: `2`
- conclusion: `按原始列表 → 重名来源和字段差异 → 定义层改名 → 重新注册和模型暴露验证进行排查。`
- implementation_boundary: `版本号在进入 Registry 前写入 Tool name；不修改已注册内部对象以免 key/name 不一致。`
- tradeoff_evidence: `结合 attempt 1，版本化会使工具列表冗长并让新旧版本长期共存。`
- acceptance_debug_order: `passed`
- acceptance_tradeoff: `passed`
- result: `passed`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch04-Q3-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch04-EX1-attempt-1:start -->
## stage-01-ch04-EX1-attempt-1

- chapter_id: `04-tool-registry-engineering`
- exercise_id: `EX1`
- attempt: `1`
- runtime_result: `passed — 两个 Tool 注册；get_weather 返回上海: sunny；公开 specs 不含 handler；重复 name 触发 ValueError。`
- acceptance_1_unified_registration: `passed`
- acceptance_2_tool_conflict: `passed`
- acceptance_3_framework_mapping: `passed — 结合本次注释与 Q2 最新有效证据`
- result: `passed`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch04-EX1-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch05-Q1-attempt-1:start -->
## stage-01-ch05-Q1-attempt-1

- chapter_id: `05-agent-loop`
- question_id: `Q1`
- attempt: `1`
- conclusion: `Tool observation 必须回传模型，用于解释、综合、继续决策或终止；否则只能返回未经综合的结果。`
- failure_no_feedback: `ToolMessage content 只是 observation，模型没有生成最终答案。`
- failure_infinite_loop: `重复 Tool Call 导致死循环、token/费用失控或重复副作用。`
- acceptance: `完全满足`
- result: `passed`
- status: `verified`
<!-- learn-agent:evidence:stage-01-ch05-Q1-attempt-1:end -->
