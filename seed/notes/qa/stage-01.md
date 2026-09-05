# Stage 01 — Q&A Ledger

只记录值得跨窗口检索的重要问题。完整解释归入对应课程笔记，本文件只作为 index / navigation aid，保留定位 answer/note 与 authoritative verdict 所需的引用信息。

Q&A Ledger 不是 mastery factual authority，不保存第二份 `question_attempt`，也不是 mastery evidence 的第二 source of truth。`acceptance_snapshot`、`acceptance_results` 与 `passed` 只保存在 `verdict_ref` 指向的 authoritative evidence record 中。

## Entry Schema

```markdown
## Q-YYYYMMDD-<topic-slug>

- chapter_id:
- topic:
- question:
- evidence_id:
- contract_chapter_id:
- question_id:
- attempt:
- answer_ref: `notes/...md#anchor`
- verdict_ref: `<authoritative-question-attempt-reference>`
```

当前暂无条目。
