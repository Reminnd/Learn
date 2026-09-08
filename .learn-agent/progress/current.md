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
last_note_update: 2026-09-08：Canonical Q2 attempt 1 needs_review；对象、输入与输出映射正确，但关键数据流把 AIMessage 错当成运行时变量并再次传回 model，需复检数据流方向。
last_section: Canonical Mastery Q&A
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: learning_check
  topic: Q2 attempt 2 (canonical mastery)
  next_action: Rewrite only the correct principle-side and LangChain-side data flows; retain the already-correct object/input/output mapping from attempt 1.
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 81
last_checkpoint_at: '2026-09-08T14:41:10+08:00'
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
- Canonical Q2：需要把原理侧与 LangChain 侧的数据流终点明确写到 assistant_message / AIMessage；AIMessage 是模型输出，不是运行时变量，除非应用显式保存并在下一轮重新组合，否则不会自动再次进入 model。
next_action: 完成 canonical mastery Q2 attempt 2：只写两条正确数据流，原理侧 user input/variables → prompt construction → list[Message] → model(messages) → assistant_message；LangChain 侧 user input/variables → ChatPromptTemplate → ChatPromptValue/Messages → chat_model.invoke(messages) → AIMessage。
next_chapter: curriculum/stage-01/02-structured-output.md
migration_evidence_id: migration-20260819T215842
```
