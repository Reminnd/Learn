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
last_note_update: 2026-10-11：L3-CHECK-3/4/5均通过：@tool声明与invoke执行边界、参数缺失校验在handler前、合法SKU格式但不存在触发业务KeyError。
last_section: 3.4 工具输入Schema与handler业务异常
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: knowledge_check
  topic: L3-CHECK-6 / attempt 1
  next_action: 为get_stock函数设计try/except，区分KeyError业务错误和ValidationError输入校验错误，并返回稳定业务错误。
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 150
last_checkpoint_at: '2026-10-11T14:57:15.793Z'
last_checkpoint_reason: knowledge_event
pending_writeback:
  transaction_id: stage01-ch03-description-review-20261011
  reason: needs_review
  phase: prepared
  started_at: '2026-10-11T15:04:51.807Z'
  targets:
  - asset_key: notes.root
    relative_pointer: stage-01/03-tool-basics.md
    evidence_id: stage01-ch03-check6-check7-20261011
    operation: upsert
    expected_change: Record L3-CHECK-6 pass and L3-CHECK-7 partial tool-description answer.
    verified: false
    error: null
  - asset_key: qa.stage
    relative_pointer: null
    evidence_id: stage01-ch03-check6-check7-20261011-ledger
    operation: upsert
    expected_change: Record L3-CHECK-6 passed and L3-CHECK-7 needs_review.
    verified: false
    error: null
  - asset_key: bugs.book
    relative_pointer: null
    evidence_id: stage01-ch03-stock-description-too-broad-20261011
    operation: upsert
    expected_change: Record overly broad stock tool description.
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
- @tool声明与执行、参数校验与业务查询边界已通过局部检查；后续需练习有结构的业务错误响应及LangChain的异常处理策略。
next_action: L3-CHECK-6：用try/except处理get_stock未知SKU的KeyError，理解不能把业务错误当作参数ValidationError。
next_chapter: null
migration_evidence_id: migration-20260819T215842
```
