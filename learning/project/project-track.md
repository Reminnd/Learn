# Project Track（项目驱动模式）

## 当前状态

- project_track_status: `deferred`
- selected_project: `TBD — 由用户决定`
- old_default_project: `disabled`

## 重要约束

当前没有用户认可的长期最终项目。

- 不要默认使用旧项目。
- 不要为了课程方便替用户选项目。
- 现在的 Demo / 小练习都只是局部练习，不自动升级为长期项目。

## 何时提醒用户选项目

在“基础 Harness 架构”已经掌握、课程即将开始模块化能力时提醒一次。判断标准：

- 最小 Agent Loop / Runtime 已掌握。
- LangGraph State / Node / Edge / Routing / Checkpoint 基础已掌握。
- 用户能解释 Session / Thread / State / Context / Runtime / Tool System 的基本边界。
- 基础架构 Q&A 达到可继续水平。
- 下一阶段将进入 Context、RAG、Planning、Memory、Multi-Agent 等可插拔/模块化能力。

在当前课程结构中，通常应在完成 Stage 01～02 的基础骨架、准备进入 Stage 03 及后续能力模块时检查一次；如果课程结构以后变化，以“能力条件”而不是固定 Stage 编号为准。

## 提醒方式

只做一次简短提示：

> 基础 Agent/Harness 骨架已经够用了。接下来会进入 Context、RAG、Memory、Multi-Agent 等模块化能力，这正是选一个长期项目并持续集成这些能力的合适节点。现在可以开始确定你真正想做的项目；如果你还不想定，也可以继续学，之后再启用 Project Track。

用户没选项目：保持 `deferred`，不要催促。

用户选定项目：

1. 将状态改为 `active`。
2. 记录项目目标、用户、核心场景、约束和“不做什么”。
3. 再根据后续课程模块生成项目集成里程碑。
4. 重要架构选择写 ADR。
