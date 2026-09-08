# Checkpoint Batching

本文件定义启用 checkpoint batching 时的教学运行策略。它不仅改变**何时 flush**，也改变普通教学回合是否访问远端 backend：在 batching 开启且未触发 flush 时，普通回合不得为了持久化重复读取或写入 GitHub。

## 1. 默认策略

运行时 manifest 若声明：

```yaml
persistence:
  checkpoint_batching:
    enabled: true
    max_checkpoints: 3
    session_access_mode: cache_until_flush
```

则本策略优先于逐回合 persistence transaction。普通教学回合先在当前 live session 中形成 candidate checkpoints，达到 flush 条件后才统一访问 GitHub 并提交。

默认 `max_checkpoints=3`：最多累计 3 个有效 checkpoint，再统一 flush。前 2 个 checkpoint 只存在于当前聊天的 session-local working state，尚未成为 committed state。

新聊天启动时读取一次 manifest、`state.current`、当前笔记必要区段与当前章节必要区段，建立 session-local working snapshot。成功恢复后，普通 buffered turn 直接基于这个 working snapshot 教学，不得在每个 assistant turn 重新读取 manifest、`state.current`、note 或 Q&A。

除非当前知识问题本身需要查询最新外部官方资料，否则 batching 未触发 flush 的普通教学回合 persistence I/O 应为：

```text
remote_reads=0
remote_writes=0
```

## 2. Candidate checkpoint

每个产生学习进度的教学回合先形成一个 candidate checkpoint，至少包含：

- 本题/练习的判定结果；
- intended Learning State delta；
- note / Q&A / Bug / code-ability 等领域事件；
- 稳定的 evidence id；
- 下一教学位置。

candidate checkpoint 以及 session-local working state 可以跨当前聊天中的多个 teaching turns 继续使用。它们不是第二个持久化 source of truth：一旦聊天重新启动，只能从 GitHub committed state 恢复。

candidate checkpoint 尚未 flush 时：

- 不得声称“已写入 GitHub”“已 checkpoint”或“已持久化”；
- 默认不需要向用户逐题报告 `1/3`、`2/3`，避免增加输出噪声；只有用户询问保存状态时才说明；
- 不创建 prepared WAL；
- 不读取或写入 GitHub persistence assets；
- 新聊天只能从最后 committed checkpoint 恢复，不能依赖未 flush 的聊天上下文。

## 3. Flush 条件

满足任一条件立即 flush：

1. candidate checkpoint 数达到 `max_checkpoints`；
2. `needs_review` / critical misconception；
3. 小节边界或章节边界；
4. mastery-sensitive action 之前；
5. 用户要求 `/checkpoint`、暂停、停止或结束学习；
6. 明确执行 conversation handoff / 用户要求切换到新聊天；
7. completion；
8. 用户明确要求立即保存。

不要仅因为“本轮产生了学习事件”就 flush。不要仅因为 assistant turn 发生变化就刷新 GitHub。

因此默认批量大小为 3 时，正常连续答对最多只有 2 个 checkpoint 处于未落盘状态。

## 4. Session-local working snapshot

启动成功后，在当前聊天中维护：

- last committed state snapshot 及其已知 blob/SHA；
- 当前 working Learning State；
- candidate checkpoint buffer；
- 已加载领域文件的内容与已知 blob/SHA；
- 当前 note/chapter 的必要教学上下文。

普通 buffered turn 只更新 working state 与 candidate buffer。

不得把“每个新 assistant turn”视为新的 backend transaction context。只有真正开始 flush 时才创建 transaction context、冻结 aggregated `targets[]` 并执行 boundary validation。

若 flush 时使用的 GitHub SHA 已过期，mutation 应产生 optimistic concurrency conflict；此时再刷新远端 authoritative state 并按冲突/恢复语义处理，而不是为了预防极少见的并发变化在每轮提前读取 GitHub。

## 5. Flush 执行

flush 时把当前 batch 中全部 candidate checkpoints 合并成一个 persistence batch：

```text
buffered candidate checkpoints
→ 按领域目标聚合/去重
→ 冻结最终 targets[]
→ 一次 transaction boundary validation
→ prepared WAL
→ 领域幂等 upsert
→ final-state+clear
```

同一物理领域文件中的多个 checkpoint 变更应尽量合并为一次文件 mutation，避免对同一个 notes / Q&A 文件逐 checkpoint 重复写入。

flush 前不要求例行重新读取已经在当前 session 中加载且未发生冲突的 state/domain 文件。只有目标文件从未加载、mutation 需要当前内容、mastery 需要此前未加载 evidence，或出现冲突/不明确结果时，才做必要读取。

flush 成功后：

- `checkpoint_version` 按本批次包含的 candidate checkpoint 数递增，而不是只递增 1；
- `return_to`、`next_action`、`last_section` 使用批次中最后一个 candidate checkpoint 的最终位置；
- `pending_writeback=null`；
- 清空 live-session candidate buffer；
- 用成功 mutation 返回的新 commit/blob 信息更新 session-local working snapshot；
- 不执行例行 readback。

## 6. 失败与恢复

一旦开始 flush 并写入 prepared WAL，仍完全遵循 `shared/session-persistence.md`：

- 写入失败不得声称已保存；
- `pending_writeback != null` 时下一轮 recovery-only；
- 不得在旧 WAL 未恢复前创建新 batch transaction；
- unknown outcome、SHA conflict、integrity reconstruction 时才刷新远端状态。

尚未开始 flush 的 candidate checkpoints 没有 WAL 保护，聊天异常终止时可能丢失。这是批处理换取更低延迟的明确权衡；新聊天必须从最后 committed state 恢复。

## 7. 与逐回合事务的关系

当 manifest 明确启用 `checkpoint_batching.enabled=true` 时，本文件与 `SKILL.md` 中的 batching 规则是当前 runtime 的 authoritative persistence cadence；不得退回“每个产生持久化事件的 teaching turn 立即创建 transaction”。

只有 batching 配置缺失、无效或明确禁用时，才使用逐回合事务语义。
