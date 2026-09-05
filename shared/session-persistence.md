# Transactional Learning Persistence

仅在恢复异常、`/checkpoint`、暂停/完成、schema 迁移、写入失败或状态冲突时读取。普通教学使用 `SKILL.md` 中的提交屏障即可。

## 1. 单一真相源与解析器

- storage manifest 决定唯一 primary backend 和逻辑资产映射；Skill 包副本只用于首次初始化。
- 所有运行资产访问都调用概念操作 `resolve(asset_key, optional_relative_pointer)`。
- `resolve` 必须：确认 key 存在；把目标规范化；确认目标仍在 backend root 内；检查所需读写能力。任一失败即停止，不使用默认目录或 Skill 种子回退。
- `state.current` 是唯一 Learning State 与最新 checkpoint；领域资产保存各自证据，聊天历史不参与冲突仲裁。

初始化或后端切换才读取 `shared/storage-adapters.md`。种子只复制缺失资产，不覆盖已有内容，也不自动多后端双写。

## 2. WAL schema

`pending_writeback` 是 Write-Ahead Log（预写日志），必须为 `null` 或以下对象：

```yaml
pending_writeback:
  transaction_id: 20260819T194231+0800-ch01-q2
  reason: knowledge_event | qa_complete | exercise_complete | debug_resolved | manual | pause | completion | recovery | migration
  phase: prepared | writing | verifying | committing
  started_at: 2026-08-19T19:42:31+08:00
  targets:
    - asset_key: notes.root
      relative_pointer: stage-01/01-llm-message-prompt-langchain.md
      evidence_id: stage-01-ch01-Q2-attempt-2
      operation: upsert
      expected_change: 校准 Prompt 构造配置与运行时输入边界
      verified: false
      error: null
```

规则：

- `transaction_id` 与每个 `evidence_id` 稳定且在本学习会话中唯一。
- `asset_key` 必须存在于 manifest；`relative_pointer` 仅能在该 key 对应 root 内解析。
- 使用 `upsert by evidence_id` 或等价幂等操作；不得无条件重复追加。
- WAL 不复制大段正文，只保存恢复所需目标、意图、ID、验证状态和错误。

## 3. 正常提交

1. 从本轮提取最小知识增量、目标与稳定 evidence ID；不改任何领域资产。
2. 把完整 WAL 以 `phase=prepared` 写入 `state.current`，回读并逐字段确认。
3. 设置 `phase=writing`；逐个解析 manifest key 并幂等写入领域资产。
4. 设置 `phase=verifying`；局部回读每个目标，验证 evidence ID、预期知识内容、关联状态与指针，逐项设 `verified=true`。
5. 所有目标验证后设置 `phase=committing`，提交位置、学习状态、mastery 派生值、薄弱点、下一步、checkpoint 版本与原因。
6. 回读状态和所引用证据，确认一致后将 `pending_writeback` 设为 `null`，再回读确认。

文件存在、修改时间变化、工具成功消息或修改行数都不构成内容验证。

## 4. 崩溃恢复

启动时发现 WAL 非空，禁止开启新教学事务：

1. 校验 WAL schema 和所有 manifest key；无效则设置 `integrity.status=needs_reconstruction` 并报告精确缺口。
2. 对每个 target 局部查找 evidence ID。已存在者只验证，不重复追加；不存在者按 `operation` 继续幂等写入。
3. 所有领域资产验证后，重新执行提交步骤并回读。
4. 只有状态与证据一致时清空 WAL。

某个目标不可写或验证失败时，保留 WAL、记录 `error`，停止推进持久化状态。可以回答用户当前问题，但不得把失败的事件当作已保存事实。

## 5. 一致性与重建

在恢复、下一道 Q&A、切换小节或 mastery 判定前，检查：

- `state.current` 的 evidence 引用在对应领域资产中存在；
- 状态与笔记的 `lifecycle_status`、`learning_status` 分别一致；
- `pending_writeback == null`；
- 所有运行指针均由 manifest key 解析且位于 backend root 内。

无法从现存证据确认的内容不得猜测。按 `shared/learning-state-machine.md` 设置 integrity 缺口；重新提问或练习后再恢复 `healthy`。

## 6. Schema v1 → v2

迁移也是事务：

1. 以 `reason=migration` 登记状态文件和当前笔记 target。
2. `notes_status` 改为 `lifecycle_status`；状态 `status` 和笔记 Metadata `status` 改为 `learning_status`。
3. 新增 `integrity` 与可重算 `mastery` 对象；旧 mastery 文本不直接作为通过证据。
4. `pending_writeback=[]` 改为 `null`；若旧列表非空，先转为结构化 WAL 并恢复。
5. 回读验证后提交 `schema_version=2` 并清空迁移 WAL。

## 7. 最小恢复上下文

恢复只加载 manifest 最小映射、`state.current`、WAL 列出的目标局部和当前笔记/章节必要区段。不要加载旧聊天、全部笔记、全部 Q&A、全部 Bug Book 或全部 ADR。
