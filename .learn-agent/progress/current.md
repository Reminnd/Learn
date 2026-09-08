# 当前学习进度

```yaml
schema_version: 2
schema_migration_evidence_id: schema-v2-state
storage_backend: git_repository
stage_id: stage-01
stage_name: LangChain 与 Agent 基础
chapter_id: 01-llm-message-prompt-langchain
chapter_file: curriculum/stage-01/01-llm-message-prompt-langchain.md
note_pointer: stage-01/01-llm-message-prompt-langchain.md
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
last_note_update: 2026-09-08：L1-CHECK-13 attempt 2 通过；正确给出 history 长度 2、4、6，并掌握每轮新增两条 Message 的线性增长规律。
last_section: 1.8 Message 历史增长
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: learning_check
  topic: L1-CHECK-14 attempt 1
  next_action: Explain the direct engineering problems caused by sending an ever-growing full message history on every model call.
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 76
last_checkpoint_at: '2026-09-08T14:01:00+08:00'
last_checkpoint_reason: knowledge_event
pending_writeback:
  transaction_id: 20260908T142136+0800-ch01-l1-check-14-attempt-1
  reason: knowledge_event
  phase: prepared
  started_at: '2026-09-08T14:21:36+08:00'
  targets:
    - asset_key: notes.root
      relative_pointer: stage-01/01-llm-message-prompt-langchain.md
      evidence_id: stage-01-ch01-L1-CHECK-14-attempt-1
      operation: upsert
      expected_change: 记录完整 history 持续增长对 token、成本、延迟与 context window 的工程影响，并进入 history 控制策略
      verified: false
      error: null
    - asset_key: qa.stage
      relative_pointer: null
      evidence_id: stage-01-ch01-L1-CHECK-14-attempt-1-ledger
      operation: upsert
      expected_change: 在 Stage 01 Q&A Ledger 记录 L1-CHECK-14 attempt 1 passed
      verified: false
      error: null
chapter_model_profile: TEACH_DEFAULT
chapter_model_profile_source: stage-01/chapter-01
deepseek_route_prompted_for:
- stage-01/chapter-03
- stage-01/chapter-04
- stage-01/chapter-05
last_deepseek_route_decision: stay
code_ability_focus: LLM / Message / Prompt
project_track_status: deferred
project_selection_prompted: true
completed: []
weak_points:
- 需要进一步理解 history 持续增长对 token、成本、延迟和 context window 的影响。
next_action: 完成 L1-CHECK-14 attempt 1：说明每次都发送完整且不断增长的 history 会带来哪些直接工程问题。
next_chapter: curriculum/stage-01/02-structured-output.md
migration_evidence_id: migration-20260819T215842
```
