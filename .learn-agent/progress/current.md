# 当前学习进度

```yaml
schema_version: 2
schema_migration_evidence_id: schema-v2-state
storage_backend: git_repository
stage_id: stage-01
stage_name: LangChain 与 Agent 基础
chapter_id: 02-structured-output
chapter_file: curriculum/stage-01/02-structured-output.md
note_pointer: stage-01/02-structured-output.md
qa_pointer: stage-01.md
lifecycle_status: active
learning_status: learning
integrity:
  status: healthy
  missing: []
  reason: null
mastery:
  score: null
  critical_questions_passed: false
  dimension_floors_passed: false
  required_exercises_passed: false
  unresolved_critical_misconceptions: 0
  mastered: false
last_note_update: 2026-10-10：已补教 model_validate 方法。此前仅在示例出现，用户未记住方法名不作为错误证据，继续实际代码执行练习。
last_section: 2.7 model_validate 与业务入口校验
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: knowledge_check
  topic: L2-CHECK-7 / attempt 7
  next_action: 复检 ProductIn.model_validate(raw) 在校验失败时是否执行 else 和 append。
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 103
last_checkpoint_at: '2026-10-10T07:12:41.446Z'
last_checkpoint_reason: knowledge_event
pending_writeback:
  transaction_id: ch02-validation-checks-a7-a8-to-retry-20261010
  reason: qa_complete
  phase: prepared
  started_at: '2026-10-10T07:27:33.609Z'
  targets:
  - asset_key: notes.root
    relative_pointer: stage-01/02-structured-output.md
    evidence_id: stage-01-ch02-L2-CHECK-7-attempt-7
    operation: upsert
    expected_change: Record correct invalid-input exception handling, without inventing missing list-state response.
    verified: false
    error: null
  - asset_key: notes.root
    relative_pointer: stage-01/02-structured-output.md
    evidence_id: stage-01-ch02-L2-CHECK-7-attempt-8
    operation: upsert
    expected_change: Record successful normal-input retest and introduce bounded retries.
    verified: false
    error: null
  - asset_key: qa.stage
    relative_pointer: null
    evidence_id: stage-01-ch02-L2-CHECK-7-attempts-7-8-ledger
    operation: upsert
    expected_change: Record complementary attempts proving validation-first save behavior.
    verified: false
    error: null
  - asset_key: bugs.book
    relative_pointer: null
    evidence_id: bug-stage-01-ch02-raw-vs-parsed-resolved-after-validation
    operation: upsert
    expected_change: Resolve misuse-of-raw misconception using Pydantic validation and save-path evidence.
    verified: false
    error: null
chapter_model_profile: TEACH_DEFAULT
chapter_model_profile_source: stage-01/chapter-02
deepseek_route_prompted_for:
- stage-01/chapter-03
- stage-01/chapter-04
- stage-01/chapter-05
last_deepseek_route_decision: stay
code_ability_focus: LLM / Message / Prompt
project_track_status: deferred
project_selection_prompted: true
completed:
- 01-llm-message-prompt-langchain
weak_points:
- 已认识到parsed应先校验，但仍需巩固原始字符串绕过校验可能静默污染业务数据，而非必然异常。
next_action: L2-CHECK-7 attempt 7：验证先校验后保存程序在 price=abc 情形下的执行流程。
next_chapter: null
migration_evidence_id: migration-20260819T215842
```
