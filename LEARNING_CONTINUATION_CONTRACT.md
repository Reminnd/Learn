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
- `.learn-agent/storage-manifest.yaml` 是云端逻辑资产映射与能力声明；所有写入必须先按 manifest 解析 `state.current`、`notes.root`、`qa.stage` 等逻辑 key。
- 本机 `D:/agent/Learn` 可作为工作副本或同步客户端；在本机继续教学前先同步 GitHub `main`，不要用较旧的本地状态覆盖较新的远端状态。
- 若环境只有 GitHub 读取能力，可以继续讲解，但不得声称学习事件已经持久化；输出最小待保存增量。
- `.learn-agent/storage.example.yaml` 保留为新环境初始化模板，不再作为云端实时续学的权威 manifest。

同一教学事务仍只有一个 primary backend。禁止同时向多个后端分别提交后再猜测合并结果。

## 3. 新聊天启动顺序

1. 打开本 contract 的 GitHub raw URL。
2. 读取 `.learn-agent/storage-manifest.yaml`；读取仓库根目录存在的 `AGENTS.md`，并读取 `SKILL.md`。若根目录没有 `AGENTS.md`，记录其不存在即可，不视为恢复失败。
3. 通过 manifest 的 `state.current` 映射读取 `.learn-agent/progress/current.md`。这是权威学习位置，不得用聊天摘要代替。
4. 确认 `integrity.status: healthy` 且 `pending_writeback: null`。若 WAL 非空，当前轮进入 recovery-only，不得创建新教学事务。
5. 根据 `note_pointer` 读取当前正式笔记的 `last_section` 附近；再读取 `chapter_file` 的必要小节和验收契约。
6. 从 `return_to` 与 `next_action` 继续，一次只问一道检验题。
7. 若当前环境具备 GitHub 持久写能力，每个产生学习事件的教学轮次直接按 `SKILL.md` 与 `shared/session-persistence.md` 对 `main` 执行：冻结完整 `targets[]` → 一次 boundary validation → prepared WAL 写入 `state.current` → 领域幂等 upsert → final-state+clear。不得绕过 WAL 直接修改最终状态。
8. GitHub Contents API 的成功 mutation 会返回明确 commit/blob 结果；正常成功路径直接把该 write acknowledgement 视为持久化成功，不再对刚成功写入的 WAL、领域文件或 final state 做例行回读。只有写入结果不明确、发生 SHA/并发冲突、进入 recovery、需要 integrity reconstruction、mastery 需要读取此前未加载证据，或用户明确要求审计时才额外读取。
9. GitHub Contents API 的每次文件 mutation 可以形成独立 Git commit；事务恢复能力由 `pending_writeback` 的 prepared/recovery 协议保证。只有 final-state+clear mutation 获得明确成功确认后才可声称已保存。
10. 若只有只读能力，完成教学反馈后输出最小待保存增量，不推进 GitHub `state.current`。

## 4. 当前已验证快照

```yaml
checkpoint_version: 67
checkpoint_at: 2026-09-07T21:36:40+09:00
stage_id: stage-01
chapter_id: 01-llm-message-prompt-langchain
learning_status: learning
integrity_status: healthy
last_section: 1.4 对话历史由应用传入
current_activity: learning
next_question: L1-CHECK-7 / attempt 1
pending_writeback: null
storage_backend: git_repository
```

当前需要继续的问题：

```python
def run_turn(model, history, user_input):
    request_messages = [
        *history,
        Message(role="user", content=user_input),
    ]

    assistant_message = model(request_messages)

    new_history = [
        *request_messages,
        assistant_message,
    ]

    return assistant_message, new_history
```

询问学习者：`request_messages`、`assistant_message`、`new_history` 分别是什么，以及它们如何串成一轮对话数据流。不要在学习者回答前公布标准答案。

## 5. 教学约束

- 默认使用简体中文解释；代码、变量名和技术术语使用 English。
- 当前为 Teacher Mode。
- 按“最小原理实现 → LangChain/LangGraph 映射 → 工程问题 → 企业级改造 → 练习 → Q&A”推进。
- 结论、练习、Q&A、误区、Bug 和学习位置变化必须通过 persistence transaction 写回。
- 正常成功写入不做重复回读；只在恢复、冲突、不明确结果、完整性重建、mastery 读取旧证据或显式审计时检查。
- 局部检查通过不等于章节 mastered；mastery 只按章节验收契约和 mastery rubric 判定。
- LangChain、LangGraph 或模型 API 的具体版本与弃用信息必须先查官方文档。

## 6. 当前恢复所需资产

```text
.learn-agent/storage-manifest.yaml
.learn-agent/progress/current.md
learning/notes/index.md
learning/notes/stage-01/01-llm-message-prompt-langchain.md
learning/qa/stage-01.md
learning/bug-book/bug-book.md
```

缺失的 `progress.code_ability`、`project.root` 与 `adr.root` 若当前仍无运行证据，不得凭空重建。

## 7. 本机与 GitHub 同步流程

当在本机 `D:/agent/Learn` 继续学习或开发时：

1. 先获取并整合 GitHub `main`，确认本机读取到最新 `state.current`。
2. 若远端 `pending_writeback` 非空，先按 recovery-only 语义恢复，不能直接覆盖。
3. 本机产生新的学习事务时仍遵守同一 WAL 协议。
4. 完成 checkpoint 并确认 `pending_writeback: null` 后，再提交并推送到 `main`。
5. 推送前若远端出现新提交，先整合远端；禁止用较旧的本地学习状态强制覆盖较新的 GitHub 状态。

## 8. 可复制到新聊天的最短指令

```text
请读取并遵循：
https://raw.githubusercontent.com/Reminnd/Learn/main/LEARNING_CONTINUATION_CONTRACT.md

从 GitHub main 的 .learn-agent/storage-manifest.yaml 与 state.current 恢复状态，
确认 integrity.status=healthy、pending_writeback=null 后，从 return_to 继续。
若当前环境有 GitHub 写权限，每个学习事件按仓库 WAL persistence 协议实时写回 main；
成功 mutation 不做重复回读，只有恢复、冲突或不明确结果时才验证。
一次只问一题，不依赖旧聊天记录。
```