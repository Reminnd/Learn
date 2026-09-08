# Transactional Learning Persistence

仅在 flush、恢复异常、`/checkpoint`、暂停/完成、schema 迁移、写入失败或状态冲突时读取。普通 buffered teaching turn 使用 `SKILL.md` 与 `shared/checkpoint-batching.md` 的 session-local 规则，不访问 persistence backend。

## 1. 单一真相源与解析器

- storage manifest 决定唯一 primary backend、逻辑资产映射与 persistence runtime policy；Skill 包副本只用于首次初始化。
- 所有运行资产访问都遵循概念操作 `resolve(asset_key, optional_relative_pointer)` 的解析语义。
- `resolve` 必须：确认 key 存在；把目标规范化；确认目标仍在 backend root 内；检查所需读写能力。任一失败即停止，不使用默认目录或 Skill 种子回退。
- 每个真正开始的 transaction 在 write boundary 前、完整 `targets[]` 冻结后，对本 transaction 所需资产及全部目标执行一次完整 resolution 与 boundary validation。
- boundary validation 成功后，同一 transaction 的后续访问直接复用这些已验证的解析结果；不得因 writing 或 final commit phase 重新 resolve 同一目标。这些结果只属于当前 transaction context，不是 cache layer，也不是第二 source of truth。
- `state.current` 是跨聊天唯一 committed Learning State 与最新 committed checkpoint；领域资产保存各自 committed evidence。
- manifest 启用 checkpoint batching 时，当前 live chat 可以维护 session-local working snapshot 与 candidate checkpoint buffer；它们不是 committed source of truth，conversation restart 后不得用于恢复。

初始化或后端切换才读取 `shared/storage-adapters.md`。种子只复制缺失资产，不覆盖已有内容，也不自动多后端双写。

## 2. Teaching Turn、Candidate Checkpoint 与 Transaction 边界

- **teaching turn（教学轮次）**：一次用户输入到一次教学响应的边界。
- **persistence event（持久化事件）**：必须最终保存的语义信息；它不是事务。
- **candidate checkpoint（候选检查点）**：一个 teaching turn 产生的判定、working-state delta、领域事件、稳定 evidence id 与下一教学位置；batching 开启时可以暂存在当前 live session。
- **persistence batch（持久化批次）**：一个或多个 candidate checkpoints 在 flush 时聚合后的提交单位。
- **domain target（领域目标）**：`targets[]` 中一条包含 `asset_key`、指针、`evidence_id`、`operation` 和 `expected_change` 的记录。
- **teaching transaction（教学事务）**：真正开始 WAL 写入的一次事务。batching 关闭时通常对应一个 teaching turn；batching 开启时对应一次 persistence batch flush，而不是每个 teaching turn。
- **prepared WAL write（prepared WAL 写入）**：任何领域写入前，把完整目标集写入 `state.current` 的第一次状态写入。
- **final-state+clear write（最终状态并清 WAL 写入）**：推进最终 committed Learning State 并设置 `pending_writeback=null` 的第二次状态写入。
- **write acknowledgement（写入确认）**：primary backend 对一次 mutation 返回明确成功；对版本化后端可包含 commit/blob SHA，对本地后端可由成功的原子写操作表示。
- **recovery-only turn（仅恢复轮次）**：轮次开始时 WAL 非空、只能恢复既有事务的轮次。
- **committed state（已提交状态）**：全部领域写入成功，且 final-state+clear write 获得明确成功确认后的状态。

### Batching 开启

若 manifest 声明 `checkpoint_batching.enabled=true`：

1. 每个普通 teaching turn 只产生/更新 candidate checkpoint 与 session-local working state。
2. 未达到 flush 条件时不创建 transaction、不写 prepared WAL、不做 persistence remote read/write。
3. candidate 数达到 `max_checkpoints` 或命中 manifest `flush_on` 条件时，将整个 buffer 聚合成一个 persistence batch。
4. flush 时同一领域文件中的多个 checkpoint 变化应尽量合并为一次 target/mutation。
5. 在 prepared WAL write 前冻结完整 aggregated `targets[]`，包括稳定的 transaction id、各 evidence id、操作和预期变化；此后不得再增删目标。
6. flush 成功后，`checkpoint_version` 按本批 candidate checkpoint 数递增，并清空 live-session buffer。

普通 buffered turn 不得因为 assistant turn 变化而重新读取 manifest/state。远端 authoritative refresh 只在 flush 所需未加载内容、冲突、unknown outcome、recovery、integrity reconstruction 或 mastery 需要此前未加载 evidence 时发生。

### Batching 关闭

若 batching 缺失、无效或禁用：

1. 没有持久化事件时创建零个教学事务。
2. 存在一个或多个持久化事件时，一个 teaching turn 最多创建一个新的教学事务，并把完整目标集放入该事务。
3. 在 prepared WAL write 前冻结完整 `targets[]`。
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
- batch transaction 可以包含来自多个 candidate checkpoints 的多个 evidence id。
- `asset_key` 必须存在于 manifest；`relative_pointer` 仅能在该 key 对应 root 内解析。
- 使用 `upsert by evidence_id` 或等价幂等操作；不得无条件重复追加。
- WAL 不复制大段正文，只保存恢复所需目标、意图、ID、验证状态和错误。
- `phase` 的全部枚举值以及 `verified`、`error` 字段继续用于既有 WAL、失败、恢复和迁移。正常成功路径只持久化 `phase=prepared`，不持久化 `writing`、`verifying`、`committing` 中间转换，也不逐目标持久化 `verified=true`。

## 4. 正常成功路径

本节适用于 `pending_writeback=null` 且已经命中 transaction start 条件的情况：batching 关闭时是一个含事件的 teaching turn；batching 开启时是一个需要 flush 的 persistence batch。

成功路径严格为：

1. 聚合本次待提交的全部持久化事件与领域目标，冻结完整 `targets[]`。
2. validate transaction boundary once：对本 transaction 所需资产及全部冻结目标执行一次完整 resolution 与 boundary validation，逐一验证 `asset_key`、`relative_pointer`、backend-root containment 和所需读写能力。任一验证失败即在 WAL 或领域 mutation 前停止。
3. 执行一次 prepared WAL write：以 `phase=prepared` 和稳定的 `transaction_id`、`evidence_id` 把完整 `pending_writeback` 写入 `state.current`；此前不得产生任何领域写入。写接口返回明确成功即视为 prepared WAL 已持久化，不再为同一次成功写入额外回读。
4. 复用第 2 步已验证的解析结果，对 `N` 个聚合后的领域目标各执行一次基于 evidence id 的幂等 upsert。每次写接口返回明确成功即视为该 target 已持久化；正常成功路径不再逐目标回读刚写入的内容。
5. 全部领域写入均明确成功后，在一次 final-state+clear write 中同时推进最终 committed Learning State 并设置 `pending_writeback=null`。batching 开启时 `checkpoint_version` 按本批 candidate checkpoint 数递增。写接口返回明确成功后，本事务成为 committed state，不再追加 final readback。

正常成功路径的最小 I/O 为：

```text
transaction_count=1
state_writes=2
state_verification_reads=0
domain_writes=N
domain_reads=0
```

对于 batching 开启但未触发 flush 的普通 teaching turn：

```text
transaction_count=0
state_writes=0
domain_writes=0
persistence_remote_reads=0
```

正常路径只信任 primary backend 对 mutation 的明确成功确认，不把工具调用前的假设、修改时间或未确认的网络结果当作成功。以下情况才执行额外读取：

- backend 返回结果不明确、超时或连接中断，无法判断 mutation 是否成功；
- optimistic concurrency / SHA 冲突、状态竞争或其他写冲突；
- recovery-only turn，需要判断 WAL target 是否已经落盘；
- integrity reconstruction，需要核对缺失证据；
- mastery-sensitive action 需要读取此前未加载的 committed evidence；
- flush 目标文件在当前 session 从未加载，且 mutation 需要其当前内容；
- 用户明确要求校验或审计。

不得仅为了“验证刚刚成功的写入”重复读取同一文件，也不得为了预防潜在并发在每个 buffered turn 提前刷新 GitHub。

## 5. 崩溃恢复与仅恢复轮次

新聊天启动或必要刷新时发现 `pending_writeback` 非空，则整个轮次都是 recovery-only turn：

1. 仅处理 WAL 中既有的 `transaction_id`、`targets[]`、`evidence_id` 和 `operation`；即使恢复成功，本轮也不得创建新的 persistence transaction。
2. 校验 WAL schema 和所有 manifest key；无效则设置 `integrity.status=needs_reconstruction` 并报告精确缺口。
3. 对每个 target 局部查找原 `evidence_id`。证据已存在时只验证；证据缺失时按原 `operation` 执行幂等 upsert。禁止 blind append。
4. 全部目标已存在或补写成功后，按既有事务的恢复/确认语义推进最终 Learning State 并清空 WAL。final-state+clear mutation 获得明确成功确认即可结束恢复；只有结果不明确时才回读确认实际状态。

恢复路径可以按既有语义使用 `phase`、`verified` 和 `error` 字段；第 4 节的正常成功路径计数不适用于恢复。恢复只加载 manifest 最小映射、`state.current`、WAL 所列目标局部和当前笔记/章节必要区段，不加载旧聊天、全部笔记、全部 Q&A、全部 Bug Book 或全部 ADR。

尚未开始 flush 的 candidate checkpoints 没有 WAL 保护；conversation restart 后它们视为丢失，从最后 committed state 继续。

## 6. 失败语义

- prepared WAL write 失败时，不执行任何领域写入。
- 任一领域目标写入失败时，最终 Learning State 不推进，`pending_writeback` 保持非空，并禁止在本轮开启第二个事务。可在既有 WAL 中记录 `error`，但不得把失败事件当作已保存事实。
- final-state+clear write 失败时，不执行补偿事务，也不创建第二个事务。下一轮读取实际 `state.current` 后进入 recovery 或 confirmation 语义。
- 任一 mutation 的返回结果若不明确，视为 unknown outcome：本轮不得声称已保存；下一轮先读取实际状态，不盲目重试或创建第二事务。
- 只有 primary backend 明确确认 final-state+clear 成功后，才可声称事务已提交。
- batching flush 失败时，已经进入 WAL 的 batch 按 recovery 恢复；不要把同一 batch 拆成新的逐 checkpoint 事务。

## 7. Schema v1 → v2

迁移仍使用现有 WAL schema，并可持久化中间 `phase`、逐目标 `verified` 和 `error`。迁移属于高风险边界，可保留显式内容验证：

1. 以 `reason=migration` 登记状态文件和当前笔记 target。
2. `notes_status` 改为 `lifecycle_status`；状态 `status` 和笔记 Metadata `status` 改为 `learning_status`。
3. 新增 `integrity` 与可重算 `mastery` 对象；旧 mastery 文本不直接作为通过证据。
4. `pending_writeback=[]` 改为 `null`；若旧列表非空，先转为结构化 WAL 并恢复。
5. 必要的迁移内容验证后提交 `schema_version=2` 并清空迁移 WAL。

不得删除或重命名 WAL 字段及 `phase` 枚举值。无法从现存证据确认的内容不得猜测；按 `shared/learning-state-machine.md` 设置 integrity 缺口，重新提问或练习后再恢复 `healthy`。
