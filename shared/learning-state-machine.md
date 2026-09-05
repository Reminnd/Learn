# Learning State Machine

仅在初始化、schema 迁移、状态冲突、恢复或掌握判定时读取。普通教学直接使用已验证的 `state.current` 最小字段。

## Schema v2

```yaml
schema_version: 2
chapter:
  stage_id: stage-01
  chapter_id: 01-llm-message-prompt-langchain
  chapter_file: curriculum/stage-01/01-llm-message-prompt-langchain.md
  note_pointer: stage-01/01-llm-message-prompt-langchain.md
lifecycle_status: initialized | active | consolidated
learning_status: not_started | learning | practice | qa | needs_review | mastered
integrity:
  status: healthy | needs_reconstruction
  missing: []
  reason: null
mastery:
  score: null
  critical_questions_passed: false
  dimension_floors_passed: false
  required_exercises_passed: false
  unresolved_critical_misconceptions: 0
  mastered: false
pending_writeback: null
```

会话位置、模式、`return_to`、checkpoint、薄弱点、模型档位和 Project Track 字段可与上面字段并列；不要复制 manifest 的物理路径映射到多个状态字段。`chapter_file` 是 Skill 内只读教材指针；`note_pointer` 是 manifest 的 `notes.root` 下相对指针，解析后必须仍在 primary backend root 内。

## 字段职责

- `lifecycle_status`：笔记资产生命周期。初始化种子为 `initialized`；出现有效知识事件后为 `active`；章节掌握且笔记已压缩为稳定总结后为 `consolidated`。
- `learning_status`：学习进程。只允许状态机中的值。
- `integrity`：持久化证据是否完整可信。`needs_reconstruction` 只能出现在 `integrity.status`。
- `mastery`：由证据重算的派生结果，不能手工凭印象设置。

当前笔记 Metadata 必须至少包含 `schema_version`、`stage_id`、`chapter_id`、`lifecycle_status`、`learning_status` 和 `last_updated`。状态文件与笔记只比较同名维度，不比较生命周期和学习进程是否“相等”。

## 学习状态转换

```text
not_started → learning → practice → qa → mastered
                    ↑         ↓
                    └── needs_review
```

`mastered` 仅由 mastery predicate 得出。`lifecycle_status=consolidated` 只允许在 `learning_status=mastered` 且笔记已完成压缩后设置；其他学习状态通常对应 `active`。

## 完整性恢复

状态引用的 Q&A、练习或知识结果在领域资产中不存在时：

1. 设置 `integrity.status=needs_reconstruction`。
2. 在 `missing` 中保存稳定 evidence ID 或精确缺口，在 `reason` 中保存可核验原因。
3. 禁止依据缺失证据判定 mastered。
4. 只从现存笔记、Q&A、Bug Book、Code Ability、ADR 与当前明确对话重建。
5. 无法重建的内容重新提问或重新练习；验证后才恢复 `healthy`。

## 从 v1 迁移

- `notes_status=initialized | active | consolidated` → `lifecycle_status`。
- `status` → `learning_status`，其中 `not_started` 保持不变。
- 笔记 Metadata 的旧 `status` → `learning_status`；根据是否已有有效知识内容设置 `lifecycle_status`。
- 旧 `mastery` 文本只作历史说明，不直接产生 `mastered=true`；按新 rubric 重算。
- `pending_writeback=[]` → `pending_writeback: null`；非空旧列表先转为 WAL transaction，再恢复。

迁移本身也必须走 WAL：先登记迁移目标，逐项更新并验证，最后提交 schema_version 2 和清空 WAL。
