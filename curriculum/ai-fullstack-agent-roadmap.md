# AI全栈与Agent产品开发补充学习路线

> **性质：职业发展与项目驱动补充路线（非课程的 canonical route）。**
>
> 本路线覆盖 Python Agent、FastAPI、TypeScript、React、Node.js 及工程化交付。它与 [课程索引](index.md) 中 Stage 01–14、40 章的唯一 canonical route 并行，不更改章节顺序、先修条件、mastery 判定或任何已提交的学习进度。只有学习者明确选择后才启动相应长期 Project Track；不能因本文件存在而自动绑定项目或跳章。

## 目标与学习策略

- **求职优先级**：尽快获得 AI Agent 开发实习，同时积累可迁移的业务后端能力。
- **目标能力**：能够解释 Agent Loop、Tool Calling、MCP 与流式事件，开发可用的服务端 API、TypeScript 前端，并完成数据库、鉴权、部署和自动化测试。
- **学习方式**：一个持续演进的项目贯穿各阶段；Python Agent 和 FastAPI 先产出最小闭环，再逐步引入 TypeScript。Stage 04 为工程化深化，但校验、基础错误处理和单元测试应从 Stage 01 起执行。
- **学习进度**：以已有已提交的课程状态为准。本文件不推测、迁移或覆盖当前正在学习的章节。

## 四阶段路线

### 阶段1：完成 Python Agent 基础与 FastAPI API

核心主题：Python、Pydantic、Tool Registry、Tool Calling、Agent Loop、FastAPI、基本异步与 HTTP。

实践里程碑：
1. 保留现有 Python Agent 基础课程，理解工具参数校验、调用链与失败处理，并能手写可测试的 Agent Loop。
2. 使用 FastAPI 提供最小 API：健康检查、提交一次 Agent 请求、查询结果（可先用内存状态）。
3. 用 Pydantic 定义输入/输出契约，建立 pytest 单元测试与 FastAPI 接口测试。

**验收标准**：能够启动并调用 API；请求验证、正常工具调用和典型错误路径有自动测试；能够说明 Python Agent 内部运行流程。

### 阶段2：掌握 TypeScript、React、Node.js

核心主题：JavaScript 异步与 Promise、TypeScript 类型系统、Node.js 运行时、HTTP API、Zod、React。

实践里程碑：
1. 学习 JavaScript 异步、Promise/async-await、异常处理与模块机制，再学习 TypeScript 的类型、接口和泛型。
2. 用 TypeScript/Node.js 实现一个独立的 API Gateway / Adapter 层，练习运行时参数校验、统一错误与事件模型。
3. 使用 React 开发简单界面，能够发起 Agent 请求并展示工具调用状态；配套 Vitest 或 Node.js 测试。

**验收标准**：能够独立解释 TypeScript 静态类型与运行时校验的区别；完成前端到 TypeScript 服务层的一次请求与错误处理。

### 阶段3：把前端与 Agent 服务连成完整产品

核心主题：跨语言 API 契约、组件边界、实时事件、任务状态、取消与错误传播。

实践里程碑：
1. 将 React（必要时 Electron/Tauri）接入 TypeScript Gateway，再由 Gateway 调用 Python Agent/FastAPI 服务。
2. 设计版本化的请求、任务 ID、状态、错误与事件契约；先完成请求/响应链路，再完成 SSE 实时事件与取消。
3. 把 Agent 工具执行信息展示为可理解的任务进度，并完善端到端测试与故障场景测试。

**验收标准**：从界面提交请求，能观察执行过程并获得结果；断连、取消与失败不会产生伪成功状态。

### 阶段4：补数据库、鉴权、流式响应、部署与测试

核心主题：PostgreSQL/MySQL、SQLAlchemy/ORM、事务、身份验证和授权、SSE/流式协议、Docker、日志、监控、CI。

实践里程碑：
1. 将阶段1/3的内存任务状态迁移到数据库，理解索引、事务与并发一致性。
2. 为业务接口添加身份认证与权限边界，明确用户和工具执行权限；安全地管理密钥。
3. 深化 SSE：增量输出、心跳、断连、取消、错误终态、资源清理与可观测性。
4. 完成测试分层（单元/契约/集成/端到端）、容器化部署、配置文档和可演示的 README。

**验收标准**：具有可复现的启动说明、持久化任务记录、鉴权、流式事件、错误恢复说明和自动化测试；能够在面试中解释设计权衡。

## 可选项目载体：动态代码工具系统（方案B）

**推荐起步架构**：TypeScript Gateway＋Python执行器优先，预留JavaScript执行器扩展槽位。

这是一项**建议，尚未自动激活为 Learn 的长期项目**。只有学习者明确选择项目后，才按既有 Project Track 规则纳入正式实践。

- **TypeScript Gateway**：HTTP/MCP接口、输入校验、请求与流式事件协调、执行器选择、统一错误与取消；尽可能复用 `Reminnd/coding-room` 的 TypeScript 协议与MCP实现模式。
- **Python Agent/FastAPI服务**：Python Agent基础和业务 API 的学习载体；可以承担Agent编排及执行任务的受控入口。**“Python执行器”本身不等于FastAPI**，如需练习FastAPI，须独立设计服务API边界。
- **Python执行器**：通过显式的 `ExecutorAdapter` 契约接入；执行可信测试样例可先用 mock/fake，真实动态代码只可在具备可靠隔离与资源限制的执行环境中运行。
- **未来JavaScript执行器**：只预留接口与契约测试，首版不实现第二执行器、不为“双语言覆盖”牺牲安全和可维护性。
- **首版非目标**：多语言任意代码的宿主机直接执行、复杂分布式任务系统、未经验证的生产级远程沙箱。

建议逐步验证：

1. **M1（Python主线）**：Tool Registry → Agent Loop → FastAPI请求与测试。
2. **M2（TypeScript主线）**：Gateway契约、Zod校验、ExecutorAdapter接口与mock，Node侧自动测试。
3. **M3（产品联调）**：React → Gateway → Python服务/执行器，稳定输出执行事件；先验收正常、失败、取消三个路径。
4. **M4（工程交付）**：数据库、鉴权、SSE边界、执行超时和资源约束、日志、部署与端到端测试。
5. **后续可选**：在Python执行器的安全性与契约稳定之后，按同一个Adapter契约增加JavaScript执行器。

**动态代码安全门禁**：任何模型生成或外部传入的代码都视为不可信输入。真实执行前须明确隔离边界（容器或等效强隔离）、时间/CPU/内存/输出限额、网络默认禁用、最小文件权限、无宿主机密钥访问、进程与子进程清理。**未通过该门禁时只运行模拟执行器或可信样例，不直接在宿主机执行任意代码。**

**现有代码复用核对**：`Reminnd/coding-room` 的 `src/mcp/http.ts`、`src/runner/executor.ts`、`src/runner/worker-adapter.ts` 提供TypeScript MCP/执行生命周期与适配器的现有设计参考；已检查的 `worker-adapter.ts` 当前实际实现为 `claude_code_cli`，不可把文档中的Codex设计直接当作已实现的可复用运行时代码。进入实施前必须复核仓库当时的实际版本与可复用模块。

## 继续学习与路线边界

- 普通“继续学习”：继续遵循 `SKILL.md`、学习状态和 [课程索引](index.md)，不根据本路线猜测已掌握程度或跳章。
- 明确请求补充路线练习：可以结合当前已掌握知识安排小练习；原课程的完成判定仍只看其章节验收契约。
- 进入实际编码与测试：遵循学习者的开发工作流，在规划确定后进入执行工具；本文件只是路线图，并未生成、修改或运行项目代码。
