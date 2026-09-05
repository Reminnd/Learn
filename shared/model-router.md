# Chapter Model Profile & DeepSeek Harness Router

目标：普通课程使用稳定的章节模型档位；只有评估是否切换到 **Claude Code + DeepSeek V4 Pro** 时才做动态路由。不要把本文件变成每轮都要读取的通用模型选择器。

## 1. 两层路由

### Layer A — 章节固定档位

进入新章节时按下表选择一次，将档位写入 manifest 的 `state.current` 中的 `chapter_model_profile`。同一章节后续直接复用，不因普通问答、练习或短暂困难反复切换。

| 章节 | 固定档位 |
|---|---|
| Stage 01 / 01～04：LLM、Message、Prompt、Structured Output、Tool 基础与 Registry | `TEACH_DEFAULT` |
| Stage 01 / 05：Agent Loop | `TEACH_DEEP` |
| Stage 02：State、Node、Edge、Routing、Checkpoint、Human-in-the-loop | `TEACH_DEEP` |
| Stage 03：Context、Budget、Compaction、Security Isolation | `TEACH_DEEP` |
| Stage 04 / 01～02：RAG 基础与检索质量 | `TEACH_DEFAULT` |
| Stage 04 / 03：Enterprise RAG | `TEACH_DEEP` |
| Stage 05：Planning、Retry、Circuit Breaker、Verification、Replan | `TEACH_DEEP` |
| Stage 06：Memory | `TEACH_DEEP` |
| Stage 07 / 01～02：Routing、Supervisor、Subagent | `TEACH_DEEP` |
| Stage 07 / 03～04：Parallel、Handoff、Synthesis、Reliability | `ARCHITECT` |
| Stage 08：Deep Agents | `TEACH_DEEP` |
| Stage 09：Harness Architecture、Hooks、Workspace、Runtime、Policy | `ARCHITECT` |
| Stage 10 / 01：MCP Foundation | `TEACH_DEEP` |
| Stage 10 / 02：MCP Enterprise | `ARCHITECT` |
| Stage 11：Observability、Evaluation | `TEACH_DEEP` |
| Stage 12：Security、Permission、Sandbox | `ARCHITECT` |
| Stage 13 / 01：FastAPI、Storage | `CODE_DEFAULT` |
| Stage 13 / 02～03：Distributed Runtime、Docker、Kubernetes | `CODE_DEEP` |
| Stage 14：Capstone Architecture、Implementation | `ARCHITECT`；进入实现后使用 `CODE_DEEP` |

当前参考映射（2026-08-19；具体型号不可用或用户询问最新选择时，先查官方文档）：

| 档位 | 默认映射 | 主要用途 |
|---|---|---|
| `TEACH_DEFAULT` | GPT-5.6 Sol + `medium` | 基础概念、普通框架内容、代码讲解 |
| `TEACH_DEEP` | GPT-5.6 Sol + `high` | Runtime、Context、Planning、复杂工程推导 |
| `CODE_DEFAULT` | Codex GPT-5.6 Terra + `high` | 常规实现、测试、普通调试 |
| `CODE_DEEP` | Codex GPT-5.6 Sol + `high` | 跨文件实现、困难调试、复杂重构 |
| `ARCHITECT` | GPT-5.6 Sol + `xhigh` | 高影响架构、安全、分布式、重大 ADR |

章节绑定的是语义档位，不是永久型号。型号换代时只更新映射表，不改课程表。

## 2. Layer B — Claude Code + DeepSeek V4 Pro 条件路由

只有当前活动可能从仓库型 Coding Harness 获益时才评估。先检查三个硬门槛：

1. **任务类型**：实现、测试、调试、重构、跨文件修改或仓库级探索；纯教学、Q&A、面试检验不满足。
2. **仓库需求**：需要真实文件、终端、测试与连续工具调用；单文件片段或伪代码不满足。
3. **数据边界**：用户允许代码进入该外部服务，且仓库不含禁止外传的源码、凭据、个人数据或受监管数据。无法确认时只提示风险，不建议迁移。

硬门槛满足后，再综合四项收益/风险：

- **难度**：更适合大量可验证的工程执行；重大架构判断、极难疑难 Bug 或高错误成本任务优先保留 `CODE_DEEP` / `ARCHITECT`，必要时做独立复核。
- **规模**：文件多、工具调用长、测试循环多、上下文大时更有价值；小改动切换成本通常不值得。
- **成本目标**：用户明确关注成本，或预计长时间高 Token Coding 时，DeepSeek 路线收益上升。
- **可并行性**：存在两个以上低耦合工作流时收益上升；强串行任务不要仅因“可用 subagent”而切换。

满足全部硬门槛，且“规模 / 成本 / 可并行性”中至少两项明显成立，同时风险不是高等级时，才建议：

> 路由建议：当前可考虑 Claude Code + DeepSeek V4 Pro；原因：{一条最关键证据}。切换前确认仓库数据边界与 API 成本。

否则保持章节档位：

> 路由建议：继续使用 `{chapter_model_profile}`；当前切换 Harness 的收益不足或风险更高。

不展示完整打分过程，除非用户询问。相同章节与相同原因只提示一次，并更新：

- `deepseek_route_prompted_for`
- `last_deepseek_route_decision`

## 3. Context 约束

- 普通继续课程：不要读取本文件；使用 manifest 的 `state.current` 已保存的档位。
- 进入新章节：只读取 Layer A 对应行与映射行。
- 评估 DeepSeek 路线：只读取 Layer B，不加载完整章节表。
- 不把模型官网、价格表、安装步骤常驻上下文。只有用户要具体配置或准备切换时，才读取最新官方文档。
- 大上下文不是切换理由本身。先按 `shared/context-budget.md` 做 Hot / Warm / Cold 过滤，再判断是否确实需要仓库 Harness。

## 4. 时效性与权限

- 模型名称、推理档位、上下文窗口、价格和 Claude Code 兼容配置都属于易变信息；输出精确配置前查 OpenAI 与 DeepSeek 官方文档。
- 官方文档确认 DeepSeek 提供 Anthropic API 兼容端点，并给出 `deepseek-v4-pro[1m]`、`max` effort 与自动压缩配置；这只证明可接入，不代表对当前仓库安全、合规或一定优于默认档位。
- 路由建议不授权安装 Claude Code、写入环境变量、保存 API Key、上传仓库或启动付费调用；这些操作必须由用户明确请求并在执行前确认。
