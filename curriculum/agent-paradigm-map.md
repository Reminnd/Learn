# Agent范式、软件设计模式与40章课程映射

> **定位**：这是 [课程索引](index.md) 的配套知识地图，不是新的课程路线、Track、章节或 mastery 契约。Stage 01–14的40章、先修条件与已提交学习位置均不改变。
>
> **学习原则**：先理解“问题 → 控制流/数据流 → 方案的代价”，再辨别具体范式、框架和代码。范式不是函数名；一个工程也未必采用与论文同名的完整实现。P0/P1/P2是**补充知识优先级**，不是课程阶段，也不能代替章节验收。

## 0. 概念分层：避免把所有东西叫“范式”

- **推理/行动策略（agent strategy）**：ReAct、Plan-and-Execute、ReWOO、Reflexion、Tree of Thoughts、LATS；说明模型如何决定下一步。
- **工作流/协作模式（workflow/orchestration）**：Prompt Chaining、Routing、Parallelization、Evaluator-Optimizer、Supervisor/Orchestrator-Workers、Handoff；说明调用、执行和交接如何组织。
- **增强能力（capability）**：Tool Calling、RAG/Agentic RAG、Memory、HITL、Context Engineering；并不与ReAct互斥。
- **运行时与协议（runtime/protocol）**：Agent Loop、LangGraph、FastAPI、MCP、SSE、Gateway、Sandbox；是实现或连接机制，不等价于推理范式。
- **软件工程设计模式（software design patterns）**：Strategy、Adapter、Factory、State Machine、Observer/事件驱动、依赖注入、Repository；是可测试和可替换的模块组织方式。

**特别说明**：经典ReAct论文使用交错的推理和工具行动轨迹；在真实产品中，学习者主要观察**工具选择、参数、调用结果、状态变化与停止条件**，不要把能拿到模型隐藏推理文本当作技术前提。原生function/tool calling可以实现ReAct式交互，但二者概念不同。

## 1. Agent范式与原有课程的逐章映射

| 优先级 | 范式或模式 | 在原课程中结合的章节 | 核心对照（真实工程要看什么） |
|---|---|---|---|
| P0 | Workflow vs Agent | [Stage 01/05 Agent Loop](stage-01/05-agent-loop.md)；[Stage 02/03 Routing](stage-02/03-edge-routing.md) | 代码固定执行路径 vs 模型动态选择下一步；何时不必做Agent |
| P0 | ReAct（Reason + Act） | [Stage 01/05 Agent Loop](stage-01/05-agent-loop.md) | LLM输出工具调用→执行→观察结果→下一轮；终止/轮数限制 |
| P0 | 原生Tool Calling + Tool Registry | [Stage 01/03 Tool](stage-01/03-tool-basics.md)；[Stage 01/04 Registry](stage-01/04-tool-registry-engineering.md) | schema校验→路由→handler→tool result→模型；与ReAct策略区别 |
| P0 | Prompt Chaining（串行链） | [Stage 01/01 Runnable](stage-01/01-llm-message-prompt-langchain.md)；[Stage 02/02 Node](stage-02/02-node.md) | 固定步骤、输入输出契约、失败停止 |
| P0 | Routing（规则/模型/混合路由） | [Stage 02/03](stage-02/03-edge-routing.md)；[Stage 07/01](stage-07/01-routing-intent.md) | 条件分支、兜底、误路由处理 |
| P0 | Plan-and-Execute（规划—执行） | [Stage 05/01 Planning](stage-05/01-planning.md)；[Stage 05/03 Replan](stage-05/03-verification-replan.md) | Planner→任务列表/依赖→Executor→进度/验证；与ReAct的调用成本对比 |
| P0 | Verification + Reflection / Evaluator-Optimizer | [Stage 05/03](stage-05/03-verification-replan.md)；[Stage 11/02 Eval](stage-11/02-evaluation.md) | evaluator反馈→修改/重新规划→有界停止；外部测试与模型自评的可信度区别 |
| P1 | Parallelization（fan-out/fan-in） | [Stage 07/03](stage-07/03-parallel-handoff-synthesis.md) | 子任务独立性、并发限制、聚合和错误传播 |
| P1 | Supervisor / Orchestrator-Workers | [Stage 07/02](stage-07/02-supervisor-subagent.md)；[Stage 07/03](stage-07/03-parallel-handoff-synthesis.md) | 调度者如何拆分/委派；与固定并行有何不同 |
| P1 | Agent as Tool / Handoff | [Stage 07/02](stage-07/02-supervisor-subagent.md)；[Stage 07/03](stage-07/03-parallel-handoff-synthesis.md) | 控制权/上下文/权限由谁拥有；工具返回与正式移交的区别 |
| P1 | RAG → Agentic RAG（动态检索） | [Stage 04/01](stage-04/01-rag-foundation.md)；[Stage 04/02](stage-04/02-retrieval-quality.md) | 固定检索链 vs Agent决定何时检索、重检；先验证检索质量 |
| P1 | Memory / Context / Compaction | [Stage 03 Context](stage-03/README.md)；[Stage 06 Memory](stage-06/README.md) | 短期状态、持久记忆、检索与压缩，避免把每段历史塞回prompt |
| P1 | Human-in-the-Loop（HITL） | [Stage 02/05](stage-02/05-human-in-the-loop.md)；[Stage 12/02](stage-12/02-permission-sandbox.md) | Interrupt/Resume、审批前后状态校验、权限隔离 |
| P1 | Deep/Long-horizon Agent + Workspace | [Stage 08](stage-08/README.md)；[Stage 09](stage-09/README.md) | 任务拆解、持久工作区、子Agent、工具权限与预算 |
| P1 | Harness + MCP + Tool Protocol | [Stage 09 Harness](stage-09/README.md)；[Stage 10 MCP](stage-10/README.md) | 模型策略/工具协议/进程执行/事件流各自的边界 |
| P2 | ReWOO | [Stage 05/01](stage-05/01-planning.md)（比较项） | 规划与观察解耦；减少回合开销的条件与代价 |
| P2 | Reflexion | [Stage 05/03](stage-05/03-verification-replan.md)；[Stage 06](stage-06/README.md)（比较项） | 基于反馈的语言反思存储及后续尝试；区别于普通单轮自我修改 |
| P2 | Tree of Thoughts（ToT）、LATS | [Stage 05](stage-05/README.md)（研究拓展） | 多路径探索、评分/搜索、分支成本；默认不要求生产实现 |

**先学P0，再以真实项目需要引入P1；P2优先阅读原理与工程对照，不强制为了覆盖术语编写完整复刻。** 工程中的ReAct式调用通常不要求暴露模型私有的内部推理过程。

## 2. 软件工程模式：以Python、TypeScript双语言做代码对照

| 优先级 | 工程模式 / 核心概念 | Python侧 | TypeScript侧 | 对应阶段 |
|---|---|---|---|---|
| P0 | Interface/Contract与运行时校验 | `Protocol` / `ABC`、Pydantic | `interface` / `type` + Zod | Stage 01 Tool、补充路线阶段2 |
| P0 | Strategy + Adapter（可替换执行器） | `Executor`协议+不同handler | `ExecutorAdapter` / `WorkerAdapter` | Stage 09 Harness、动态工具项目 |
| P0 | Registry / Factory + Dependency Injection | Tool Registry、依赖注入 | 工厂/注册表、依赖注入 | Stage 01 Tool Registry、Stage 09 |
| P0 | State Machine（状态机） | Enum状态+受控转换 | Discriminated Union+状态转换 | Stage 02 State、Stage 09 Runtime |
| P0 | Async + Event-driven（异步事件） | `asyncio` / `async def` | `Promise` / `async-await` / Event | Stage 02执行、补充路线阶段2/3 |
| P0 | Testing / Fake / Contract Test（测试替身与契约） | pytest、FastAPI TestClient | Node test/Vitest、Zod契约测试 | 所有阶段均贯穿 |
| P1 | Observer / Pub-Sub / SSE事件流 | async generator / EventStream | stream / EventEmitter / SSE | 补充路线阶段3/4、Stage 11 |
| P1 | Repository / Unit of Work / Transaction | SQLAlchemy/SQL事务 | ORM/数据库事务 | Stage 13 FastAPI与持久化 |
| P1 | Idempotency / Retry / Cancellation | 幂等键、重试上界、取消传播 | AbortSignal、幂等键、取消传播 | Stage 05可靠性、阶段3/4 |
| P2 | CQRS / Outbox / 分布式Saga | 规模确有需要再学 | 规模确有需要再学 | Stage 13分布式运行时（拓展） |

注意：TypeScript类型检查在运行时会消失，`interface`不是请求数据校验；Pydantic和Zod都可以用于**运行时校验**。不要因为要学习一个设计模式就强行把简单代码抽象成多层工厂。

## 3. 推荐的“同一个知识点”学习证据

1. **概念**：用自己的话解释问题、控制流、适用范围及不适用场景。
2. **最小原理**：用几十行以内的Python伪代码/小例子理解核心接口或函数；需要时对照TypeScript写法。
3. **真实项目定位**：在学习者提供且可访问的仓库中定位**实际存在的**入口函数、执行函数、状态写入点、外部调用点和测试；未提供代码时不猜路径。
4. **调用链追踪**：记录`入口 → 参数校验 → 业务/策略 → 工具或执行器 → 结果/错误 → 返回`，明确对象状态和异步边界。
5. **问题分析**：以真实调用场景比较至少一种替代设计、失败路径及Trade-off，确认当前模式是否真的存在，而非按文件名贴标签。
6. **掌握验证**：优先让学习者解释一小段源代码的输入/输出、定位错误或推断修改影响；可选择增加小测试/最小改动，但**不要求先亲手写完整项目**。
7. **证据区分**：`observed`（只看到源码）、`explained`（能独立讲清）、`verified`（运行测试/亲自验证）、`authored`（独立编写并验证）。不得以AI生成的代码、项目运行成功或阅读过源码自动认定为`authored`或`mastered`。

具体操作模板见 [真实项目源码映射学习法](../shared/project-source-learning.md)。该法用于**增强**原课程练习，不私自修改章节EX/Q&A/mastery要求。

## 4. 与四阶段AI全栈路线的关联

| 补充路线阶段 | 重点范式 | 优先寻找的函数和模块 |
|---|---|---|
| ① Python Agent＋FastAPI | ReAct、Tool Calling、Routing、基本Chaining | tool decorator/schema、注册表、Agent Loop、路由处理器、FastAPI endpoint |
| ② TypeScript＋React＋Node.js | Adapter、Strategy、状态机、事件驱动 | Zod schema、接口/adapter、Promise、worker入口、前端异步状态 |
| ③ 前后端Agent产品集成 | Handoff、事件流、Agent/Workflow边界 | HTTP调用、SSE事件、取消、错误传播、UI状态同步 |
| ④ 后端工程化与验证 | Evaluator-Optimizer、Reflection、可靠性、持久化与安全 | verifier、幂等处理、数据库事务、权限审批、测试和部署入口 |

原四阶段路线和工程载体：[AI全栈与Agent产品开发补充学习路线](ai-fullstack-agent-roadmap.md)。

## 5. 官方/原始资料（用于按需查证，不要求先全文啃论文）

- ReAct（ICLR 2023）：https://arxiv.org/abs/2210.03629
- Anthropic，Building effective agents：https://www.anthropic.com/engineering/building-effective-agents
- Anthropic，工作流模式（2026）：https://claude.com/resources/articles/common-workflow-patterns-for-ai-agents-and-when-to-use-them
- LangChain，Plan-and-Execute/LLMCompiler/ReWOO对照：https://www.langchain.com/blog/planning-agents
- ReWOO：https://arxiv.org/abs/2305.18323
- Reflexion：https://arxiv.org/abs/2303.11366
- Tree of Thoughts：https://arxiv.org/abs/2305.10601
- LATS：https://arxiv.org/abs/2310.04406
- LangChain/LangGraph官方学习目录：https://docs.langchain.com/oss/python/learn

查阅实时API前，以官方最新文档与项目实际版本为准；历史论文用来理解思想，不代表现在应直接使用论文中的旧API。
