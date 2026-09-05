# 课程笔记索引

| Stage | Chapter | 笔记 | Q&A Ledger | 状态 | 最后更新 |
|---|---|---|---|---|---|
| stage-01 | 01 | `learning/notes/stage-01/01-llm-message-prompt-langchain.md` | `learning/qa/stage-01.md` | learning | 2026-08-19 |

<!-- learn-agent:evidence:stage-01-ch01-mastered-index:start -->
## stage-01 / Chapter 01 最新状态

- note: `stage-01/01-llm-message-prompt-langchain.md`
- learning_status: `mastered`
- lifecycle_status: `consolidated`
- score: `82/100`
- completed_at: `2026-08-20`
<!-- learn-agent:evidence:stage-01-ch01-mastered-index:end -->

<!-- learn-agent:evidence:stage-01-ch02-index-active:start -->
## stage-01 / Chapter 02 最新状态

- note: `stage-01/02-structured-output.md`
- learning_status: `mastered`
- lifecycle_status: `consolidated`
- score: `88/100`
- completed_at: `2026-08-21`
<!-- learn-agent:evidence:stage-01-ch02-index-active:end -->

<!-- learn-agent:evidence:stage-01-ch03-index-active:start -->
## stage-01 / Chapter 03 最新状态

- note: `stage-01/03-tool-basics.md`
- learning_status: `mastered`
- lifecycle_status: `consolidated`
- score: `87/100`
- completed_at: `2026-08-21`
<!-- learn-agent:evidence:stage-01-ch03-index-active:end -->

<!-- learn-agent:evidence:stage-01-ch04-index-active:start -->
## stage-01 / Chapter 04 最新状态

- note: `stage-01/04-tool-registry-engineering.md`
- learning_status: `mastered`
- lifecycle_status: `consolidated`
- score: `85/100`
- completed_at: `2026-08-22`
<!-- learn-agent:evidence:stage-01-ch04-index-active:end -->

<!-- learn-agent:evidence:session-summary-20260822:start -->
## 2026-08-22 学习总结

- completed: `Chapter 04 Tool Registry Engineering — mastered 85/100`
- note: `stage-01/04-tool-registry-engineering.md`
- curriculum_update: `结构校验、定义冻结、权限、风险、超时、重试、审计、结果限长`
- resume_at: `Chapter 05 Agent Loop`
- session_status: `paused`
<!-- learn-agent:evidence:session-summary-20260822:end -->

<!-- learn-agent:evidence:stage-01-ch05-index-active:start -->
## stage-01 / Chapter 05 最新状态

- note: `stage-01/05-agent-loop.md`
- learning_status: `learning`
- lifecycle_status: `active`
- current_section: `5.1 Agent Loop 的反馈循环与终止边界`
- started_at: `2026-08-22`
<!-- learn-agent:evidence:stage-01-ch05-index-active:end -->

<!-- learn-agent:evidence:stage-01-ch06-production-hardening-added:start -->
## Stage 01 / Chapter 06 课程迁移

- chapter: `stage-01/06-production-hardening.md`
- title: `生产级强化：从最小 Agent 到可治理 Harness`
- prerequisites: `Chapter 01～05`
- Chapter 01: `调用记录、Message/metadata/usage、Prompt/Schema 版本、脱敏与可重放边界`
- Chapter 02: `JSON/Schema 分层校验、版本兼容、机器动作与有界重试`
- Chapter 03: `Tool 契约与 args 校验、异常分类、tool_call_id、ToolMessage 限长`
- Chapter 04: `定义冻结、Registry 元数据、权限/风险、timeout/retry、审计、受控 override`
- Chapter 05: `turn/tool/token/time/cost 预算、重复调用、stop reason、幂等与副作用`
- route: `Chapter 05 mastered → Chapter 06 → Stage 02`
- model_profile: `TEACH_DEEP`
- status: `not_started`
<!-- learn-agent:evidence:stage-01-ch06-production-hardening-added:end -->

<!-- learn-agent:evidence:teaching-rule-langchain-langgraph-detailed-explanation:start -->
## LangChain / LangGraph 教学规则

- official_docs_role: `核对当前 API、版本、弃用信息与补充出处`
- prohibited: `只给官方文档链接，或让学习者自行阅读代替教学`
- required_explanation: `真实问题 → 手写最小实现 → 核心对象和类型 → 构造/运行阶段 → 输入输出与状态数据流 → 最小可运行框架代码 → 内部行为 → Harness 责任、失败边界与 Trade-off`
- link_timing: `完成详细解析后才可作为证据或延伸阅读`
- scope: `所有 LangChain、LangGraph 章节和生产级框架映射`
- status: `active`
<!-- learn-agent:evidence:teaching-rule-langchain-langgraph-detailed-explanation:end -->
