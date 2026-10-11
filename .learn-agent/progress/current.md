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
last_note_update: 2026-10-11：从已掌握Chapter02按canonical课程索引切入Chapter03 Tool基础；开始3.1 Python工具函数、name/description/parameters/handler与执行边界。
last_section: 3.1 工具调用最小原理与执行边界
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: knowledge_check
  topic: L3-CHECK-1 / attempt 1
  next_action: 解释LLM仅提出tool call而运行时没有执行handler为何不能得到业务真实库存。
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 144
last_checkpoint_at: '2026-10-11T14:12:41.831Z'
last_checkpoint_reason: chapter_boundary
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
- Chapter03尚未掌握：需要建立tool name/description/parameters/handler及模型选择与Python执行的边界；保留Chapter02 raw/parsed类型区分作为轻量复习。
next_action: L3-CHECK-1 attempt1：模型只提出get_stock的工具调用但程序未执行，是否能获得真实库存、为什么。
next_chapter: null
migration_evidence_id: migration-20260819T215842
```
