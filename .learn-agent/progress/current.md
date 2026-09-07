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
last_note_update: 2026-09-07：L1-CHECK-10 attempt 1 通过；确认 ChatPromptTemplate.invoke 的 Message 类型与变量替换结果，并进入 Runnable 组合。
last_section: 1.7 Runnable：把 Prompt 与 Chat Model 串起来
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: learning_check
  topic: L1-CHECK-11 attempt 1
  next_action: Distinguish the output responsibility of prompt.invoke from (prompt | model).invoke.
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 72
last_checkpoint_at: '2026-09-07T21:23:38+08:00'
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
- 需要区分 Prompt 单独 invoke 只构造模型输入，与 Runnable 链 invoke 会继续调用 Chat Model。
next_action: 完成 L1-CHECK-11 attempt 1：说明 prompt.invoke(...) 与 (prompt | model).invoke(...) 分别返回什么，以及哪个步骤真正调用 model。
next_chapter: curriculum/stage-01/02-structured-output.md
migration_evidence_id: migration-20260819T215842
```
