# Stage 01 — Q&A Ledger

只记录值得跨窗口检索的重要问题、单句结论、entry lifecycle status，以及定位正式笔记/答案与 authoritative verdict 所需的引用信息。本文件只作为 index / navigation aid。

Q&A Ledger 不是 mastery factual authority，不保存第二份 `question_attempt`，也不是 mastery evidence 的第二 source of truth。`status` 只表示 ledger/index lifecycle，取值为 `open | verified`，不表示 `passed`、`accepted` 或 mastery verdict；`answer_ref` 指向正式笔记/答案，authoritative verdict 仅由 `verdict_ref` 指向。`acceptance_snapshot`、`acceptance_results` 与 `passed` 只保存在该 authoritative evidence record 中。

## Entry Schema

```markdown
## Q-YYYYMMDD-<topic-slug>

- chapter_id:
- topic:
- question:
- conclusion:
- status: open | verified
- evidence_id:
- contract_chapter_id:
- question_id:
- attempt:
- answer_ref: `notes/...md#anchor`
- verdict_ref: `<authoritative-question-attempt-reference>`
```

当前暂无条目。
