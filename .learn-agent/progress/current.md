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
learning_status: qa
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
last_note_update: 2026-10-12：Chapter03 Q2 critical通过：区分Tool args_schema与LLM结构化输出，掌握name路由、invoke校验、handler执行、ToolMessage回填；进入Q3。
last_section: Chapter03正式验收 Q3 — 参数错误排查与Trade-off
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: qa
return_to:
  activity: knowledge_check
  topic: Chapter03-Q3 / attempt 1
  next_action: 排查get_price Tool Call错误参数字段product_id，提出可执行排查顺序和一种修复Trade-off。
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 183
last_checkpoint_at: '2026-10-12T07:25:46.738Z'
last_checkpoint_reason: section_boundary
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
- Chapter03 Q1、Q2关键题已通过；仍需正式验收Q3参数错误排查和EX1必做练习，再按掌握度评分规则决定mastered。
next_action: Chapter03 Q3 attempt1：面对get_price.invoke({'product_id':'KB-001'})抛ValidationError，说明分阶段排查顺序、修复方案与一项Trade-off。
next_chapter: null
migration_evidence_id: migration-20260819T215842
```
