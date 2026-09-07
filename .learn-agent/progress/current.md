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
last_note_update: 2026-09-07：L1-CHECK-9 attempt 1 needs_review；已识别 SystemMessage，但需补全构造并区分 SystemMessage 与 HumanMessage 职责。
last_section: 1.5 LangChain Messages 映射
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: learning_check
  topic: L1-CHECK-9 attempt 2
  next_action: Provide the complete SystemMessage constructor and distinguish system instructions from user input.
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 70
last_checkpoint_at: '2026-09-07T21:04:00+08:00'
last_checkpoint_reason: recovery
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
- 需要补全 SystemMessage 构造，并区分系统级行为/上下文指令与用户输入。
next_action: 完成 L1-CHECK-9 attempt 2：写出 SystemMessage(content="Answer briefly.")，并说明 SystemMessage 用于系统级行为/上下文指令，HumanMessage 表示用户输入。
next_chapter: curriculum/stage-01/02-structured-output.md
migration_evidence_id: migration-20260819T215842
```
