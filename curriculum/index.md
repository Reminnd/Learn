# 课程索引

> 本文件是 40 个章节顺序与 Track 归属的唯一 canonical route。定位时不要把所有章节正文同时读入上下文。

## Core Path

Stage 01–09，共 29 章。

### [Stage 01 — LangChain 与 Agent 基础](stage-01/README.md)

1. [`stage-01/01-llm-message-prompt-langchain.md`](stage-01/01-llm-message-prompt-langchain.md)
   - LLM、Message、Prompt、Runnable 与 LangChain 心智模型
2. [`stage-01/02-structured-output.md`](stage-01/02-structured-output.md)
   - Pydantic、JSON Schema、Structured Output
3. [`stage-01/03-tool-basics.md`](stage-01/03-tool-basics.md)
   - Tool 原理、LangChain `@tool`、Tool Calling
4. [`stage-01/04-tool-registry-engineering.md`](stage-01/04-tool-registry-engineering.md)
   - Tool Registry、校验、超时、重试、副作用
5. [`stage-01/05-agent-loop.md`](stage-01/05-agent-loop.md)
   - Agent Loop 原理与 LangChain/LangGraph Agent

### [Stage 02 — LangGraph 核心](stage-02/README.md)

1. [`stage-02/01-state.md`](stage-02/01-state.md)
2. [`stage-02/02-node.md`](stage-02/02-node.md)
3. [`stage-02/03-edge-routing.md`](stage-02/03-edge-routing.md)
4. [`stage-02/04-checkpoint-persistence.md`](stage-02/04-checkpoint-persistence.md)
5. [`stage-02/05-human-in-the-loop.md`](stage-02/05-human-in-the-loop.md)

### [Stage 03 — Context Engineering](stage-03/README.md)

1. [`stage-03/01-context-model.md`](stage-03/01-context-model.md)
2. [`stage-03/02-context-budget-compaction.md`](stage-03/02-context-budget-compaction.md)
3. [`stage-03/03-context-security-isolation.md`](stage-03/03-context-security-isolation.md)

### [Stage 04 — RAG](stage-04/README.md)

1. [`stage-04/01-rag-foundation.md`](stage-04/01-rag-foundation.md)
2. [`stage-04/02-retrieval-quality.md`](stage-04/02-retrieval-quality.md)
3. [`stage-04/03-enterprise-rag.md`](stage-04/03-enterprise-rag.md)

### [Stage 05 — Planning 与可靠性](stage-05/README.md)

1. [`stage-05/01-planning.md`](stage-05/01-planning.md)
2. [`stage-05/02-retry-circuit-breaker.md`](stage-05/02-retry-circuit-breaker.md)
3. [`stage-05/03-verification-replan.md`](stage-05/03-verification-replan.md)

### [Stage 06 — Memory](stage-06/README.md)

1. [`stage-06/01-memory-model.md`](stage-06/01-memory-model.md)
2. [`stage-06/02-memory-engineering.md`](stage-06/02-memory-engineering.md)

### [Stage 07 — Multi-Agent](stage-07/README.md)

1. [`stage-07/01-routing-intent.md`](stage-07/01-routing-intent.md)
2. [`stage-07/02-supervisor-subagent.md`](stage-07/02-supervisor-subagent.md)
3. [`stage-07/03-parallel-handoff-synthesis.md`](stage-07/03-parallel-handoff-synthesis.md)
4. [`stage-07/04-multi-agent-reliability.md`](stage-07/04-multi-agent-reliability.md)

### [Stage 08 — Deep Agents](stage-08/README.md)

1. [`stage-08/01-deep-agents-model.md`](stage-08/01-deep-agents-model.md)
2. [`stage-08/02-deep-agents-integration.md`](stage-08/02-deep-agents-integration.md)

### [Stage 09 — Agent Harness](stage-09/README.md)

1. [`stage-09/01-harness-architecture.md`](stage-09/01-harness-architecture.md)
2. [`stage-09/02-hooks-workspace-runtime-policy.md`](stage-09/02-hooks-workspace-runtime-policy.md)

## Advanced Track

Stage 10–14，共 11 章。只有 Core Path 完成后，学习者明确选择 Advanced Track 才进入 Stage 10。

### [Stage 10 — MCP](stage-10/README.md)

1. [`stage-10/01-mcp-foundation.md`](stage-10/01-mcp-foundation.md)
2. [`stage-10/02-mcp-enterprise.md`](stage-10/02-mcp-enterprise.md)

### [Stage 11 — Observability 与 Evaluation](stage-11/README.md)

1. [`stage-11/01-observability.md`](stage-11/01-observability.md)
2. [`stage-11/02-evaluation.md`](stage-11/02-evaluation.md)

### [Stage 12 — Security](stage-12/README.md)

1. [`stage-12/01-agent-security.md`](stage-12/01-agent-security.md)
2. [`stage-12/02-permission-sandbox.md`](stage-12/02-permission-sandbox.md)

### [Stage 13 — 企业服务化](stage-13/README.md)

1. [`stage-13/01-fastapi-storage.md`](stage-13/01-fastapi-storage.md)
2. [`stage-13/02-distributed-runtime.md`](stage-13/02-distributed-runtime.md)
3. [`stage-13/03-docker-kubernetes.md`](stage-13/03-docker-kubernetes.md)

### [Stage 14 — 用户自选项目综合集成](stage-14/README.md)

1. [`stage-14/01-capstone-architecture.md`](stage-14/01-capstone-architecture.md)
2. [`stage-14/02-capstone-implementation.md`](stage-14/02-capstone-implementation.md)

---

## 完成边界

- Stage 09 完成即 Core Path 完成；不得自动进入 Stage 10，必须等待学习者明确选择 Advanced Track。
- Stage 14 完成即完整课程完成；不存在后续 Stage。

## 课程完成标准

能力主线覆盖：

`LangChain + LangGraph + Harness + Deep Agents + RAG + Tool + Multi-Agent + MCP + Memory + HITL + Persistence + Observability + Evaluation`

长期项目由用户在 Project Track 触发点自行选择，不以预设项目作为课程完成条件。

每章只有完成 Q&A 并达到 `mastered` 才算完成。
