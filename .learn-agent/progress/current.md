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
last_note_update: 2026-09-08：Canonical Q1 attempt 2 通过；结合 attempt 1 的失败条件与本次分层断点定位因果关系，正式 Q1 acceptance 已满足。
last_section: Canonical Mastery Q&A
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: learning_check
  topic: Q2 attempt 1 (canonical mastery)
  next_action: Explain the principle-to-framework mapping from native model invocation to LangChain ChatModel, including corresponding objects, input, output, and key data flow.
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 80
last_checkpoint_at: '2026-09-08T14:41:10+08:00'
last_checkpoint_reason: knowledge_event
pending_writeback:
  transaction_id: 20260908T144110+0800-ch01-q2-attempt-1
  reason: knowledge_event
  phase: prepared
  started_at: '2026-09-08T14:41:10+08:00'
  targets:
    - asset_key: notes.root
      relative_pointer: stage-01/01-llm-message-prompt-langchain.md
      evidence_id: stage-01-ch01-Q2-attempt-1
      operation: upsert
      expected_change: 记录 canonical Q2 attempt 1 needs_review；对象与输入输出基本正确，但关键数据流错误
      verified: false
      error: null
    - asset_key: qa.stage
      relative_pointer: null
      evidence_id: stage-01-ch01-Q2-attempt-1-ledger
      operation: upsert
      expected_change: 在 Stage 01 Q&A Ledger 记录 canonical Q2 attempt 1 needs_review
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
- Canonical Q2：需要把原生 model(messages) 与 LangChain ChatModel.invoke(messages) 的关键数据流方向完整说清；AIMessage 是模型输出，不是运行时变量，也不会自动再传回 model 生成用户消息。
next_action: 完成 canonical mastery Q2 attempt 2：只重写正确数据流，保持原理侧与 LangChain 侧对象/输入/输出映射不变。
next_chapter: curriculum/stage-01/02-structured-output.md
migration_evidence_id: migration-20260819T215842
```
