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
last_note_update: 2026-10-12：L3-CHECK-16和17通过；L3-CHECK-18发现未知工具键读取发生在try外，需复检dict.get与KeyError。
last_section: 3.15 未知工具查表与异常边界
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: knowledge_check
  topic: L3-CHECK-18 / attempt 2
  next_action: 检查未知工具名称时dict.get返回None与if None分支，巩固异常位置。
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 168
last_checkpoint_at: '2026-10-12T10:46:00+08:00'
last_checkpoint_reason: needs_review
pending_writeback:
  transaction_id: stage01-ch03-check18a2-check19a1-20261012
  reason: knowledge_event
  phase: prepared
  started_at: '2026-10-12T03:16:56.908Z'
  targets:
  - asset_key: notes.root
    relative_pointer: stage-01/03-tool-basics.md
    evidence_id: stage01-ch03-check18a2-19a1-notes-20261012
    operation: upsert
    expected_change: Record successful missing-tool lookup check and follow-up misconception about repeated model retries.
    verified: false
    error: null
  - asset_key: qa.stage
    relative_pointer: null
    evidence_id: stage01-ch03-check18a2-19a1-qa-20261012
    operation: upsert
    expected_change: Record check18 passed and check19 needs review.
    verified: false
    error: null
  - asset_key: bugs.book
    relative_pointer: null
    evidence_id: stage01-ch03-unknown-tool-continue-unpaired-20261012
    operation: upsert
    expected_change: Record missing ToolMessage cannot be assumed to produce retry loop.
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
- L3-CHECK-18需区分dict[key]的KeyError与dict.get(key)的None，并注意try覆盖范围。
next_action: L3-CHECK-18 attempt2：若tools_by_name.get('delete_product')返回None，判断接下来if None的行为。
next_chapter: null
migration_evidence_id: migration-20260819T215842
```
