# 代码能力追踪

等级：0 未接触；1 需要大量引导；2 能在提示下完成；3 能独立完成；4 能解释 Trade-off 并做工程设计。

| 知识点 | 看懂代码 | 补全/修改 | 独立实现 | 调试排错 | 工程设计 | 最近证据 | 更新时间 |
|---|---:|---:|---:|---:|---:|---|---|
| LangChain 基础 | 1 | 0 | 0 | 0 | 1 | Q2：能读出 Prompt→Model 数据流，但需提示区分构造配置、运行时输入和 ChatPromptValue | 2026-08-19 |
| Tool / Tool Calling | 0 | 0 | 0 | 0 | 0 | 尚未开始 | - |
| Agent Loop / Runtime | 0 | 0 | 0 | 0 | 0 | 尚未开始 | - |
| LangGraph State / Node / Edge | 0 | 0 | 0 | 0 | 0 | 尚未开始 | - |
| Checkpoint / HITL | 0 | 0 | 0 | 0 | 0 | 尚未开始 | - |
| Context Engineering | 0 | 0 | 0 | 0 | 0 | 尚未开始 | - |
| RAG | 0 | 0 | 0 | 0 | 0 | 尚未开始 | - |
| Planning / Reliability | 0 | 0 | 0 | 0 | 0 | 尚未开始 | - |
| Memory | 0 | 0 | 0 | 0 | 0 | 尚未开始 | - |
| Multi-Agent | 0 | 0 | 0 | 0 | 0 | 尚未开始 | - |
| Agent Harness Engineering | 0 | 0 | 0 | 0 | 0 | 尚未开始 | - |

## 最近能力变化

- 2026-08-19：LangChain 基础“工程设计”从 0 → 1；证据为 Q1 能说明 Message 结构化保存的生产价值，但尚未完成代码实现或独立设计。
- 2026-08-19：LangChain 基础“看懂代码”从 0 → 1；Q2 能识别主要数据流，但输入输出类型仍需引导。

<!-- learn-agent:evidence:stage-01-ch01-Q2b-ability-evidence:start -->
### 2026-08-19 — LangChain 基础证据补充

Q2b 在一次纠正后能准确复述 Prompt → ChatPromptValue → Chat Model → AIMessage 数据流。当前仍保留“看懂代码 = 1”，等待无提示新场景再次成功后再升级。
<!-- learn-agent:evidence:stage-01-ch01-Q2b-ability-evidence:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q3-design-evidence:start -->
### 2026-08-19 — LangChain 基础工程设计 = 2

证据：Q3 能在提示框架下按历史依赖强度选择滑动窗口、摘要和检索，并说明每种方案的代价。尚需通过 EX1 验证代码实现、非破坏性上下文选择和调试能力。
<!-- learn-agent:evidence:stage-01-ch01-Q3-design-evidence:end -->

<!-- learn-agent:evidence:stage-01-ch01-EX1-attempt-1-ability:start -->
### 2026-08-20 — EX1 attempt 1 能力证据

- LangChain 基础看懂代码：2。能解释并正确补全消息追加、历史增长和窗口主路径。
- LangChain 基础补全/修改：2。在语法模板提示下完成前三部分并获得运行证据。
- 独立实现：暂不升级；本次使用了较完整模板。
- 调试排错：暂不升级；system 重复与依赖缺失由老师测试定位。
- 工程设计：保持 2。
<!-- learn-agent:evidence:stage-01-ch01-EX1-attempt-1-ability:end -->

<!-- learn-agent:evidence:stage-01-ch01-EX1-attempt-2-ability:start -->
### 2026-08-20 — EX1 attempt 2 能力证据

在明确根因与修复方向后，正确修改列表推导式和切片顺序，长短历史测试均通过。补全/修改维持 2 并获得强化；调试根因由老师提供，因此调试排错暂不升级。
<!-- learn-agent:evidence:stage-01-ch01-EX1-attempt-2-ability:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-3-ability:start -->
### 2026-08-20 — Q2 attempt 3 能力证据

LangChain 基础看懂代码保持 2，但精确类型边界不稳定：能识别 ChatModel 与 AIMessage，仍会把 ChatPromptTemplate 组件误作 ChatPromptValue 输出。本次不升级或降级，等待同概念复检。
<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-3-ability:end -->

<!-- learn-agent:evidence:stage-01-ch01-mastery-ability-summary:start -->
### 2026-08-20 — Chapter 01 能力小结

- LangChain 基础看懂代码：2。
- 补全/修改：2。
- 独立实现：1；EX1 使用了较完整语法脚手架。
- 调试排错：1；能根据反馈修复边界，但根因主要由老师定位。
- 工程设计：2。

章节知识达到继续学习标准，不等同于已能无提示独立开发；后续章节继续累积独立实现和调试证据。
<!-- learn-agent:evidence:stage-01-ch01-mastery-ability-summary:end -->

<!-- learn-agent:evidence:stage-01-ch02-EX1-attempt-1-ability:start -->
### 2026-08-21 — Chapter 02 EX1 能力证据

- LangChain 基础看懂代码：保持 2。能读懂 JSON 解析、Pydantic 校验和框架映射。
- 补全/修改：保持 2。在完整脚手架下正确补全三类错误策略和映射。
- 独立实现：保持 1。本次主要结构由老师提供，尚不能证明无脚手架实现。
- 调试排错：1 → 2。能根据 `ValidationError.errors()` 的类型对缺失、枚举和范围错误分类，并提出查看日志和重试代价。
- 工程设计：保持 2。能说明重试成本与确定性修复边界。
<!-- learn-agent:evidence:stage-01-ch02-EX1-attempt-1-ability:end -->

<!-- learn-agent:evidence:stage-01-ch03-Q1-tool-design-ability:start -->
### 2026-08-21 — Chapter 03 Q1 Tool 设计证据

- Tool / Tool Calling 工程设计：0 → 1。能解释 name、description、parameters、handler 的职责，并预测缺失或设计不当的失败后果。
- 尚无独立代码与真实执行证据；看懂、补全、独立实现和调试等级等待后续练习。
<!-- learn-agent:evidence:stage-01-ch03-Q1-tool-design-ability:end -->

<!-- learn-agent:evidence:stage-01-ch03-executor-attempt1-ability:start -->
### 2026-08-21 — 最小 Tool 执行器 attempt 1

- Tool / Tool Calling 看懂代码：1。能理解 Tool、Tool Call 和 handler 的关系。
- 补全/修改：1。三种机器动作的业务逻辑正确，但控制流存在 if/elif 语法错误。
- 独立实现与调试暂不升级；等待修改后通过编译和三分支运行测试。
<!-- learn-agent:evidence:stage-01-ch03-executor-attempt1-ability:end -->

<!-- learn-agent:evidence:stage-01-ch03-executor-attempt2-ability:start -->
### 2026-08-21 — 最小 Tool 执行器 attempt 2

- Tool / Tool Calling 看懂代码：1 → 2。能解释 Tool Call、参数、handler 与结构化动作返回。
- 补全/修改：1 → 2。在明确根因后正确改为 guard clause，三分支运行测试通过。
- 独立实现：保持 0；本次使用完整脚手架。
- 调试排错：1。根因由老师定位，能依据反馈完成修复。
- 工程设计：保持 1。已使用 success/retry_model/fail_fast 机器动作。
<!-- learn-agent:evidence:stage-01-ch03-executor-attempt2-ability:end -->

<!-- learn-agent:evidence:stage-01-ch03-Q3-tool-error-design-ability:start -->
### 2026-08-21 — Chapter 03 Q3 参数错误证据

- Tool / Tool Calling 调试排错：保持 1；能按层定位，但尚未通过代码实现验证。
- 工程设计：1 → 2。能选择 retry_model 并说明 token 成本，知道重复失败后需要回查输入。
- 后续通过 EX1 验证额外字段、异常分类与最大重试策略。
<!-- learn-agent:evidence:stage-01-ch03-Q3-tool-error-design-ability:end -->

<!-- learn-agent:evidence:stage-01-ch03-EX1-attempt1-ability:start -->
### 2026-08-21 — Chapter 03 EX1 attempt 1

- Tool / Tool Calling 看懂代码：保持 2。
- 补全/修改：保持 2；在完整脚手架下完成参数与异常分支，实际运行通过。
- 独立实现：保持 0；核心结构由老师提供。
- 调试排错：1 → 2；能实现类型、额外字段、空值、TimeoutError 与 ValueError 分类。
- 工程设计：保持 2；区分 retry_model、retry_tool、fail_fast 和 success。
- 框架映射仍需复检默认 Tool name 来源。
<!-- learn-agent:evidence:stage-01-ch03-EX1-attempt1-ability:end -->

<!-- learn-agent:evidence:stage-01-ch03-mastery-ability-summary:start -->
### 2026-08-21 — Chapter 03 能力小结

- Tool / Tool Calling 看懂代码：2。
- 补全/修改：2。
- 独立实现：0 → 1；已能在完整脚手架下完成综合 Tool，但尚无无提示实现证据。
- 调试排错：2；能修复控制流语法并分类参数与 handler 异常。
- 工程设计：2；能设计机器动作和重试边界。

章节知识达到 mastered，不等同于已经能无提示设计生产级 Tool Registry；下一章继续积累独立实现、超时、副作用与安全证据。
<!-- learn-agent:evidence:stage-01-ch03-mastery-ability-summary:end -->

<!-- learn-agent:evidence:stage-01-ch04-mastery-ability-summary:start -->
### 2026-08-22 — Chapter 04 Tool Registry 能力小结

- Tool / Tool Calling 看懂代码：保持 2。能追踪 Registry、bound model、AIMessage、ToolCall 和 ToolMessage。
- 补全/修改：保持 2。在完整脚手架下正确实现 register、get、list_specs 与冲突测试。
- 独立实现：保持 1；核心结构和测试要求由老师提供。
- 调试排错：保持 2；能按原始定义、重名来源、定义层修复、重新暴露验证定位冲突。
- 工程设计：保持 2；能说明 fail-fast、版本化和受控 override 的边界与成本。

下一阶段需积累无脚手架 Registry/Agent Loop 实现，以及结构校验、并发安全、策略元数据与可观测性证据。
<!-- learn-agent:evidence:stage-01-ch04-mastery-ability-summary:end -->
