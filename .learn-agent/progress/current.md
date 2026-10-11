# 当前学习进度

```yaml
schema_version: 2
schema_migration_evidence_id: schema-v2-state
storage_backend: git_repository
stage_id: stage-01
stage_name: LangChain 与 Agent 基础
chapter_id: 03-tool-basics
chapter_file: curriculum/stage-01/03-tool-basics.md
note_pointer: stage-01/03-tool-basics.md
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
last_note_update: 2026-10-11：L3-CHECK-1已理解工具指令不等于执行；L3-CHECK-2复检通过**args关键字参数解包。
last_section: 3.3 LangChain @tool工具声明
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: knowledge_check
  topic: L3-CHECK-3 / attempt 1
  next_action: 识别@tool的name、description、parameters和handler并运行本地工具。
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 147
last_checkpoint_at: '2026-10-11T14:33:07.992Z'
last_checkpoint_reason: needs_review
pending_writeback:
  transaction_id: stage01-ch03-tool-checks-3to5-20261011
  reason: knowledge_event
  phase: prepared
  started_at: '2026-10-11T14:57:15.793Z'
  targets:
  - asset_key: notes.root
    relative_pointer: stage-01/03-tool-basics.md
    evidence_id: stage01-ch03-L3-CHECKS3-5-batch-20261011
    operation: upsert
    expected_change: Record Check3 decorator execution boundary; Check4 missing sku validation; Check5 handler KeyError.
    verified: false
    error: null
  - asset_key: qa.stage
    relative_pointer: null
    evidence_id: stage01-ch03-L3-CHECKS3-5-batch-20261011-ledger
    operation: upsert
    expected_change: Record three accepted checks and next handler error-treatment exercise.
    verified: false
    error: null
chapter_model_profile: TEACH_DEFAULT
chapter_model_profile_source: stage-01/chapter-03
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
- 02-structured-output
weak_points:
- Tool字典解包已复检；下步掌握@tool四部分，注意关键字传参方式与sku:str类型不同。
next_action: L3-CHECK-3：识别装饰器工具四部分与invoke调用时机；之后动手运行。
next_chapter: null
migration_evidence_id: migration-20260819T215842
```
