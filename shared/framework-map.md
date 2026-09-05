# 原理与框架映射速查

> 当前章节需要比较“手写原理版 vs 框架版”时按需读取。

| 原理能力 | LangChain | LangGraph | Deep Agents / Harness |
|---|---|---|---|
| Model / Message | Chat Model / Messages | Node 内调用模型 | Model policy |
| Structured Output | Pydantic / structured output | State + structured node output | Runtime validation |
| Tool | `@tool` / tool binding | ToolNode / Graph routing | Tool registry / permission / sandbox |
| State | 应用自行维护 | State / Reducer | Runtime state model |
| Agent Loop | Agent abstraction | Graph execution | Harness runtime |
| Routing | Runnable / model decision | Conditional Edge | Supervisor / policy routing |
| Persistence | 应用层 | Checkpointer / Store | Durable runtime |
| HITL | 应用层控制 | Interrupt / Resume | Approval policy |
| RAG | Loader / Splitter / Retriever | Retrieval node | Context engine |
| Memory | Memory / Store patterns | Store / State / persistence | Memory policy |
| Multi-Agent | Agent as Tool 等 | Graph orchestration | Supervisor / Subagent |
| Observability | LangSmith callbacks/tracing | Graph trace | OTel / eval / audit |
