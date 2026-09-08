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
  critical_questions_passed: true
  dimension_floors_passed: false
  required_exercises_passed: false
  unresolved_critical_misconceptions: 0
  mastered: false
last_note_update: 2026-09-08：Canonical Q3 attempt 1 通过；已给出 Message history 增长的可执行排查顺序，并说明 summary + recent history 的细节失真 Trade-off；继续补充学习 sliding window。
last_section: Canonical Mastery Q&A
teaching_mode: teacher
mode_prompted_for: []
learning_session_id: learn-agent-main
session_mode: learning
session_status: active
current_activity: learning
return_to:
  activity: required_exercise
  topic: EX1
  next_action: Run examples/stage-01/ex1_message_prompt_langchain.py and verify the six exact acceptance output lines.
resume_contract:
  auto_resume: true
  continue_from_checkpoint: true
  require_user_confirmation: false
checkpoint_version: 85
last_checkpoint_at: '2026-09-08T15:52:20+08:00'
last_checkpoint_reason: qa_complete
pending_writeback:
  transaction_id: 20260908T162300+0800-ch01-ex1-mastery
  reason: exercise_complete
  phase: prepared
  started_at: 2026-09-08T16:23:00+08:00
  targets:
  - asset_key: notes.root
    relative_pointer: stage-01/01-llm-message-prompt-langchain.evidence.yaml
    evidence_id: stage-01-ch01-mastery-evidence-bundle-q1a2-q2a4-q3a1-ex1a1
    operation: upsert
    expected_change: Persist structured latest-valid Q1/Q2/Q3 evidence, EX1 acceptance evidence, and the Chapter 01 mastery assessment.
    verified: false
    error: null
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
- Sliding window：需要继续巩固“只控制本轮送入模型的最近上下文，不等于删除持久化聊天记录”的边界。
next_action: 完成 required exercise EX1：运行 examples/stage-01/ex1_message_prompt_langchain.py，并验证 canonical acceptance 要求的六条精确输出。
next_chapter: curriculum/stage-01/02-structured-output.md
migration_evidence_id: migration-20260819T215842
```
