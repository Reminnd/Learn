# Chapter Acceptance Contract

只在首次进入章节、章节契约缺失、准备练习/Q&A 或 mastery 判定时读取。普通讲解只保留当前小节与已解析的契约摘要。

每章必须包含一个 `## 验收契约`，并声明以下稳定结构：

```yaml
chapter_id: <stable-id>
prerequisites:
  - <可验证前置条件；无则 []>
required_exercises:
  - id: EX1
    task: <章节特有任务>
    acceptance:
      - <可观察结果>
questions:
  - id: Q1
    prompt: <章节特有问题>
    critical: true
    acceptance:
      - <必须命中的概念或判断>
mastery:
  threshold: 80
  dimension_floor_ratio: 0.60
  critical_questions: [Q1]
  required_exercises: [EX1]
```

约束：

- `chapter_id` 全课程唯一；问题与练习 ID 在章节内唯一。
- `critical_questions` 必须引用 `questions` 中存在且 `critical: true` 的 ID。
- `required_exercises` 必须引用存在且 acceptance 非空的练习。
- acceptance 写可观察结果，不写“理解”“熟悉”“掌握良好”等主观词。
- 章节可以增加题目、练习或提高阈值；不得降低全局 mastery rubric。
- 契约缺失或无效时允许继续教学，但不允许判定 mastered。

验收 evidence 使用稳定 ID，例如 `<chapter_id>-Q1-attempt-2`、`<chapter_id>-EX1-attempt-1`，便于 WAL 恢复时幂等检查。
