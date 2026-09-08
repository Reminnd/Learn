# Learn Agent 新聊天续学 Contract

## 1. 目标

在新的云端聊天中，从 GitHub 仓库恢复当前 Agent Harness 课程状态并继续教学。学习状态以 GitHub `main` 分支中的持久化资产为准，不以旧聊天记录为准。

云端入口：

- Contract：`https://raw.githubusercontent.com/Reminnd/Learn/main/LEARNING_CONTINUATION_CONTRACT.md`
- State：`https://raw.githubusercontent.com/Reminnd/Learn/main/.learn-agent/progress/current.md`
- Manifest：`https://raw.githubusercontent.com/Reminnd/Learn/main/.learn-agent/storage-manifest.yaml`
- 仓库：`https://github.com/Reminnd/Learn`

## 2. 后端与同步关系

- 跨聊天共享的 Primary backend：GitHub `Reminnd/Learn` 的 `main` 分支，backend 类型为 `git_repository`。
- 云端环境只要具备可靠的 GitHub 持久读写能力（例如已授权 GitHub connector / Contents API），即可直接对 `main` 执行学习 persistence transaction；不要求先建立本地 checkout。
- `.learn-agent/storage-manifest.yaml` 是云端逻辑资产映射、能力声明与 persistence runtime policy；所有写入必须先按 manifest 解析 `state.current`、`notes.root`、`qa.stage` 等逻辑 key。
- 本机 `D:/agent/Learn` 可作为工作副本或同步客户端；在本机继续教学前先同步 GitHub `main`，不要用较旧的本地状态覆盖较新的远端状态。
- 若环境只有 GitHub 读取能力，可以继续讲解，但不得声称学习事件已经持久化。
- `.learn-agent/storage.example.yaml` 仅作为新环境初始化模板，不是云端实时续学的权威 manifest。

同一 persistence batch 仍只有一个 primary backend。禁止同时向多个后端分别提交后再猜测合并结果。

## 3. Checkpoint batching

当前 runtime manifest 启用了：

```yaml
persistence:
  checkpoint_batching:
    enabled: true
    max_checkpoints: 3
```

详细规则见 `shared/checkpoint-batching.md`。

默认连续普通教学 checkpoint 先在当前 live session 中累计，达到 3 个再统一 flush。这样优先保证教学响应速度，而不是每答一题都等待 GitHub 写入。

立即 flush 条件包括：

- candidate checkpoint 数达到 3；
- `needs_review` / critical misconception；
- 小节或章节边界；
- mastery-sensitive action 之前；
- 用户要求 checkpoint、暂停、停止、结束学习；
- conversation handoff / 即将切换新聊天；
- completion；
- 用户明确要求立即保存。

尚未 flush 的 candidate checkpoint 只存在于当前 live session，不能声称已经写入 GitHub。默认最多有 2 个普通 checkpoint 处于这种未落盘状态。新聊天只从最后 committed state 恢复。

flush 时把本批全部 candidate checkpoints 聚合成一个 persistence batch，按 `shared/checkpoint-batching.md` 和 `shared/session-persistence.md` 执行一次 WAL transaction。`checkpoint_version` 按本批 checkpoint 数递增；同一领域文件中的多个增量应尽量合并为一次文件 mutation。

## 4. 新聊天启动顺序

1. 打开本 contract 的 GitHub raw URL。
2. 读取 `.learn-agent/storage-manifest.yaml`；读取仓库根目录存在的 `AGENTS.md`，并读取 `SKILL.md`。若根目录没有 `AGENTS.md`，记录其不存在即可，不视为恢复失败。
3. 通过 manifest 的 `state.current` 映射读取 `.learn-agent/progress/current.md`。这是权威 committed 学习位置，不得用聊天摘要代替。
4. 确认 `integrity.status: healthy`。若 `pending_writeback != null`，当前轮进入 recovery-only，不得创建新教学 batch。
5. 根据 `note_pointer` 读取当前正式笔记的 `last_section` 附近；再读取 `chapter_file` 的必要小节和验收契约。
6. 从 `return_to` 与 `next_action` 继续，一次只问一道检验题。
7. 若当前环境具备 GitHub 持久写能力，读取 manifest 中的 checkpoint batching 配置；普通 teaching turns 先形成 candidate checkpoints，达到 flush 条件时才统一写入。
8. flush 时执行：冻结聚合后的完整 `targets[]` → 一次 boundary validation → prepared WAL → 领域幂等 upsert → final-state+clear。不得绕过 WAL 直接修改最终 Learning State。
9. GitHub mutation 返回明确 commit/blob 成功结果时，正常成功路径直接信任 write acknowledgement，不对刚成功写入的 WAL、领域文件或 final state 做例行回读。只有结果不明确、SHA/并发冲突、recovery、integrity reconstruction、mastery 读取此前未加载证据或用户明确要求审计时才额外读取。
10. 若只有只读能力，允许继续教学，但所有未提交增量都必须明确标记为未持久化。

## 5. 当前已验证快照

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
```

当前需要继续的问题：

初始 `history=[]`，每一轮追加 1 条 `HumanMessage` 与 1 条 `AIMessage`。询问学习者按顺序给出第 1、2、3 轮结束后的 `len(history)`。不要在学习者回答前公布标准答案。

## 6. 教学约束

- 默认使用简体中文解释；代码、变量名和技术术语使用 English。
- 当前为 Teacher Mode。
- 按“最小原理实现 → LangChain/LangGraph 映射 → 工程问题 → 企业级改造 → 练习 → Q&A”推进。
- 结论、练习、Q&A、误区、Bug 和学习位置变化都必须形成 candidate checkpoint；是否立即写 GitHub 由 checkpoint batching flush policy 决定。
- 未 flush 的 candidate checkpoint 不得称为 committed checkpoint。
- 正常成功写入不做重复回读；只在恢复、冲突、不明确结果、完整性重建、mastery 读取旧证据或显式审计时检查。
- `needs_review` 必须立即 flush，避免关键误区只留在聊天上下文。
- 局部检查通过不等于章节 mastered；mastery-sensitive action 前必须先 flush 当前 batch，再按章节验收契约和 mastery rubric 判定。
- LangChain、LangGraph 或模型 API 的具体版本与弃用信息必须先查官方文档。

## 7. 当前恢复所需资产

```text
.learn-agent/storage-manifest.yaml
.learn-agent/progress/current.md
shared/checkpoint-batching.md
learning/notes/index.md
learning/notes/stage-01/01-llm-message-prompt-langchain.md
learning/qa/stage-01.md
learning/bug-book/bug-book.md
```

缺失的运行资产若当前仍无运行证据，不得凭空重建。

## 8. 本机与 GitHub 同步流程

当在本机 `D:/agent/Learn` 继续学习或开发时：

1. 先获取并整合 GitHub `main`，确认本机读取到最新 committed `state.current`。
2. 若远端 `pending_writeback` 非空，先按 recovery-only 语义恢复，不能直接覆盖。
3. 本机产生 candidate checkpoints 时读取同一 batching policy；触发 flush 后再执行 WAL transaction。
4. 暂停、结束或准备切换聊天/环境前必须 flush 当前 batch。
5. 推送前若远端出现新提交，先整合远端；禁止用较旧的本地学习状态强制覆盖较新的 GitHub 状态。

## 9. 可复制到新聊天的最短指令

```text
请读取并遵循：
https://raw.githubusercontent.com/Reminnd/Learn/main/LEARNING_CONTINUATION_CONTRACT.md

从 GitHub main 的 .learn-agent/storage-manifest.yaml 与 state.current 恢复 committed 状态，
确认 integrity.status=healthy，并从 return_to 继续。
若 checkpoint_batching 已启用，普通学习 checkpoint 先累计，达到 manifest 的 batch size 或 flush 条件时再统一写 GitHub；
needs_review、章节/小节边界、mastery 前、暂停/停止和切换聊天前必须立即 flush。
成功 mutation 不做重复回读，只有恢复、冲突或不明确结果时才验证。
一次只问一题，不依赖旧聊天记录。
```
