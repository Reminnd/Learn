# Deterministic Mastery Rubric

在章节 Q&A、补考、切章或任何 `mastered` 判定时读取。本文件是掌握判定的唯一事实源；`shared/qa-rubric.md` 只说明反馈维度，不得定义另一套阈值。

## 评分维度

总分 100：

| 维度 | 满分 |
|---|---:|
| 概念理解 | 25 |
| 因果与数据流解释 | 20 |
| 应用与框架映射 | 20 |
| 调试与故障排查 | 20 |
| 迁移、边界与 Trade-off | 15 |

每个维度必须达到其满分的 60%。章节可以提高阈值，不能降低全局底线。

## Mastery predicate

`mastery.mastered=true` 当且仅当全部满足：

1. 总分 `>= 80`；
2. 章节声明的所有 `critical_questions` 最近一次有效作答均通过；
3. 五个维度均达到 floor；
4. 所有 `required_exercises` 满足其 acceptance criteria；
5. `unresolved_critical_misconceptions == 0`；
6. `integrity.status == healthy`；
7. 本章存在合法验收契约，且引用的问题和练习 ID 都存在。

```text
0–59   → needs_review
60–79  → qa（允许继续局部学习，但本章未 mastered）
80–100 → 重新执行全部硬门槛；通过后才 mastered
```

“可继续当前教学”与“本章已掌握”是两个判断，75 分不等于 mastered。

## 关键题

关键题必须由章节以稳定 ID 显式声明，不能由当前窗口临时决定。关键题通过至少要求：回答命中该题的 acceptance 要点，且没有与核心模型冲突的陈述。评分证据记录 question ID、attempt、维度得分、结论与 evidence ID。

## 补考

- 每次作答追加独立 attempt，不覆盖历史证据。
- 每道题只采用最近一次有效 attempt；无效或中断 attempt 不参与计算。
- 基于各题最近有效答案重新计算五维得分和所有门槛；不把新旧总分取平均。
- 补考通过后仍需重新执行完整 mastery predicate。

## 可重算性

状态中的 `score`、各布尔门槛和 `mastered` 都是派生值。若无法从当前笔记和 Q&A evidence 重算，设置 `integrity.status=needs_reconstruction`，而不是沿用旧结论。
