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
last_note_update: 2026-09-08：L1-CHECK-12 attempt 1 通过；确认同一个 Runnable chain 不会自动提供跨调用记忆，并进入 Message 历史增长。
last_section: 1.8 Message 历史增长
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: learning_check
  topic: L1-CHECK-13 attempt 1
  next_action: Calculate how history length grows when each turn appends one HumanMessage and one AIMessage.
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 74
last_checkpoint_at: '2026-09-08T14:00:53+08:00'
last_checkpoint_reason: knowledge_event
pending_writeback: null
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
next_action: 完成 L1-CHECK-13 attempt 1：计算每轮新增一条 HumanMessage 和一条 AIMessage 时 history 长度如何增长。
next_chapter: curriculum/stage-01/02-structured-output.md
migration_evidence_id: migration-20260819T215842
```
