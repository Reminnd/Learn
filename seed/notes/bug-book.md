# Bug Book（错题本 / 调试本）

> 只记录可复用的错误模式，不记录聊天流水账。默认按需读取当前主题或最近条目，不要每次全部加载。

## 状态

- `open`：仍容易犯错，需要复习；`resolution_evidence_id=null`
- `improving`：已纠正，但还需要再次验证；`resolution_evidence_id=null`
- `resolved`：已通过后续练习 / Q&A 验证；`resolution_evidence_id` 必须是 valid matching resolution evidence ID

`status` 只能取以上三个值。仅当误解与 critical question acceptance 或核心模型直接冲突时，才设置 `critical: true`。

`resolved` 只有在 resolution evidence 已通过 S03 domain verification、进入 committed state，并匹配当前 `contract_chapter_id` 与该 `misconception_id` 时才有效。若条目有 `question_id`，evidence 还必须与对应 question/core-model 的原误解相关；其内容必须具体证明该误解已经解决。

`status=resolved` 但 `resolution_evidence_id=null`，或 resolution evidence 不存在、未 verified、未 committed、不匹配或无法证明误解已解决时，不得视为 resolved。Mastery 计算必须使用 `effective_status=improving`，该 misconception 仍是 unresolved。

## 条目模板

```markdown
### BUG-YYYYMMDD-NN — 简短标题

- misconception_id:
- contract_chapter_id:
- question_id:
- critical: <boolean>
- status: open | improving | resolved
- source_evidence_id:
- resolution_evidence_id: <null-for-open-or-improving|required-valid-resolution-evidence-id-for-resolved>
- 日期：
- Stage / Chapter：
- 类型：Q&A | Code | Debug | Architecture | Trade-off
- 关联知识点：
- 复现/触发：

**错误 / 症状**

...

**当时的错误理解**

...

**根因**

...

**正确模型 / 修复**

...

**如何避免再次发生**

...

**验证证据**

- 尚未验证 / 后续哪道题或哪次代码已验证
```

## Active Mistakes（当前需要优先复习）

暂无。

## Resolved（已解决）

暂无。
