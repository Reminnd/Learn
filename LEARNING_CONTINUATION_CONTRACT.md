# Learn Agent 新聊天续学 Contract

## 1. 目标

在新的云端聊天中，从 GitHub 仓库恢复当前 Agent Harness 课程状态并继续教学。学习状态以 GitHub `main` 分支中的 committed 持久化资产为准，不以旧聊天记录为准。

云端入口：

- Contract：`https://raw.githubusercontent.com/Reminnd/Learn/main/LEARNING_CONTINUATION_CONTRACT.md`
- State：`https://raw.githubusercontent.com/Reminnd/Learn/main/.learn-agent/progress/current.md`
- Manifest：`https://raw.githubusercontent.com/Reminnd/Learn/main/.learn-agent/storage-manifest.yaml`
- 仓库：`https://github.com/Reminnd/Learn`

## 2. 后端与同步关系

- 跨聊天共享的 Primary backend：GitHub `Reminnd/Learn` 的 `main` 分支，backend 类型为 `git_repository`。
- 云端环境只要具备可靠的 GitHub 持久读写能力，即可直接对 `main` 执行学习 persistence transaction；不要求先建立本地 checkout。
- `.learn-agent/storage-manifest.yaml` 是云端逻辑资产映射、能力声明与 persistence runtime policy 的权威来源。
- manifest 启用 `checkpoint_batching` 时，batching cadence 优先于逐回合 transaction；不得因为 `SKILL.md` 中的通用安全语义而退回每题立即写 GitHub。
- 本机 `D:/agent/Learn` 可作为工作副本或同步客户端；在本机继续教学前先同步 GitHub `main`，不要用较旧的本地状态覆盖较新的远端状态。
- 若环境只有 GitHub 读取能力，可以继续讲解，但不得声称 candidate checkpoint 已经 committed。

同一 persistence batch 只有一个 primary backend。

## 3. Checkpoint Batching 与 Session Cache

当前 runtime manifest 启用了：

```yaml
persistence:
  checkpoint_batching:
    enabled: true
    max_checkpoints: 3
    session_access_mode: cache_until_flush
    normal_buffered_turn_remote_reads: 0
    normal_buffered_turn_remote_writes: 0
    refresh_before_each_turn: false
```

详细规则见 `SKILL.md`、`shared/checkpoint-batching.md` 与 `shared/session-persistence.md`。

新聊天完成一次启动恢复后，建立 session-local working snapshot。后续普通 teaching turns：

```text
用户回答
→ 本地判定
→ 更新 session-local working state
→ 加入 candidate checkpoint buffer
→ 立即继续下一题
```

**此时不得为了 persistence 再调用 GitHub。**

普通 buffered turn 的目标 I/O：

```text
GitHub persistence reads  = 0
GitHub persistence writes = 0
```

不要在每题后重新读取：

- `.learn-agent/storage-manifest.yaml`
- `.learn-agent/progress/current.md`
- 当前 notes
- 当前 Q&A ledger
- 刚写过的文件

也不要逐题向用户输出“正在写入 GitHub”“正在验证状态”“1/3、2/3”等持久化过程信息；除非用户明确询问保存状态。

只有达到 flush / refresh 条件时才访问 GitHub persistence backend。

## 4. Flush / Refresh 条件

立即 flush 条件：

- candidate checkpoint 数达到 `max_checkpoints=3`；
- `needs_review` / critical misconception；
- 小节或章节边界；
- mastery-sensitive action 之前；
- 用户要求 checkpoint、暂停、停止、结束学习；
- 用户明确要求 conversation handoff / 切换新聊天；
- completion；
- 用户明确要求立即保存。

不要仅因为“本轮有学习事件”就 flush。

只有以下情况需要刷新/额外读取远端：

- SHA / optimistic concurrency conflict；
- mutation 结果不明确；
- `pending_writeback != null` 的 recovery；
- integrity reconstruction；
- mastery 需要此前未加载的 committed evidence；
- flush 目标文件此前从未加载且 mutation 需要当前内容；
- 用户明确要求审计。

## 5. 新聊天启动顺序

新聊天启动只做一次恢复读：

1. 打开本 Contract。
2. 读取 `.learn-agent/storage-manifest.yaml`。
3. 读取 `SKILL.md`；根目录存在 `AGENTS.md` 才读取，不存在不视为失败。
4. 通过 manifest 读取一次 `state.current`，建立 committed baseline。
5. 确认 `integrity.status=healthy`；若 `pending_writeback != null`，进入 recovery-only。
6. 根据 `note_pointer` 读取当前正式笔记的必要区段。
7. 读取 `chapter_file` 当前小节与验收契约的必要区段。
8. 若 batching 开启，读取 `shared/checkpoint-batching.md`，建立 session-local working snapshot 与空 candidate buffer。
9. 从 `return_to` / `next_action` 继续，一次只问一题。

**完成第 9 步后，不得在普通 buffered teaching turn 再执行启动流程，也不得重新读取 committed state。**

只有 flush / refresh / recovery / mastery 边界才重新进入 persistence 操作。

如果当前问题涉及 LangChain、LangGraph 或模型 API 的最新版本、弃用或当前能力，可以查询官方文档；这种 external knowledge lookup 与 GitHub persistence refresh 无关，不应触发 state 读写。

## 6. Flush 执行

达到 flush 条件后，把当前 batch 中全部 candidate checkpoints 聚合成一个 persistence batch：

```text
buffered checkpoints
→ 合并 working-state deltas
→ 按物理领域文件聚合/去重变更
→ 冻结 targets[]
→ 一次 boundary validation
→ prepared WAL
→ 领域幂等 upsert
→ final-state+clear
```

要求：

- 同一个 notes 文件中 3 个 checkpoint 的变化尽量一次 mutation 写入；
- 同一个 Q&A 文件中 3 个 checkpoint 的变化尽量一次 mutation 写入；
- `checkpoint_version` 按本批 checkpoint 数递增；
- final state 使用本批最后一个 candidate 的 `return_to` / `next_action` / `last_section`；
- GitHub mutation 返回明确成功时直接信任 write acknowledgement，不做例行 readback；
- flush 成功后用已知 replacement content 与 mutation 返回的新 SHA 更新 session-local snapshot，清空 candidate buffer，然后立即继续教学。

## 7. 当前 committed 快照

```yaml
checkpoint_version: 75
checkpoint_at: 2026-09-08T14:00:53+08:00
stage_id: stage-01
chapter_id: 01-llm-message-prompt-langchain
learning_status: learning
integrity_status: healthy
last_section: 1.8 Message 历史增长
current_activity: learning
next_question: L1-CHECK-13 / attempt 2
pending_writeback: null
storage_backend: git_repository
checkpoint_batching: 3
session_access_mode: cache_until_flush
```

当前需要继续的问题：

初始 `history=[]`，每一轮追加 1 条 `HumanMessage` 与 1 条 `AIMessage`。询问学习者按顺序给出第 1、2、3 轮结束后的 `len(history)`。不要在学习者回答前公布标准答案。

## 8. 教学约束

- 默认使用简体中文解释；代码、变量名和技术术语使用 English。
- 当前为 Teacher Mode。
- 按“最小原理实现 → LangChain/LangGraph 映射 → 工程问题 → 企业级改造 → 练习 → Q&A”推进。
- 结论、练习、Q&A、误区、Bug 和学习位置变化形成 candidate checkpoint；是否访问 GitHub 由 batching flush policy 决定。
- 未 flush 的 candidate checkpoint 不得称为 committed checkpoint。
- `needs_review` 必须立即 flush。
- 局部检查通过不等于章节 mastered；mastery-sensitive action 前先 flush 当前 buffer，再按章节验收契约与 mastery rubric 判定。
- 正常成功写入不做重复回读。
- 一次只问一题。
- 不要向用户暴露冗余 persistence 执行日志；只有失败、恢复、冲突或用户主动询问时才说明。

## 9. 本机与 GitHub 同步流程

当在本机 `D:/agent/Learn` 继续学习或开发时：

1. 新 session 启动时先获取并整合 GitHub `main`。
2. 建立 working snapshot 后，普通 buffered turns 不重复 pull/fetch state。
3. 若远端 `pending_writeback` 非空，先 recovery-only。
4. candidate checkpoints 触发 flush 后再执行 WAL transaction。
5. 暂停、结束或明确准备切换聊天/环境前必须 flush 当前 batch。
6. flush 出现远端 SHA conflict 时再整合远端，禁止为预防冲突每题刷新。

## 10. 可复制到新聊天的最短指令

```text
请读取并遵循：
https://raw.githubusercontent.com/Reminnd/Learn/main/LEARNING_CONTINUATION_CONTRACT.md

启动时从 GitHub main 读取 manifest、state.current、当前笔记和当前章节必要区段，建立 session-local working snapshot。
若 checkpoint_batching 已启用：普通 teaching turn 不读、不写 GitHub persistence；只在当前聊天累计 candidate checkpoints。
达到 batch size=3、needs_review、小节/章节边界、mastery 前、暂停/停止或明确 handoff 时才统一 flush。
普通 buffered turn 不重复读取 manifest/state/notes/Q&A，也不输出 persistence 过程日志。
成功 mutation 不做重复回读；冲突、recovery 或 unknown outcome 时才刷新远端。
从 return_to 继续，一次只问一题。
```
