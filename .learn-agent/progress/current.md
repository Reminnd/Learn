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
last_note_update: 2026-10-12：L3-CHECK-15实际运行双工具成功：get_stock=12，get_price=199，DeepSeek最终回答正确。
last_section: 3.13 多工具异常隔离
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: knowledge_check
  topic: L3-CHECK-16 / attempt 1
  next_action: 分析循环首个库存工具抛KeyError之后，价格工具与最终模型回答是否继续执行。
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 165
last_checkpoint_at: '2026-10-12T10:46:00+08:00'
last_checkpoint_reason: section_boundary
pending_writeback:
  transaction_id: stage01-ch03-L3-check16-18-20261012
  reason: knowledge_event
  phase: prepared
  started_at: '2026-10-12T10:46:00+08:00'
  targets:
  - asset_key: notes.root
    relative_pointer: stage-01/03-tool-basics.md
    evidence_id: stage01-ch03-L3-check16-18-20261012
    operation: upsert
    expected_change: Save exercise results.
    verified: false
    error: null
  - asset_key: qa.stage
    relative_pointer: null
    evidence_id: stage01-ch03-L3-check16-18-qa-20261012
    operation: upsert
    expected_change: Save exercise results.
    verified: false
    error: null
  - asset_key: bugs.book
    relative_pointer: null
    evidence_id: stage01-ch03-L3-check18-keyerror-before-try-20261012
    operation: upsert
    expected_change: Save exercise results.
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
- 已实测成功的双工具调用；待学习单工具异常时的错误隔离和回填。
next_action: L3-CHECK-16：分析多Tool Call中第一条执行失败引发异常时，后续工具和模型调用的执行行为。
next_chapter: null
migration_evidence_id: migration-20260819T215842
```
