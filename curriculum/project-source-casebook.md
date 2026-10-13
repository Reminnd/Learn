# Coding Agent开源项目源码学习案例库（首批6个）

> 建档日期：2026-10-13。用户在对话中提供这6个仓库作为后续源码学习参考。**仓库是公开源码参考，不推断用户为原作者、维护者或独立开发者，也不推断这些仓库全部由用户Vibe Coding完成。**
>
> **定位：案例索引，不是第41章，也不是新Track。** 与[40章课程索引](index.md)、[Agent范式地图](agent-paradigm-map.md)、[AI全栈路线](ai-fullstack-agent-roadmap.md)、[源码学习方法](../shared/project-source-learning.md)配合使用。所有来源均为本轮实际检查过的GitHub仓库/目录/部分源文件；本文件并**未**证明每条端到端执行路径都已完整验证。未修改现有学习状态和mastery。
>
> **使用原则**：当前课程一个知识点 → 在最匹配的仓库选择1个真实文件/函数 → 先追踪最短调用链 → 比较Python/TypeScript/框架实现 → 独立解释一个问题。**不要一次学习6个完整项目，也不要以能下载源码代替掌握。**

## 一、仓库一览与使用优先级

| 编号 | 项目 | 技术语言/主要定位 | 用于什么知识点 | 推荐等级 |
|---|---|---|---|---|
| CC-REV | [`oboard/claude-code-rev`](https://github.com/oboard/claude-code-rev) | TypeScript / Bun | Tool抽象、MCP Tool、恢复源码中的Query/工具调用 | P2（补充研究） |
| CODEX | [`openai/codex`](https://github.com/openai/codex) | Rust（核心）+ TypeScript SDK | 工具注册/路由、跨语言SDK、线程事件、审批/权限 | P1（工程进阶） |
| DEEPSEEK | [`deepseek-ai/deepseek-harness`](https://github.com/deepseek-ai/deepseek-harness) | 以TypeScript / Node.js为主的Monorepo | ReAct式Agent Loop、并行工具调度、插件化、Programmatic Tool Calling与隔离 | P1（Harness与动态工具系统重点） |
| PI | [`earendil-works/pi`](https://github.com/earendil-works/pi) | TypeScript / Node.js | 最小可读的Agent Loop、工具执行、串并行调度、事件流与SDK | P0（TypeScript Agent Loop首选） |
| KIMI-PY | [`MoonshotAI/kimi-cli`](https://github.com/MoonshotAI/kimi-cli) | Python | Pydantic/Python异步Agent、Toolset、KimiSoul循环 | P0（Python → TypeScript桥接） |
| KIMI-TS | [`MoonshotAI/kimi-code`](https://github.com/MoonshotAI/kimi-code) | TypeScript / Node.js | Tool Registry、Schema校验、Executor、状态机、MCP、运行时抽象 | P0（TypeScript Tool工程重点） |

### 必须区分的仓库状态

- **`MoonshotAI/kimi-cli`**：官方README已说明Python仓库归档、无后续维护，由`MoonshotAI/kimi-code`接替。它在学习中负责**Python历史代码对照**，不能作为当前可维护的项目依赖或安全参考。
- **`oboard/claude-code-rev`**：README明确说是source map恢复的第三方源码，不是Anthropic原始仓库，包含shim、fallback和未恢复的原生集成。可看工具抽象，不以其行为推断官方Claude Code的准确实现；默认静态阅读。
- **`deepseek-ai/deepseek-harness`**：官方开发者预览，有破坏兼容性的变更风险；源码与文档需按commit快照阅读。
- **`earendil-works/pi`**：README明确以轻量可扩展为取向，并未默认提供子Agent、Plan Mode或内建访问权限系统。不要把扩展包的能力写成Pi的内建保证。
- **`openai/codex`**：核心代码是Rust；TypeScript目录包含SDK，**学习SDK≠读懂Rust Agent核心**。可先看SDK调用与事件，再按需查看Rust工具分发。
- **`MoonshotAI/kimi-code`**：新版TypeScript Coding Agent，借旧版Python学习概念对照时要比较接口与行为，不应假设重构前后是同一实现。

## 二、已核实的源码切入点

下面的路径使用2026-10-13取得的Git commit SHA，避免后续仓库变化导致误以为实例完全相同。每条仅声明**已经核实的目录、类、函数或模块职责**；“学习目标”是未来教学的追踪任务，而非已经跑通的调用链。

### CC-REV · [oboard/claude-code-rev](https://github.com/oboard/claude-code-rev)

- **状态/限制**：非官方恢复版；source map还原，有shim/fallback；研究参考，不等同Anthropic官方源码
- **版本快照**：分支 `main`，commit [`3b0498a6c684`](https://github.com/oboard/claude-code-rev/commit/3b0498a6c684683161077f3c6c5097c6d37cc882)
- **主要用途**：Tool抽象、MCP Tool、恢复源码中的Query/工具调用
- **源码切入点**：
  - [`src/Tool.ts`](https://github.com/oboard/claude-code-rev/blob/3b0498a6c684683161077f3c6c5097c6d37cc882/src/Tool.ts)：`buildTool`与`findToolByName`：工具定义/查找
  - [`src/QueryEngine.ts`](https://github.com/oboard/claude-code-rev/blob/3b0498a6c684683161077f3c6c5097c6d37cc882/src/QueryEngine.ts)：`QueryEngine`：查询编排的恢复版实现
  - [`src/tools/MCPTool/MCPTool.ts`](https://github.com/oboard/claude-code-rev/blob/3b0498a6c684683161077f3c6c5097c6d37cc882/src/tools/MCPTool/MCPTool.ts)：`MCPTool`：MCP工具封装；关注真实Schema来自何处

### CODEX · [openai/codex](https://github.com/openai/codex)

- **状态/限制**：官方开源；核心运行时主要是Rust，TypeScript SDK是客户端层
- **版本快照**：分支 `main`，commit [`f82e36592278`](https://github.com/openai/codex/commit/f82e36592278a0a782fb0d0fc97e5fa10e832ac2)
- **主要用途**：工具注册/路由、跨语言SDK、线程事件、审批/权限
- **源码切入点**：
  - [`codex-rs/core/src/tools/registry.rs`](https://github.com/openai/codex/blob/f82e36592278a0a782fb0d0fc97e5fa10e832ac2/codex-rs/core/src/tools/registry.rs)：`ToolRegistry`相关工具分发与注册（Rust）
  - [`codex-rs/core/src/tools/router.rs`](https://github.com/openai/codex/blob/f82e36592278a0a782fb0d0fc97e5fa10e832ac2/codex-rs/core/src/tools/router.rs)：`build_tool_call`、`dispatch_tool_call_with_code_mode_result`等分发流程（Rust）
  - [`sdk/typescript/src/codex.ts`](https://github.com/openai/codex/blob/f82e36592278a0a782fb0d0fc97e5fa10e832ac2/sdk/typescript/src/codex.ts)：`Codex.startThread` / `resumeThread`：SDK入口
  - [`sdk/typescript/src/thread.ts`](https://github.com/openai/codex/blob/f82e36592278a0a782fb0d0fc97e5fa10e832ac2/sdk/typescript/src/thread.ts)：`Thread.runStreamed`：异步事件迭代与线程接口

### DEEPSEEK · [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)

- **状态/限制**：官方开发者预览；everything-is-a-plugin架构，兼容性可能变化
- **版本快照**：分支 `master`，commit [`d74326738864`](https://github.com/deepseek-ai/deepseek-harness/commit/d743267388641bc76f17c45ce8b4c231aed1d32c)
- **主要用途**：ReAct式Agent Loop、并行工具调度、插件化、Programmatic Tool Calling与隔离
- **源码切入点**：
  - [`packages/core/agent-loop/src/agent.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/agent-loop/src/agent.ts)：`ReactLoopAgent`：轮次/步骤驱动
  - [`packages/core/agent-loop/src/tool-calls.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/agent-loop/src/tool-calls.ts)：`executeToolCalls`：工具调度、并行/独占与取消
  - [`packages/core/tools/src/schema.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/tools/src/schema.ts)：工具Schema与运行时类型校验
  - [`packages/ptc-runtime/ptc-runtime-node/src/process.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/ptc-runtime/ptc-runtime-node/src/process.ts)：`runNodeMain`：独立Node子进程执行入口
  - [`packages/ptc-runtime/ptc-runtime-node/README.zh.md`](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/ptc-runtime/ptc-runtime-node/README.zh.md)：官方包级文档：执行隔离与限制

### PI · [earendil-works/pi](https://github.com/earendil-works/pi)

- **状态/限制**：开源Pi发行仓库；简约可扩展；不默认提供权限系统/内置子Agent与Plan Mode
- **版本快照**：分支 `main`，commit [`7d75a0e3eb27`](https://github.com/earendil-works/pi/commit/7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6)
- **主要用途**：最小可读的Agent Loop、工具执行、串并行调度、事件流与SDK
- **源码切入点**：
  - [`packages/agent/src/agent-loop.ts`](https://github.com/earendil-works/pi/blob/7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6/packages/agent/src/agent-loop.ts)：`agentLoop` / `runAgentLoop` / `runToolCall`：完整调用链
  - [`packages/agent/src/types.ts`](https://github.com/earendil-works/pi/blob/7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6/packages/agent/src/types.ts)：`AgentLoopConfig`、`AgentTool`、`ToolExecutionMode`：类型契约
  - [`packages/agent/src/agent.ts`](https://github.com/earendil-works/pi/blob/7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6/packages/agent/src/agent.ts)：`Agent`：状态与消息队列
  - [`packages/coding-agent/docs/extensions.md`](https://github.com/earendil-works/pi/blob/7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6/packages/coding-agent/docs/extensions.md)：扩展机制（不要误认为内置多Agent）

### KIMI-PY · [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli)

- **状态/限制**：官方历史Python版本；已归档，只用于源码对照，不作为新项目依赖
- **版本快照**：分支 `main`，commit [`9ab1286b8fe4`](https://github.com/MoonshotAI/kimi-cli/commit/9ab1286b8fe4e6bcd116949a27ce5e0ac3389c82)
- **主要用途**：Pydantic/Python异步Agent、Toolset、KimiSoul循环
- **源码切入点**：
  - [`src/kimi_cli/soul/toolset.py`](https://github.com/MoonshotAI/kimi-cli/blob/9ab1286b8fe4e6bcd116949a27ce5e0ac3389c82/src/kimi_cli/soul/toolset.py)：`KimiToolset.add` / `find`：Python工具注册与查找
  - [`src/kimi_cli/soul/kimisoul.py`](https://github.com/MoonshotAI/kimi-cli/blob/9ab1286b8fe4e6bcd116949a27ce5e0ac3389c82/src/kimi_cli/soul/kimisoul.py)：`KimiSoul._agent_loop`：Python Agent运行循环
  - [`src/kimi_cli/soul/agent.py`](https://github.com/MoonshotAI/kimi-cli/blob/9ab1286b8fe4e6bcd116949a27ce5e0ac3389c82/src/kimi_cli/soul/agent.py)：`Agent`与运行上下文装配

### KIMI-TS · [MoonshotAI/kimi-code](https://github.com/MoonshotAI/kimi-code)

- **状态/限制**：当前官方继任实现；TypeScript；不能假设与归档Python版逐行等价
- **版本快照**：分支 `main`，commit [`afd95f64a544`](https://github.com/MoonshotAI/kimi-code/commit/afd95f64a5444b649a4cc33504513bf88e4c54ba)
- **主要用途**：Tool Registry、Schema校验、Executor、状态机、MCP、运行时抽象
- **源码切入点**：
  - [`packages/agent-core-v2/src/agent/toolRegistry/toolRegistry.ts`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/agent/toolRegistry/toolRegistry.ts)：`IAgentToolRegistryService`：`register`、`resolve`、`list`契约
  - [`packages/agent-core-v2/src/tool/args-validator.ts`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/tool/args-validator.ts)：`compileToolArgsValidator` / `validateToolArgs`：AJV/JSON Schema运行时校验
  - [`packages/agent-core-v2/src/agent/toolExecutor/toolScheduler.ts`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/agent/toolExecutor/toolScheduler.ts)：`ToolScheduler.add`：并行调用与访问冲突协调
  - [`packages/agent-core-v2/src/agent/loop/loop.ts`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/agent/loop/loop.ts)：Loop契约、停止条件及事件接口
  - [`packages/agent-core-v2/src/mcpCore/connection-manager.ts`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/mcpCore/connection-manager.ts)：`McpConnectionManager`：连接状态/传输/重连边界
  - [`packages/agent-core-v2/src/runtime/runtime.ts`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/runtime/runtime.ts)：`Runtime`/`RuntimeLease`：运行时能力契约


## 三、映射到Learn 40章及四阶段AI全栈路线

| 当前或后续课程位置 | 本轮先看哪个源文件 | 只追踪一个问题 | 暂不要求 |
|---|---|---|---|
| **Stage 01/03–04** Tool Calling/Registry | [Kimi Python `toolset.py`](https://github.com/MoonshotAI/kimi-cli/blob/9ab1286b8fe4e6bcd116949a27ce5e0ac3389c82/src/kimi_cli/soul/toolset.py) → [Kimi TS `toolRegistry.ts`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/agent/toolRegistry/toolRegistry.ts) → [TS `args-validator.ts`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/tool/args-validator.ts) | 由tool名称/Schema如何找到handler，怎样把未知参数拒绝掉？ | 重写两个仓库的全部工具 |
| **Stage 01/05** Agent Loop / ReAct | [Pi `agent-loop.ts`](https://github.com/earendil-works/pi/blob/7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6/packages/agent/src/agent-loop.ts) ↔ [Kimi Python `kimisoul.py`](https://github.com/MoonshotAI/kimi-cli/blob/9ab1286b8fe4e6bcd116949a27ce5e0ac3389c82/src/kimi_cli/soul/kimisoul.py) | 模型返回toolCall后，谁执行工具、如何拼回结果并结束循环？ | 对照所有框架和多Agent系统 |
| **Stage 02** State、Node、Routing | [Pi `agent.ts`](https://github.com/earendil-works/pi/blob/7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6/packages/agent/src/agent.ts) 与 [Kimi Code `loop.ts`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/agent/loop/loop.ts) | 谁持有状态，下一步如何决策，如何处理取消？ | 只凭目录名认定完整状态机 |
| **Stage 05** Planning、Verification | [DeepSeek `plan-mode`](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/plan/plan-mode/src/client.ts)，再对照现有规划函数 | 区分Plan Mode与完整Plan-and-Execute；计划如何进入执行？ | 强行要求论文式ReWOO/ToT实现 |
| **Stage 07** Multi-Agent、Handoff | [Codex `multi_agent_tool.rs`](https://github.com/openai/codex/blob/f82e36592278a0a782fb0d0fc97e5fa10e832ac2/codex-rs/core/src/tools/multi_agent_tool.rs)，对照Kimi Code子Agent组件 | 谁下发任务、交接控制权、汇总结果？ | 假设Pi开箱自带Supervisor |
| **Stage 09** Harness & Adapter | [DeepSeek `ReactLoopAgent`](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/agent-loop/src/agent.ts) + [Kimi `Runtime`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/runtime/runtime.ts) | Agent策略、工具、runtime、session/插件之间边界如何划分？ | 理解每个插件的内部实现 |
| **Stage 10** MCP | [Kimi `McpConnectionManager`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/mcpCore/connection-manager.ts) + [恢复版 `MCPTool`](https://github.com/oboard/claude-code-rev/blob/3b0498a6c684683161077f3c6c5097c6d37cc882/src/tools/MCPTool/MCPTool.ts) | MCP工具如何发现、封装、调用及处理连接异常？ | 把非官方恢复模块当规范 |
| **Stage 12** Sandbox/权限 | [DeepSeek PTC Node进程入口](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/ptc-runtime/ptc-runtime-node/src/process.ts) 与 [包级说明](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/ptc-runtime/ptc-runtime-node/README.zh.md) | 子进程如何隔离、超时和限制输出？什么必须交由宿主沙箱保障？ | 在宿主机直接执行模型写的任意代码 |
| **Stage 13+** API与实时事件 | [Codex TypeScript SDK `Thread`](https://github.com/openai/codex/blob/f82e36592278a0a782fb0d0fc97e5fa10e832ac2/sdk/typescript/src/thread.ts) | SDK如何返回异步事件？API/Agent Runtime边界在哪里？ | 把CLI SDK误当成FastAPI业务后端 |

**FastAPI、数据库、鉴权、业务服务**并非这些Coding Agent CLI仓库的主要优势。相应章节仍应使用现有Learn最小练习、用户自选真实业务项目，或方案B的独立Python服务进行学习；不能仅靠阅读上述6个仓库就宣称掌握企业后端。

## 四、当前最近章节建议从哪里切入

结合对话中已完成的Python Tool Registry练习，**下一次需要真实源码示例时优先用两个文件**：

1. **Python侧**：[Kimi CLI `KimiToolset`](https://github.com/MoonshotAI/kimi-cli/blob/9ab1286b8fe4e6bcd116949a27ce5e0ac3389c82/src/kimi_cli/soul/toolset.py)：定位`add`、`find`，对照自己的字典式Tool Registry，分析为什么有运行时封装。
2. **TypeScript侧**：[Kimi Code `IAgentToolRegistryService`](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/agent/toolRegistry/toolRegistry.ts)：看`register`与`resolve`签名，再到[AJV参数校验](https://github.com/MoonshotAI/kimi-code/blob/afd95f64a5444b649a4cc33504513bf88e4c54ba/packages/agent-core-v2/src/tool/args-validator.ts)中确认`compileToolArgsValidator`及`validateToolArgs`的职责。

**一个跨语言练习问题**：用户传入一个未注册的工具名，或传入错误类型的参数，哪一层负责拒绝？如果在Python用Pydantic、TypeScript用AJV，会有哪些不同？到独立回答这一问题再做下一步。

之后到Agent Loop章，优先阅读[Pi的`agentLoop` → `runAgentLoop` → `runToolCall`](https://github.com/earendil-works/pi/blob/7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6/packages/agent/src/agent-loop.ts)；它更适合从Python迁移到TypeScript。先看短调用链，再深入DeepSeek完整插件式Harness。

## 五、把案例用于方案B：TypeScript Gateway + Python Executor

建议的组合（**学习参考，不代表直接复制现有代码**）：

- **Gateway Tool Contract**：参照Kimi Code的TypeScript接口、AJV运行时校验，以及Codex TypeScript SDK的`runStreamed`事件暴露方式。
- **Agent Loop**：参照Pi的完整事件/工具调用循环与Kimi Python归档实现，形成自己能解释的Python → TypeScript对照。
- **工具执行/并发与取消**：参照DeepSeek的`executeToolCalls`和Kimi Code的`ToolScheduler`；后者有显式的资源访问约束，不要简单理解为`Promise.all`。
- **隔离执行**：参考DeepSeek的PTC Node包及安全说明来理解安全边界；**方案B首版是Python Executor**，不能拿Node实现直接当Python沙箱替代品。
- **运行时模块化**：参照Pi的薄Agent Core与DeepSeek的插件化设计，比较抽象复杂度，按第一版实际规模选择，不必照搬大型框架。

### 借助真实工程学习的使用约束

- 教师每次只选择**当前知识点相关的1～2个仓库**，先核对当时的代码及commit，讲解真实存在的函数。未验证的源码结构不得编造。
- 各项目仅是用户选择的**参考源码案例**；以后如果给出个人Vibe Coding项目或其Fork，再把实际项目的某个函数与上述参考实现连成学习卡，且不改变其作者归属记录。
- 按“看过 → 能讲清 → 亲自验证 → 独立改写”分别描述掌握证据；**无需把每个项目从零敲一遍**，也不以AI生成代码数量决定能力等级。
- 不为学习随意运行不可信CLI安装脚本、动态代码执行器，尤其不在缺失隔离时运行任意生成代码。优先静态阅读、已有测试与可信最小样例。
- 原40章课程的先修、必做EX、Q&A和mastery门槛继续有效；案例库**不能**更改或代替它们。

## 六、仓库更新/失效时的刷新规则

本文中的commit链接可固定回到已核对的版本；教学需要最新行为时，再读取新HEAD、比较相关文件变化。归档仓库保留为历史对照，不用旧API指导新项目部署。源码迁移、删除或架构大改后，记录新路径与差异，不将旧断言默认为新版本事实。
