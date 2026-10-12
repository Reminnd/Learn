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
learning_status: practice
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
last_note_update: 2026-10-12：EX1 Part2必填字段校验复检通过；Part3初次类型校验未使用not导致条件反向，待针对性复检。
last_section: Chapter03 EX1 Part3：类型校验失败条件
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: practice
return_to:
  activity: knowledge_check
  topic: Chapter03-EX1 / part 3 attempt 2
  next_action: 判断正确的not isinstance(...)条件在sku为合法字符串时是否会抛TypeError。
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 193
last_checkpoint_at: '2026-10-12T11:46:41.291Z'
last_checkpoint_reason: needs_review
pending_writeback: null
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
- EX1 Part2必填字段检查已通过，需掌握if not isinstance(...)按类型不符合要求时抛异常，再完成handler分派与@tool框架映射。
next_action: EX1 Part3 attempt2：预测not isinstance对正确SKU类型的判断结果，之后实现原理版Runtime handler并验证。
next_chapter: null
migration_evidence_id: migration-20260819T215842
```
