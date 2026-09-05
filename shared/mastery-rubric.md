# Deterministic Mastery Rubric

在章节 Q&A、补考、切章或任何 `mastered` 判定时读取。本文件是完整 mastery predicate 的唯一 authoritative source；章节契约只定义 acceptance contract 的结构与有效性，`shared/qa-rubric.md` 只说明反馈维度。

所有判定均使用当前重新读取且有效的章节验收契约，以及与其 `chapter_id` 对应的 committed evidence。该 ID 在 evidence 中记为 `contract_chapter_id`。

## Stable evidence contract

### Question attempt

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
  - <criterion-result>
passed: <boolean>
```

`passed` 的定义是：

```text
passed :=
  all acceptance criteria satisfied
  AND no conflict with the question core model
```

### Exercise attempt

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
  - <criterion-result>
accepted: <boolean>
```

`accepted` 的定义是：

```text
accepted := all acceptance criteria satisfied
```

### Mastery assessment

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

五个维度的满分是：

| Dimension | Maximum |
|---|---:|
| `conceptual_understanding` | 25 |
| `causal_and_dataflow` | 20 |
| `application_and_framework_mapping` | 20 |
| `debugging_and_troubleshooting` | 20 |
| `migration_boundaries_and_tradeoffs` | 15 |

完整 mastery assessment 的 `source_evidence_ids` 必须恰好引用每道 declared question 当前选中的 latest valid attempt，且 `dimension_scores` 必须包含全部五个维度。`score` 是五个维度原始分数的直接和；缺少任一道 declared question 的 latest valid attempt、引用不完整或缺少任一维度时，`score=null`。

### Misconception evidence

参与本章 mastery 判定的 misconception 使用以下字段：

```yaml
misconception_id: <stable-misconception-id>
contract_chapter_id: <current-contract-chapter-id>
question_id: <declared-question-id>
critical: <boolean>
status: <open|improving|resolved>
source_evidence_id: <source-evidence-id>
resolution_evidence_id: <resolution-evidence-id-or-null>
```

## Valid attempt

`valid attempt` 是派生判断，不得把 `valid: true` 直接保存在 evidence 中。Question attempt 或 exercise attempt 必须同时满足以下条件才是 valid：

- evidence 已通过 S03 domain verification。
- evidence 已进入 committed state。
- `evidence_id` 与 `(contract_chapter_id, item_id, attempt)` 唯一对应；question 的 `item_id` 是 `question_id`，exercise 的 `item_id` 是 `exercise_id`。
- 对应 record 的 required fields 完整。
- item ID 存在于当前章节验收契约。
- `acceptance_snapshot` 与该 item 的当前 acceptance list 完全相等。

Invalid、interrupted 或 stale attempt 不参与 mastery 计算。

## Latest valid attempt

对每个 item，latest valid attempt 是 attempt number 最高的 valid record。

- 新的 valid failure 必须替换旧 pass；曾经通过不构成永久通过。
- Invalid 或 interrupted attempt 不覆盖此前的 latest valid attempt。
- Recovery 必须重用原 `evidence_id`，不得创建新 attempt。
- 每次新的 valid evidence 提交后，重新选择全部 latest valid attempts 并重新计算完整 mastery，不平均新旧分数，也不继承旧 `mastered=true`。

## Hard gates

```text
critical_questions_passed :=
  for every question in the current critical set,
  its latest valid attempt has passed == true

required_exercises_passed :=
  for every exercise in the current required exercise set,
  its latest valid attempt has accepted == true

dimension_floors_passed :=
  for every dimension d,
  dimension_score[d] >= dimension_max[d] * dimension_floor_ratio

unresolved_critical_misconceptions :=
  count distinct misconception_id for the current contract_chapter_id
  where critical == true AND status in {open, improving}
```

Dimension floor 使用未取整的乘积比较，不得先对 floor 取整。

## Required evidence

```text
required_evidence_exists :=
  a latest valid attempt exists for every declared question
  AND a latest valid attempt exists for every required exercise
  AND a complete mastery assessment references exactly
      the selected latest-valid question attempts
```

## Authoritative mastery predicate

```text
mastered :=
  chapter_contract_valid
  AND required_evidence_exists
  AND score IS NOT null
  AND score >= current threshold
  AND dimension_floors_passed
  AND critical_questions_passed
  AND required_exercises_passed
  AND unresolved_critical_misconceptions == 0
  AND integrity.status == healthy
  AND committed_state.pending_writeback == null
```

任何 hard gate 都不得由总分、历史 `mastered` 值、用户指令、对话记忆或旧 evidence 绕过。

## Contract change

每次判定都重新读取当前章节验收契约：

- threshold 或 dimension floor 改变：使用当前值重新计算。
- 新增 required item：缺少该 item 的 current evidence，因此不 mastered。
- 删除 item：其旧 evidence 不再参与计算。
- critical designation 改变：以当前 critical set 为准。
- acceptance 改变：旧 `acceptance_snapshot` 不再匹配，attempt 变为 stale。
- stable ID 改变：视为新 item。
- contract 无效：不 mastered。
- 旧 `mastered=true`：不构成任何豁免。
