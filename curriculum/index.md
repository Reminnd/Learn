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
   **第04→05章教学桥接（不计入40章）**：[FastAPI最小业务后端](stage-01/fastapi-backend-bridge.md)——先熟悉路由、Pydantic、依赖注入、HTTP错误与pytest，再让第05章Agent Loop接入API。它是第05章内容开始前的教学插曲，不改变正式章序或mastery。
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

## 配套学习路线、范式与项目源码阅读（不改变40章顺序）

- [Agent范式、软件设计模式与40章课程映射](agent-paradigm-map.md)：将 **ReAct、Tool Calling、Prompt Chaining、Routing、Plan-and-Execute、Reflection / Evaluator-Optimizer、Parallelization、Supervisor/Handoff、RAG/Agentic RAG** 按P0/P1优先级嵌入现有章节；ReWOO、Reflexion、ToT/LATS为按需拓展。不新增编号章节。
- [AI全栈与Agent产品开发补充学习路线](ai-fullstack-agent-roadmap.md)：**Python Agent＋FastAPI → TypeScript/React/Node.js → 产品集成 → 数据库、鉴权、SSE与部署测试**；与原课程并行实践，原40章仍是唯一canonical route。
- [真实项目源码映射学习法](../shared/project-source-learning.md)：用学习者**提供的Vibe Coding项目**作为源码学习实例，查真实函数、调用链与工程范式。项目不需要由学习者手写；仅代码阅读不等于独立开发或掌握。
- [首批6个Coding Agent开源源码案例库](project-source-casebook.md)：Pi、Kimi Python旧版与TypeScript新版、DeepSeek Harness、Codex、非官方Claude Code恢复版。仅作为经过路径核实的参考案例，按当前知识点选择1～2个对照。
- [已确认的后端先行教学桥接](stage-01/fastapi-backend-bridge.md)：Stage01/04完成后、正式讲Stage01/05 Agent Loop前插入FastAPI最小服务与接口测试；SQL/ORM在LangGraph阶段逐步引入，Stage13保留高级服务化。不新增正式章节。
- [Stage 01已完成章节新增内容补课（2026-10-13）](stage-01/retroactive-review-20261013.md)：针对已掌握的01–03章新增Prompt Chaining、跨语言Schema、Tool Calling/ReAct对照，按R01→R02→R03补课；**不改40章路由、不重新判定旧mastery**。
- 已有章节继续按原验收契约和committed state推进。补充范式和案例不能绕过原有EX/Q&A/mastery判定，也不自动激活长期Project Track。

## 完成边界

- Stage 09 完成即 Core Path 完成；不得自动进入 Stage 10，必须等待学习者明确选择 Advanced Track。
- Stage 14 完成即完整课程完成；不存在后续 Stage。

## 课程完成标准

能力主线覆盖：

`LangChain + LangGraph + Harness + Deep Agents + RAG + Tool + Multi-Agent + MCP + Memory + HITL + Persistence + Observability + Evaluation`

长期项目由用户在 Project Track 触发点自行选择，不以预设项目作为课程完成条件。

每章只有完成 Q&A 并达到 `mastered` 才算完成。
