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
  - criterion: <exact-acceptance-criterion>
    satisfied: <boolean>
    evidence: <specific-verifiable-answer-evidence>
core_model_conflict:
  detected: <boolean>
  evidence: <specific-check-observation>
passed: <derived-boolean>
```

`passed` 的定义是：

```text
passed :=
  every acceptance_results[*].satisfied == true
  AND core_model_conflict.detected == false
```

`core_model_conflict` 必须完整记录：`detected` 是 explicit boolean，`evidence` 非空、具体、可检查，并记录实际执行的 core-model conflict 检查依据。若 record 保存 `passed`，stored `passed` 必须严格等于按上式 recomputed `passed`；不一致时该 attempt invalid。Agent impression、用户指令或旧 `passed` boolean 均不得作为通过依据。

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
  - criterion: <exact-acceptance-criterion>
    satisfied: <boolean>
    evidence: <specific-verifiable-artifact-observation>
accepted: <derived-boolean>
```

`accepted` 的定义是：

```text
accepted := every acceptance_results[*].satisfied == true
```

若 record 保存 `accepted`，stored `accepted` 必须严格等于按上式 recomputed `accepted`；不一致时该 attempt invalid。

Question attempt 和 exercise attempt 的 `acceptance_results` 只使用以上一种确定结构，并与各自的 `acceptance_snapshot` 严格、按顺序一一对应：

1. 两个 list 的数量必须完全相等。
2. 每个 snapshot criterion 都必须有且只有一个 result，不得缺少 criterion，也不得多出 criterion。
3. 第 `i` 个 `acceptance_results` 必须对应第 `i` 个 `acceptance_snapshot`，且 `result.criterion` 必须与 snapshot criterion 文本严格相等；禁止 fuzzy matching。
4. `acceptance_snapshot` 和 `acceptance_results` 中均不得出现重复 criterion。
5. 每个 `satisfied` 必须是 explicit boolean。
6. 每个 `evidence` 必须非空、具体、可检查；question 记录可验证的 answer evidence，exercise 记录可验证的 artifact observation。

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

完整 mastery assessment 必须已经通过 domain verification 并进入 committed state；其 required fields 完整，`contract_chapter_id` 等于当前契约 ID，`source_evidence_ids` 无重复且作为集合恰好等于每道 declared question 当前选中的 latest valid attempt evidence ID 集合，并且 `dimension_scores` 恰好包含全部五个维度且各自在上表范围内。

对当前选中的 latest-valid question source set，必须只有一个 committed complete mastery assessment；同一 source set 的幂等提交或 recovery 必须重用原 `evidence_id`，不得提交另一个 assessment。只有恰好一个匹配的 committed complete assessment 时，它才是 authoritative assessment。零个匹配项或多个匹配项均表示没有唯一确定的 authoritative assessment；尤其不得在两个 `dimension_scores` 冲突的 assessment 之间任选其一，此时 `score=null`。`score` 是所选 authoritative assessment 五个维度原始分数的直接和；缺少任一道 declared question 的 latest valid attempt 时同样为 `score=null`。

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

`status` 与 resolution evidence 的关系固定为：

- `open`：`resolution_evidence_id=null`。
- `improving`：`resolution_evidence_id=null`。
- `resolved`：`resolution_evidence_id` 必须是 valid matching resolution evidence ID。

Valid matching resolution evidence 必须同时满足：`resolution_evidence_id` 非空且对应 evidence 存在；evidence 已通过 S03 domain verification 并进入 committed state；evidence 的 `contract_chapter_id` 和 `misconception_id` 分别匹配当前章节契约和该 misconception；若 misconception 有 `question_id`，evidence 必须与对应 question/core-model 的原误解相关；evidence 内容必须具体证明该 misconception 已解决。

```text
resolved_valid :=
  status == resolved
  AND valid matching committed resolution evidence exists

effective_status :=
  resolved   if resolved_valid == true
  improving  if status == resolved AND resolved_valid == false
  status     otherwise
```

只有 valid resolution evidence 才能形成有效 `resolved` 状态。`status=resolved` 但 evidence ID 为 null、evidence 不存在、未 committed、未 verified、chapter 或 misconception 不匹配、与对应 question/core-model 的原误解无关，或内容无法证明已解决时，`resolved_valid=false`；mastery 计算必须将其作为 `effective_status=improving`，不得 silent fallback 为 resolved。

## Valid attempt

`valid attempt` 是派生判断，不得把 `valid: true` 直接保存在 evidence 中。Question attempt 或 exercise attempt 必须同时满足以下条件才是 valid：

- evidence 已通过 S03 domain verification。
- evidence 已进入 committed state。
- `evidence_id` 与 `(contract_chapter_id, item_id, attempt)` 唯一对应；question 的 `item_id` 是 `question_id`，exercise 的 `item_id` 是 `exercise_id`。
- 对应 record 的 required fields 完整。
- item ID 存在于当前章节验收契约。
- `acceptance_snapshot` 与该 item 的当前 acceptance list 完全相等。
- Question attempt 的 `acceptance_results` schema 有效、与 `acceptance_snapshot` exact ordered one-to-one、每项 evidence 非空且具体，`core_model_conflict` record 完整，且 stored `passed` 等于 recomputed `passed`。
- Exercise attempt 的 `acceptance_results` schema 有效、与 `acceptance_snapshot` exact ordered one-to-one、每项 evidence 非空且具体，且 stored `accepted` 等于 recomputed `accepted`。

Invalid、interrupted 或 stale attempt 不参与 mastery 计算。

## Latest valid attempt

`attempt` 的编号范围是同一 `(contract_chapter_id, item_id)`。第一个 logical attempt 必须使用 `attempt: 1`；此后每个新的 logical attempt 的 attempt number 必须严格大于该 item 此前已分配的所有 attempt number，无论此前 attempt 最终 valid、invalid 或 interrupted。新 logical attempt 不得复用旧 attempt number 或旧 `evidence_id`。

对每个 item，latest valid attempt 是 attempt number 最高的 valid record。

- 新的 valid failure 必须替换旧 pass；曾经通过不构成永久通过。
- Invalid 或 interrupted attempt 不覆盖此前的 latest valid attempt。
- Recovery 是原 logical attempt 的继续，必须重用原 `evidence_id` 和 attempt number，不得创建新 attempt。
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
  where critical == true AND effective_status in {open, improving}
```

Invalid resolved misconception 的 `effective_status` 是 `improving`，因此仍计入 `unresolved_critical_misconceptions`。

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
