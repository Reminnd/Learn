# Transactional Learning Persistence

仅在恢复异常、`/checkpoint`、暂停/完成、schema 迁移、写入失败或状态冲突时读取。普通教学使用 `SKILL.md` 中的提交屏障即可。

## 1. 单一真相源与解析器

- storage manifest 决定唯一 primary backend 和逻辑资产映射；Skill 包副本只用于首次初始化。
- 所有运行资产访问都调用概念操作 `resolve(asset_key, optional_relative_pointer)`。
- `resolve` 必须：确认 key 存在；把目标规范化；确认目标仍在 backend root 内；检查所需读写能力。任一失败即停止，不使用默认目录或 Skill 种子回退。
- `state.current` 是唯一 Learning State 与最新 checkpoint；领域资产保存各自证据，聊天历史不参与冲突仲裁。

初始化或后端切换才读取 `shared/storage-adapters.md`。种子只复制缺失资产，不覆盖已有内容，也不自动多后端双写。

## 2. 教学轮次与聚合边界

- **teaching turn（教学轮次）**：一次用户输入到一次教学响应的边界。
- **persistence event（持久化事件）**：必须保存的语义信息；它不是事务。
- **domain target（领域目标）**：`targets[]` 中一条包含 `asset_key`、指针、`evidence_id`、`operation` 和 `expected_change` 的记录。
- **teaching transaction（教学事务）**：为一个教学轮次的全部持久化事件和领域目标建立的唯一新 WAL 事务。
- **prepared WAL write（prepared WAL 写入）**：任何领域写入前，把完整目标集写入 `state.current` 的第一次状态写入。
- **domain verification read（领域验证读取）**：正常成功路径中，某个目标写入后的唯一一次内容读取。
- **final-state+clear write（最终状态并清 WAL 写入）**：推进最终 Learning State 并设置 `pending_writeback=null` 的第二次状态写入。
- **recovery-only turn（仅恢复轮次）**：轮次开始时 WAL 非空、只能恢复既有事务的轮次。
- **committed state（已提交状态）**：全部目标通过验证，且 final-state+clear write 被回读验证后的状态。

每个教学轮次先聚合本轮产生的全部持久化事件及其全部领域目标，包括 checkpoint、暂停、完成、Bug 和 code-ability 目标。聚合规则如下：

1. 没有持久化事件时创建零个教学事务。
2. 存在一个或多个持久化事件时，最多创建一个新的教学事务，并把完整目标集放入该事务。
3. 在 prepared WAL write 前冻结完整 `targets[]`，包括稳定的 `transaction_id`、`evidence_id`、操作和预期变化；此后不得再增删目标。
4. 禁止按事件或按目标分别开启事务。

## 3. WAL schema

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

- `transaction_id` 与每个 `evidence_id` 稳定且在本学习会话中唯一；重试或恢复不得生成替代 ID。
- `asset_key` 必须存在于 manifest；`relative_pointer` 仅能在该 key 对应 root 内解析。
- 使用 `upsert by evidence_id` 或等价幂等操作；不得无条件重复追加。
- WAL 不复制大段正文，只保存恢复所需目标、意图、ID、验证状态和错误。
- `phase` 的全部枚举值以及 `verified`、`error` 字段继续用于既有 WAL、失败、恢复和迁移。正常成功路径只持久化 `phase=prepared`，不持久化 `writing`、`verifying`、`committing` 中间转换，也不逐目标持久化 `verified=true`。

## 4. 正常成功路径

本节仅适用于轮次开始时 `pending_writeback=null` 且聚合得到 `N >= 1` 个领域目标的教学轮次。成功路径严格为：

1. 聚合全部持久化事件与领域目标，冻结完整 `targets[]`。
2. 执行一次 prepared WAL write：以 `phase=prepared` 和稳定的 `transaction_id`、`evidence_id` 把完整 `pending_writeback` 写入 `state.current`；此前不得产生任何领域写入。
3. 回读一次 `state.current`，逐字段验证 prepared WAL；验证通过前不得产生任何领域写入。
4. 对 `N` 个领域目标各执行一次基于原 `evidence_id` 的幂等 upsert，共 `N` 次领域写入。
5. 对每个目标在写入后执行一次 domain verification read，共 `N` 次领域读取；按内容验证 `evidence_id`、预期变化、关联状态与指针。文件存在、修改时间变化、工具成功消息或修改行数均不构成内容验证。
6. 全部目标验证通过后，在一次原子的 final-state+clear write 中同时推进最终 Learning State 并设置 `pending_writeback=null`。
7. 回读一次 `state.current`，同时验证最终 Learning State 与 WAL 已清空。正常成功路径在 final-state+clear write 后不再读取领域证据。

准确计数为：

```text
transaction_count=1
state_writes=2
state_verification_reads=2
domain_writes=N
domain_reads=N
```

只有第 7 步通过后才能称为 committed state，并向用户声称已保存或已提交。

## 5. 崩溃恢复与仅恢复轮次

轮次开始时发现 `pending_writeback` 非空，则整个轮次都是 recovery-only turn：

1. 仅处理 WAL 中既有的 `transaction_id`、`targets[]`、`evidence_id` 和 `operation`；即使恢复成功，本轮也不得创建新的教学事务。
2. 校验 WAL schema 和所有 manifest key；无效则设置 `integrity.status=needs_reconstruction` 并报告精确缺口。
3. 对每个 target 局部查找原 `evidence_id`。证据已存在时只验证；证据缺失时按原 `operation` 执行幂等 upsert 后验证。禁止 blind append。
4. 全部领域目标验证通过后，按既有事务的恢复/确认语义推进最终 Learning State、清空 WAL 并回读确认。

恢复路径可以按既有语义使用 `phase`、`verified` 和 `error` 字段；第 4 节的正常成功路径计数不适用于恢复。恢复只加载 manifest 最小映射、`state.current`、WAL 所列目标局部和当前笔记/章节必要区段，不加载旧聊天、全部笔记、全部 Q&A、全部 Bug Book 或全部 ADR。

## 6. 失败语义

- 任一 WAL 写入/验证、领域写入/验证或最终状态写入/验证失败，都不得声称已保存或已提交。
- prepared WAL 回读验证失败时，不执行任何领域写入。
- 领域目标写入或验证失败时，最终 Learning State 不推进，`pending_writeback` 保持非空，并禁止在本轮开启第二个事务。可在既有 WAL 中记录 `error`，但不得把失败事件当作已保存事实。
- final-state+clear write 或其最终回读失败时，不执行补偿事务，也不创建第二个事务。下一轮先确定 `state.current` 的实际状态，再遵循恢复或确认语义。

## 7. Schema v1 → v2

迁移仍使用现有 WAL schema，并可持久化中间 `phase`、逐目标 `verified` 和 `error`：

1. 以 `reason=migration` 登记状态文件和当前笔记 target。
2. `notes_status` 改为 `lifecycle_status`；状态 `status` 和笔记 Metadata `status` 改为 `learning_status`。
3. 新增 `integrity` 与可重算 `mastery` 对象；旧 mastery 文本不直接作为通过证据。
4. `pending_writeback=[]` 改为 `null`；若旧列表非空，先转为结构化 WAL 并恢复。
5. 回读验证后提交 `schema_version=2` 并清空迁移 WAL。

不得删除或重命名 WAL 字段及 `phase` 枚举值。无法从现存证据确认的内容不得猜测；按 `shared/learning-state-machine.md` 设置 integrity 缺口，重新提问或练习后再恢复 `healthy`。
