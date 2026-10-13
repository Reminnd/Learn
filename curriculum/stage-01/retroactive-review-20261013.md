# Stage 01 已完成章节新增内容补课（2026-10-13）

> **定位：非canonical的定向补课计划，不是第41章，也不替代任何原有章节。** 它服务于本次用户明确提出的“检查新加内容是否覆盖已学章节，并调整当前学习顺序优先补课”请求。
>
> **版本与证据**：2026-10-13读取GitHub `main` 的 `state.current`、Stage 01第01–04章笔记、Stage 01 Q&A、已有原章节契约以及[范式地图](../agent-paradigm-map.md)、[六个项目案例库](../project-source-casebook.md)后制定。未发现足以自动否定原有mastery的新正式验收条件；补充范式/源码案例是独立知识扩展。
>
> **硬约束**：保持第01–03章已提交mastered证据及成绩不变；不提前给第04章或第05章mastery；不修改Stage 01–14 canonical路由。当前正式章节始终为第04章。补课完成后恢复原第04章4.1的问题，无须重新过此前必做EX/Q&A。

## 一、审计快照与优先级

| 已提交原章节 | 可核实已有证据 | 新增内容实际缺口 | 决策 |
|---|---|---|---|
| Stage 01/01 · LLM/Message/Prompt/Runnable（82/100，已完成） | Prompt构造、Message历史、Runnable `prompt \| model`、数据流及Q&A | **Prompt Chaining、Workflow vs Agent**的显式比较及是否应该引入Agent的判断；已有Runnable基础不等于证明理解范式选型 | **R01：轻量补课**，不重复Message练习 |
| Stage 01/02 · Structured Output（82/100，已完成） | Pydantic、`json.loads/model_validate`、`with_structured_output`、Schema错误定位、真实DeepSeek API调用 | **Python Pydantic vs TypeScript静态类型及运行时AJV/JSON Schema**：跨语言接口边界未见独立验证证据 | **R02：轻量补课**，不重复Pydantic EX1 |
| Stage 01/03 · Tool基础（84/100，已完成） | `name/description/parameters/handler`、原理版`invoke_raw_tool`、`@tool`、`bind_tools`、ToolMessage回填及用户本地测试 | **Tool Calling ≠ ReAct**的概念边界；在真实Python项目中定位工具声明、查找与执行调用链的学习证据不足 | **R03：轻量补课**，不重复原EX1 |
| Stage 01/04 · Tool Registry（进行中） | 当前`4.1`与`L4-CHECK-1 / attempt 1`，已开始统一注册/同名风险 | 新增`KimiToolset`、Kimi Code TS Registry、Adapter等案例 | **随正常第04章教学融合**，不计入“已学完待补” |
| Stage 01/05及后续 | 状态中未标为已完成 | ReAct完整Agent Loop、Plan-and-Execute、Reflection、Multi-Agent/Harness/MCP、Deep Agents等 | **在未来原章节学习**，不作为本次旧章补课 |

> **不做虚假缺口判断**：已学过的内容不重复；某个关键词未在笔记中出现，不必然说明完全不会，只表示尚缺可核验的、针对“新增范式/语言映射”的独立证据。

## 二、3个最小补课任务

每一项均按“**已学知识 → 新范式/语言抽象 → 一处真实函数 → 一个可独立回答的问题**”进行。一次只问一题；问题的第一次答案不在课堂提问前公开。不要求从零重写开源大项目。

### R01 · 第01章：Prompt Chaining与Workflow/Agent边界

- **学习起点**：已学的`chain = prompt | model`和`chain.invoke(inputs)`。
- **新概念**：固定调用顺序的Prompt Chaining是工作流；由LLM动态决定下一步工具或行动才需要Agent。判断是否真的需要Agent，不能以“有LLM就是Agent”为标准。
- **工程对照**：用已有`prompt | model`作为固定链实例；只在理解差异时预览[Pi `agentLoop`](https://github.com/earendil-works/pi/blob/7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6/packages/agent/src/agent-loop.ts)。Pi完整调用链与ReAct正式教学留到第05章。
- **学习目标**：能判断两段需求哪个该使用固定Chain、哪个有理由使用Agent，以及更复杂策略引入的开销。
- **复检题R01**：`A. 用户给文本 → 固定提取标题 → 固定翻译 → 返回。B. 用户提出复杂任务，需要根据每次工具输出决定是检索、调用计算工具还是结束。` 分别优先采用固定工作流还是Agent？为什么？
- **状态记录**：完成题目后在补课记录中写`R01=passed/retry`与回答依据，不自动回溯修改第01章mastery。

### R02 · 第02章：Python Pydantic与TypeScript运行时校验

- **学习起点**：已学`Product.model_validate(...)`、Pydantic错误定位及`with_structured_output`。
- **新概念**：TypeScript的`interface/type`主要用于静态编译期检查；HTTP/模型传入的数据在运行时依然需要AJV/Zod等对数据实际值进行验证；Python Pydantic亦是运行时校验。
- **工程对照**：[Kimi Code `validateToolArgs`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/tool/args-validator.ts)；仅追踪编译validator→校验args→错误返回，先解释新语言语法，不强制写TS。
- **学习目标**：对`price: number`类型声明和外部实际输入`{"price":"abc"}`，能说明运行时风险、正确验证时机以及失败后哪个组件应该拒绝进入业务处理。
- **复检题R02**：一份网络请求在TS中声明`interface Product { price: number }`，但实际收到`{"price":"abc"}`。仅有`interface`能阻止该值流入运行时handler吗？Pydantic或AJV/Zod应该在哪里发挥作用？
- **状态记录**：完成后记`R02=passed/retry`，不修改原Structured Output验收证据。

### R03 · 第03章：Tool Calling与ReAct边界、源码追踪

- **学习起点**：已学手写Tool定义、`@tool`、模型返回`tool_calls`、应用手工`invoke(...)`、`ToolMessage`回填。
- **新概念**：Tool Calling是接口能力/一次工具调用机制；ReAct是可循环的“决定行动→执行→观察→再次决定”的策略，**有Tool Calling并不保证有完整ReAct循环**；模型隐藏推理文本无需也不能被视为一定可见。
- **源码对照**：[Kimi CLI `KimiToolset.add/find`](https://github.com/MoonshotAI/kimi-cli/blob/9ab1286b8fe4e6bcd116949a27ce5e0ac3389c82/src/kimi_cli/soul/toolset.py)（已归档的历史Python源码）；用实际`add`/`find`解释为什么工具定义和查找不同于模型自动执行。完整loop留到第05章。
- **学习目标**：能以模型返回Tool Call后发生的步骤说明“工具描述/注册→模型提出请求→Runtime验证/查找/执行→结果成为下一轮模型输入”的控制权边界。
- **复检题R03**：一个程序只调用`model.bind_tools(...)`取得包含`tool_calls`的消息，但没有执行handler，也没有把ToolMessage放回下一次模型调用。能说它已经完成ReAct Agent吗？缺了哪些关键步骤？
- **状态记录**：完成后记`R03=passed/retry`，不自动更改原第03章成绩。

## 三、推进与恢复规则

- **开始顺序**：R01 → R02 → R03。不同任务不要一次问完。每次先教授新增内容及最小代码/真实源码说明，再给一个问题。
- **可重复**：若回答显示误区，只在对应补课任务内复检；不得随意用它覆盖原章节mastery，除非用户明确要求按正式contract重新考核。
- **补课完成判据**：对每项，能在无标准答案提示下给出因果链和一个边界/代价；真实源码阅读记录需区分“能解释”与“亲自运行/亲手编写”。
- **持久化**：使用manifest解析出的`notes.root`补课记录、`notes.index`索引，教学checkpoint沿现有S03 WAL/batching规则；不要新增Mastery状态字段或第二份学习位置数据库。
- **原位置精确保留**：
  - `stage_id=stage-01`
  - `chapter_id=04-tool-registry-engineering`
  - `chapter_file=curriculum/stage-01/04-tool-registry-engineering.md`
  - `note_pointer=stage-01/04-tool-registry-engineering.md`
  - `last_section=4.1 Tool Registry统一注册与同名工具冲突`
  - `return_to.activity=knowledge_check`
  - `return_to.topic=L4-CHECK-1 / attempt 1`
  - `return_to.next_action=回答重复注册get_price时会使用哪个handler，并说明风险。`
  - `next_action=L4-CHECK-1 attempt1：解释Registry同名工具覆盖并识别风险。`
- **恢复**：R03通过并按运行时持久化策略提交后，从上面原位置恢复第04章，不跳入第05章。原第01–03章的`completed`成员不动。

## 四、与大纲的关系

- [原40章索引](../index.md)：唯一canonical route。
- [Agent范式知识地图](../agent-paradigm-map.md)：新内容详细位置。
- [6项目源码案例库](../project-source-casebook.md)：真实代码、版本快照与局限。
- [Vibe Coding项目源码学习法](../../shared/project-source-learning.md)：讲解、独立说明、运行验证和原创实现等证据级别的区别。
