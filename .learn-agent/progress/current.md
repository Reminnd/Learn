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
last_note_update: 2026-10-10：L2-CHECK-6 attempt 2 通过；能够区分LangChain原始AIMessage与结构化后的ProductIn，进入解析失败处理。
last_section: 2.7 Structured Output 解析失败与可靠性
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: knowledge_check
  topic: L2-CHECK-7 / attempt 1
  next_action: 判断include_raw=True时Pydantic解析失败的raw/parsed/parsing_error字段。
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 98
last_checkpoint_at: '2026-10-10T06:52:35.795Z'
last_checkpoint_reason: qa_complete
pending_writeback:
  transaction_id: learn-stage01-ch02-check7-a1-20261010
  reason: knowledge_event
  phase: prepared
  started_at: '2026-10-10T06:57:44.154Z'
  targets:
  - asset_key: notes.root
    relative_pointer: stage-01/02-structured-output.md
    evidence_id: stage-01-ch02-L2-CHECK-7-attempt-1
    operation: upsert
    expected_change: Record L2-CHECK-7 partial answer and correct parsing failure handling.
    verified: false
    error: null
  - asset_key: qa.stage
    relative_pointer: null
    evidence_id: stage-01-ch02-L2-CHECK-7-attempt-1-ledger
    operation: upsert
    expected_change: Record L2-CHECK-7 needs_review and targeted retest.
    verified: false
    error: null
  - asset_key: bugs.book
    relative_pointer: null
    evidence_id: bug-stage-01-ch02-raw-vs-parsed-on-validation-failure
    operation: upsert
    expected_change: Capture incorrect assumption that raw is validated and parsed key is absent.
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
weak_points: []
next_action: L2-CHECK-7 / attempt 1：include_raw=True 时解析失败的诊断字段，随后学习有限重试、校验及测试。
next_chapter: null
migration_evidence_id: migration-20260819T215842
```
