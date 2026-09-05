# Chapter Acceptance Contract

本文件只定义章节验收契约的结构与有效性。完整 mastery predicate 只由 `shared/mastery-rubric.md` 定义。

每章必须包含以下稳定结构：

```yaml
## 验收契约

chapter_id: <canonical-stable-id>
prerequisites:
  - <可解析的前置引用；无则 []>
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
      - <可观察结果>
mastery:
  threshold: 80
  dimension_floor_ratio: 0.60
  critical_questions: [Q1]
  required_exercises: [EX1]
```

## 契约有效性

章节验收契约当且仅当同时满足以下条件时有效：

- 章节内恰好存在一个 `## 验收契约`。
- `chapter_id` 是 canonical ID，且在全课程中唯一。
- `questions` 非空。
- `required_exercises` 非空。
- 当前 critical question set 非空，即至少一道 question 显式声明 `critical: true`，且 `mastery.critical_questions` 非空。
- `questions` 中的 question ID 在本章内唯一。
- `required_exercises` 中的 exercise ID 在本章内唯一。
- 每道 question 的 `prompt` 非空，`critical` 显式为 `true` 或 `false`，`acceptance` 非空且每项均描述可观察结果。
- 每项 exercise 的 `task` 非空，`acceptance` 非空且每项均描述可观察结果。
- `mastery.critical_questions` 恰好等于 `critical: true` 的 question ID 集合。
- `mastery.required_exercises` 恰好等于 `required_exercises` 中声明的 exercise ID 集合。
- `mastery.threshold` 在 `[80, 100]` 内。
- `mastery.dimension_floor_ratio` 在 `[0.60, 1.00]` 内。
- 每个 `prerequisites` 引用都能解析到其 canonical 前置目标。

acceptance 必须写可验证的行为、输出或判断条件。只要 criterion 同时指定可检查的回答或 artifact，以及其中应呈现的具体关系、判断、数据流或输出，就是 observable；因此当前 canonical 形式“产出可运行代码或可执行伪代码，展示：<具体关系/判断/输出>”有效。`展示：` 后使用“理解”作为引导词也不使 criterion 失效，前提是整体已指定可检查的 artifact，且展示对象具体。只有“理解”“熟悉”“掌握良好”等词而没有可检查 evidence 或具体展示对象的裸描述不是 observable。契约无效时可以继续教学，但 mastery 判定必须为 false。

## `contract_chapter_id`

`contract_chapter_id` 是当前 canonical chapter acceptance contract 的 `chapter_id`。它只把 evidence 与当前验收契约关联起来。

`contract_chapter_id` 不替代也不迁移 state `chapter_id`、seed note `chapter_id` 或 routing/display ID；这些 ID 保持各自现有职责。
