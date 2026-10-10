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
last_note_update: 2026-10-10：L2-CHECK-7 attempt 1 部分正确，混淆 parsed=None 与字段缺失，误将 raw 作为可信数据；已纠正并安排复检。
last_section: 2.7 Structured Output 解析失败与可靠性
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: knowledge_check
  topic: L2-CHECK-7 / attempt 2
  next_action: 复检解析失败时 parsed=None 的安全访问条件，以及 raw 不可绕过 Schema 校验的原因。
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 99
last_checkpoint_at: '2026-10-10T06:57:44.154Z'
last_checkpoint_reason: knowledge_event
pending_writeback: null
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
- LangChain Structured Output 解析失败时 parsed 仍存在但为 None；raw 未通过校验不可直接用于业务。
next_action: L2-CHECK-7 attempt 2，正确判定 parsed 并处理 parsing_error，再继续有限重试与可靠性测试。
next_chapter: null
migration_evidence_id: migration-20260819T215842
```
