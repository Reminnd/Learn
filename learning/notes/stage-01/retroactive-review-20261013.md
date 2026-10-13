<!-- learn-agent:evidence:stage01-supplemental-20261013-plan-v1:start -->
# Stage 01｜新增知识专项补课记录（2026-10-13）

> 该文件位于manifest的`notes.root`之下，维护**已完成章节新增知识**的补课计划与后续答题证据；不是新的正式章节，不替代旧章已经提交的mastery记录。当前状态只表示**补课已安排，尚无通过证据**。课程说明见[定向补课教材](../../../curriculum/stage-01/retroactive-review-20261013.md)（从仓库根目录引用：`curriculum/stage-01/retroactive-review-20261013.md`）。

## 补课队列（所有通过状态必须以后续用户回答的真实证据为准）

| 任务ID | 所属已完成章节 | 只补新增知识 | 状态 | 答题证据 |
|---|---|---|---|---|
| R01 | Stage 01/01（mastered=82） | Prompt Chaining与固定Workflow / Agent边界 | in_progress，待首次提问 | 无 |
| R02 | Stage 01/02（mastered=82） | Pydantic与TS静态类型/AJV运行时Schema校验 | pending | 无 |
| R03 | Stage 01/03（mastered=84） | Tool Calling与ReAct区分，Kimi Python Toolset源码 | pending | 无 |

- **优先顺序**：R01 → R02 → R03；一回合仅问一题，先讲新增知识再复检。
- **通过准则**：在没有直接展示标准答案的前提下，用户能独立解释关键因果关系、控制流以及至少一个适用或失败边界；如不通过只复检该任务。
- **学习证据分级**：阅读源码不等于独立编写；项目来源与作者归属不能凭项目访问记录推断。仅记录真实回答、阅读/运行行为，不凭计划本身生成passed/mastered。
- **当前正式章节与章节验收不变**：`stage-01/04-tool-registry-engineering`仍处于`learning`，第01–03章仍为completed；未来第05章ReAct完整循环不提前毕业。

## 原课程待答问题（补课结束后必须精确恢复）

```yaml
stage_id: stage-01
chapter_id: 04-tool-registry-engineering
chapter_file: curriculum/stage-01/04-tool-registry-engineering.md
note_pointer: stage-01/04-tool-registry-engineering.md
last_section: 4.1 Tool Registry统一注册与同名工具冲突
current_activity: learning
return_to:
  activity: knowledge_check
  topic: L4-CHECK-1 / attempt 1
  next_action: 回答重复注册get_price时会使用哪个handler，并说明风险。
next_action: L4-CHECK-1 attempt1：解释Registry同名工具覆盖并识别风险。
```

## 后续答题记录（尚无）

- R01：待授课/待回答，不是passed。
- R02：待授课/待回答，不是passed。
- R03：待授课/待回答，不是passed。

新增答题证据必须以稳定ID幂等记录并遵守S03 WAL + batching。第03题通过并flush后恢复第04章原问题，不得跳章。
<!-- learn-agent:evidence:stage01-supplemental-20261013-plan-v1:end -->
