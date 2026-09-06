# <章节标题> — 课程笔记

## Metadata

- stage_id: `<stage-id>`
- chapter_id: `<chapter-id>`
- chapter_file: `<curriculum path>`
- schema_version: `2`
- lifecycle_status: `initialized | active | consolidated`
- learning_status: `not_started | learning | practice | qa | needs_review | mastered`
- last_updated: `<time or turn>`

## 1. 本章目标

## 2. 核心概念

## 3. Harness 中的位置

## 4. 最小原理实现

## 5. LangChain / LangGraph 框架实现

## 6. 手写版 vs 框架版

## 7. 工程问题与解决方案

## 8. Trade-off / 架构选择

## 9. 企业级设计结论

## 10. 关键英文术语

## 11. 代码与调试记录

## 12. Evidence 记录

以下 YAML 块是未提交的 record template，不是当前 evidence。只有实际作答或练习经过验证并进入 committed state 后，才填写对应记录；字段定义以 `shared/mastery-rubric.md` 为唯一权威来源。

### 12.1 Question attempt

```yaml
kind: question_attempt
evidence_id: <stable-evidence-id>
contract_chapter_id: <current-contract-chapter-id>
question_id: <declared-question-id>
attempt: <positive-integer>
answer_ref: <answer-or-note-reference>
acceptance_snapshot:
  - <acceptance-criterion>
acceptance_results:
  - criterion: <exact-acceptance-criterion>
    satisfied: <boolean>
    evidence: <specific-verifiable-answer-evidence>
core_model_conflict:
  detected: <boolean>
  evidence: <specific-check-observation>
passed: <derived-boolean>
```

### 12.2 Exercise attempt

```yaml
kind: exercise_attempt
evidence_id: <stable-evidence-id>
contract_chapter_id: <current-contract-chapter-id>
exercise_id: <declared-exercise-id>
attempt: <positive-integer>
artifact_ref: <artifact-reference>
acceptance_snapshot:
  - <acceptance-criterion>
acceptance_results:
  - criterion: <exact-acceptance-criterion>
    satisfied: <boolean>
    evidence: <specific-verifiable-artifact-observation>
accepted: <derived-boolean>
```

### 12.3 Mastery assessment

```yaml
kind: mastery_assessment
evidence_id: <stable-evidence-id>
contract_chapter_id: <current-contract-chapter-id>
source_evidence_ids:
  - <question-attempt-evidence-id>
dimension_scores:
  conceptual_understanding: <0..25>
  causal_and_dataflow: <0..20>
  application_and_framework_mapping: <0..20>
  debugging_and_troubleshooting: <0..20>
  migration_boundaries_and_tradeoffs: <0..15>
```

## 13. 易错点 / 薄弱点

## 14. 复习卡片

## 15. 下一步


## 16. Bug Book 关联

- 本章相关 Bug ID：暂无

## 17. Q&A Ledger 关联

- 本章相关 Q&A ID：暂无
