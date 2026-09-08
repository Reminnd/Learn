# Checkpoint Batching

本文件定义 GitHub 云端教学的 checkpoint 批处理优化。它只改变**何时 flush**，不改变学习事件、领域证据、WAL 恢复和 mastery 的语义。

## 1. 默认策略

运行时 manifest 若声明：

```yaml
persistence:
  checkpoint_batching:
    enabled: true
    max_checkpoints: 3
```

则普通教学回合不再每题立即写 GitHub，而是在当前 live session 中累计 candidate checkpoints。

默认 `max_checkpoints=3`：最多累计 3 个有效 checkpoint，再统一 flush。前 2 个 checkpoint 只存在于当前聊天上下文，尚未成为 committed state。

## 2. Candidate checkpoint

每个产生学习进度的教学回合先形成一个 candidate checkpoint，至少包含：

- 本题/练习的判定结果；
- intended Learning State delta；
- note / Q&A / Bug / code-ability 等领域事件；
- 稳定的 evidence id；
- 下一教学位置。

candidate checkpoint 尚未 flush 时：

- 不得声称“已写入 GitHub”“已 checkpoint”或“已持久化”；
- 可以说明“已加入待提交批次（1/3、2/3）”；
- 新聊天只能从最后 committed checkpoint 恢复，不能依赖未 flush 的聊天上下文。

## 3. Flush 条件

满足任一条件立即 flush：

1. candidate checkpoint 数达到 `max_checkpoints`；
2. `needs_review` / critical misconception；
3. 小节边界或章节边界；
4. mastery-sensitive action 之前；
5. 用户要求 `/checkpoint`、暂停、停止或结束学习；
6. 即将进行 conversation handoff / 新聊天续学；
7. completion；
8. 用户明确要求立即保存。

因此默认批量大小为 3 时，正常连续答对最多只有 2 个 checkpoint 处于未落盘状态。

## 4. Flush 执行

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

flush 成功后：

- `checkpoint_version` 按本批次包含的 candidate checkpoint 数递增，而不是只递增 1；
- `return_to`、`next_action`、`last_section` 使用批次中最后一个 candidate checkpoint 的最终位置；
- `pending_writeback=null`；
- 清空 live-session candidate buffer。

GitHub mutation 返回明确成功时继续遵循现有优化：正常成功路径不对刚写入的内容做例行回读。

## 5. 失败与恢复

一旦开始 flush 并写入 prepared WAL，仍完全遵循 `shared/session-persistence.md`：

- 写入失败不得声称已保存；
- `pending_writeback != null` 时下一轮 recovery-only；
- 不得在旧 WAL 未恢复前创建新 batch transaction。

尚未开始 flush 的 candidate checkpoints 没有 WAL 保护，聊天异常终止时可能丢失。这是批处理换取更低延迟的明确权衡；新聊天必须从最后 committed state 恢复。

## 6. 与默认逐回合事务的关系

`SKILL.md` 中“每个产生持久化事件的教学回合最多一个 transaction”是安全默认值。manifest 明确启用 `checkpoint_batching` 时，本文件作为该 runtime backend 的性能优化层：多个连续 teaching turns 可以先形成 candidate checkpoints，并在 flush 边界合并为一个 transaction。

如果 batching 配置缺失、无效或被禁用，则退回 `SKILL.md` 的逐回合事务语义。
