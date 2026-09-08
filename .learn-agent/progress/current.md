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
last_note_update: 2026-09-08：Canonical Q2 attempt 3 needs_review；原理侧抽象已基本正确，LangChain 侧需修正为运行时变量进入 ChatPromptTemplate，再由 Messages 进入 chat_model。
last_section: Canonical Mastery Q&A
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: learning_check
  topic: Q2 attempt 4 (canonical mastery)
  next_action: Rewrite only the LangChain data flow: runtime inputs → ChatPromptTemplate → ChatPromptValue/Messages → chat_model.invoke(messages) → AIMessage.
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 83
last_checkpoint_at: '2026-09-08T15:27:33+08:00'
last_checkpoint_reason: knowledge_event
pending_writeback:
  transaction_id: stage-01-ch01-Q2-attempt-4
  status: prepared
  targets:
  - learning/notes/stage-01/01-llm-message-prompt-langchain.md
  - learning/qa/stage-01.md
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
- Canonical Q2：LangChain 侧需要明确运行时变量先进入 `ChatPromptTemplate`，得到 `ChatPromptValue / Messages`，再进入 `chat_model.invoke(messages)`；如果写成 `chain = prompt | model`，则 `chain.invoke(...)` 的参数仍是运行时变量。
next_action: 完成 canonical mastery Q2 attempt 4：只写 LangChain 数据流 `user input / variables → ChatPromptTemplate → ChatPromptValue / Messages → chat_model.invoke(messages) → AIMessage`。
next_chapter: curriculum/stage-01/02-structured-output.md
migration_evidence_id: migration-20260819T215842
```
