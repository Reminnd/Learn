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
last_note_update: 2026-10-11：L3-CHECK-9 attempt1获取Tool Call参数字典正确，但把LangChain StructuredTool当普通Python函数传递**kwargs；已说明调用需使用invoke。
last_section: 3.7 Tool对象invoke与普通handler区别
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: knowledge_check
  topic: L3-CHECK-9 / attempt 2
  next_action: 复检LangChain工具对象的invoke接口与原生Python函数handler(**args)的差别；之后运行工具并返回ToolMessage。
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 155
last_checkpoint_at: '2026-10-11T15:39:47.307Z'
last_checkpoint_reason: needs_review
pending_writeback:
  transaction_id: stage01-ch03-l3-check9-a2-20261011
  reason: needs_review
  phase: prepared
  started_at: '2026-10-11T15:44:27.290Z'
  targets:
  - asset_key: notes.root
    relative_pointer: stage-01/03-tool-basics.md
    evidence_id: stage01-ch03-L3-CHECK-9-attempt2-20261011
    operation: upsert
    expected_change: Record L3-CHECK-9 attempt2 needs_review: wrong invoke keyword unpacking and expected ToolMessage instead of int.
    verified: false
    error: null
  - asset_key: qa.stage
    relative_pointer: null
    evidence_id: stage01-ch03-L3-CHECK-9-attempt2-qa-20261011
    operation: upsert
    expected_change: Track incorrect Tool.invoke arguments and result type; repeat targeted check.
    verified: false
    error: null
  - asset_key: bugs.book
    relative_pointer: null
    evidence_id: stage01-ch03-tool-invoke-kwargs-toolmessage-20261011
    operation: upsert
    expected_change: Document difference between invoke(args_dict) and invoke(complete_tool_call).
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
- 需要独立区分LangChain StructuredTool.invoke(args_dict)与原生Python handler(**args)；再学习ToolMessage的tool_call_id关联。
next_action: L3-CHECK-9 attempt2：使用selected_tool.invoke(call['args'])执行LangChain工具，复检返回库存12。
next_chapter: null
migration_evidence_id: migration-20260819T215842
```
