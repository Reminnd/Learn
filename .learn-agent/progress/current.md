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
last_note_update: 2026-10-10：L2-CHECK-14 MySQL UNIQUE行为通过；已引入SQLAlchemy IntegrityError/Session.rollback/查询。L2-CHECK-13 attempt 5的Python if复检仍保留。
last_section: 2.11.3 MySQL UNIQUE 与 SQLAlchemy IntegrityError
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: knowledge_check
  topic: L2-CHECK-15 / attempt 1
  next_action: 判断SQLAlchemy INSERT触发IntegrityError后使用同一Session查询历史订单为何应先rollback；随后返回L2-CHECK-13 attempt 5复检。
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 116
last_checkpoint_at: '2026-10-10T08:43:07.305Z'
last_checkpoint_reason: qa_complete
pending_writeback:
  transaction_id: stage01-ch02-check15-batch20261010
  reason: qa_complete
  phase: prepared
  started_at: '2026-10-10T08:52:06.535Z'
  targets:
  - asset_key: notes.root
    relative_pointer: stage-01/02-structured-output.md
    evidence_id: stage01-ch02-L2-CHECK-15-attempts1-3
    operation: upsert
    expected_change: Commit three SQLAlchemy rollback checks and correct misrecorded if check.
    verified: false
    error: null
  - asset_key: qa.stage
    relative_pointer: null
    evidence_id: stage01-ch02-L2-CHECK-15-attempts1-3-ledger
    operation: upsert
    expected_change: Record rollback check outcomes and fix previous incorrect answer attribution.
    verified: false
    error: null
  - asset_key: bugs.book
    relative_pointer: null
    evidence_id: stage01-ch02-if-controlflow-evidence-correction
    operation: upsert
    expected_change: Mark if automatic recheck misunderstanding resolved based on actual answer.
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
- L2-CHECK-13：需要巩固if只在执行到条件时求值一次，之后状态变化不会自动重新执行。
next_action: L2-CHECK-15：理解session.rollback后查询已有订单；后续复检L2-CHECK-13 attempt 5的if执行边界。
next_chapter: null
migration_evidence_id: migration-20260819T215842
```
