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
last_note_update: 2026-09-07：L1-CHECK-7 attempt 1 通过；已说明 run_turn 中三类消息变量的职责与完整数据流。
last_section: 1.5 LangChain Messages 映射
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: learning_check
  topic: L1-CHECK-8 attempt 1
  next_action: Map handwritten user/assistant Message roles to LangChain HumanMessage and AIMessage.
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 68
last_checkpoint_at: '2026-09-07T21:53:54+09:00'
last_checkpoint_reason: knowledge_event
pending_writeback:
  transaction_id: 20260907T215916+0900-ch01-l1-check-8
  reason: knowledge_event
  phase: prepared
  started_at: '2026-09-07T21:59:16+09:00'
  targets:
    - asset_key: notes.root
      relative_pointer: stage-01/01-llm-message-prompt-langchain.md
      evidence_id: stage-01-ch01-L1-CHECK-8-attempt-1
      operation: upsert
      expected_change: 记录手写 user/assistant Message 到 LangChain HumanMessage/AIMessage 的映射
      verified: false
      error: null
    - asset_key: qa.stage
      relative_pointer: null
      evidence_id: stage-01-ch01-L1-CHECK-8-attempt-1-ledger
      operation: upsert
      expected_change: 在 Stage 01 Q&A Ledger 记录 L1-CHECK-8 attempt 1 passed
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
- 需要建立手写 Message role 与 LangChain Message 类型的对应关系。
next_action: 完成 L1-CHECK-8 attempt 1：说明手写 user/assistant Message 分别对应 LangChain 的 HumanMessage / AIMessage。
next_chapter: curriculum/stage-01/02-structured-output.md
migration_evidence_id: migration-20260819T215842
```
