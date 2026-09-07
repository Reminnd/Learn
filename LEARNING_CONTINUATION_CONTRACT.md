# Learn Agent 新聊天续学 Contract

## 1. 目标

在新的云端聊天中，从公开 GitHub 仓库读取当前 Agent Harness 课程快照并继续教学。学习状态以 GitHub `main` 分支中的持久化资产为准，不以旧聊天记录为准。

云端入口：

- Contract：`https://raw.githubusercontent.com/Reminnd/Learn/main/LEARNING_CONTINUATION_CONTRACT.md`
- State：`https://raw.githubusercontent.com/Reminnd/Learn/main/.learn-agent/progress/current.md`
- 仓库：`https://github.com/Reminnd/Learn`

## 2. 后端与同步关系

- 本机 Primary backend：`D:/agent/Learn` 对应的 local workspace。
- 云端读取源：公开仓库 `Reminnd/Learn` 的 `main` 分支。
- GitHub 是经过 checkpoint 的同步快照；云端新聊天先读取它恢复上下文。
- 云端环境若有仓库写权限，可把当前 checkout 配置为 `git_repository` backend 并提交后续证据；只有网页读取能力时，可以继续讲解，但不得声称学习事件已经持久化。
- `storage.yaml` 含机器绝对路径，不上传；使用 `.learn-agent/storage.example.yaml` 在新机器初始化。

本 contract 明确授权新聊天读取上述公开 GitHub 仓库作为续学快照。在有 checkout 的运行环境中，使用该 checkout 的 workspace-local manifest；若用户级 locator 指向其他目录，以本 contract 绑定的仓库 checkout 为目标，不根据修改时间猜测。

## 3. 新聊天启动顺序

1. 打开本 contract 的 GitHub raw URL。
2. 读取仓库根目录的 `AGENTS.md` 与 `SKILL.md`；可用时启用 `learn-agent` skill。
3. 读取 `.learn-agent/progress/current.md`。这是 GitHub 快照中的权威学习位置，不得用聊天摘要代替。
4. 确认 `integrity.status: healthy` 且 `pending_writeback: null`。若不满足，停止推进状态并报告具体缺口。
5. 根据 `note_pointer` 读取 `learning/notes/<note_pointer>` 的 `last_section` 附近；再读取 `chapter_file` 的必要小节和验收契约。
6. 从 `return_to` 与 `next_action` 继续，一次只问一道检验题。
7. 若云端环境有仓库 checkout 与写权限，从 `.learn-agent/storage.example.yaml` 创建 workspace-local `storage.yaml`，填写当前 checkout 的绝对路径，并用 `scripts/persistence.py validate` 验证后再写回。
8. 若只有 GitHub 网页读取能力，完成教学反馈后输出最小待保存增量；不得宣称已写入 checkpoint。

## 4. 当前已验证快照

```yaml
checkpoint_version: 65
checkpoint_at: 2026-09-07T19:51:12+08:00
stage_id: stage-01
chapter_id: 01-llm-message-prompt-langchain
learning_status: learning
integrity_status: healthy
last_section: 1.4 对话历史由应用传入
current_activity: learning
next_question: L1-CHECK-5 / attempt 1
pending_writeback: null
```

当前需要继续的问题：

```python
history = []

_, history = run_turn(model, history, "My name is Lin.")
_, history = run_turn(model, history, "What is my name?")
```

询问学习者：谁保存第一轮对话？第二次调用时必须把哪个变量传给 `run_turn`？不要在学习者回答前公布标准答案。

## 5. 教学约束

- 默认使用简体中文解释；代码、变量名和技术术语使用 English。
- 当前为 Teacher Mode。
- 按“最小原理实现 → LangChain/LangGraph 映射 → 工程问题 → 企业级改造 → 练习 → Q&A”推进。
- 结论、练习、Q&A、误区、Bug 和学习位置变化必须通过 persistence transaction 写回。
- 写回后局部验证 evidence ID、状态、指针以及 `pending_writeback: null`。
- 局部检查通过不等于章节 mastered；mastery 只按章节验收契约和 mastery rubric 判定。
- LangChain、LangGraph 或模型 API 的具体版本与弃用信息必须先查官方文档。

## 6. 当前恢复所需资产

```text
.learn-agent/progress/current.md
learning/notes/index.md
learning/notes/stage-01/01-llm-message-prompt-langchain.md
learning/qa/stage-01.md
learning/bug-book/bug-book.md
```

缺失的 `progress.code_ability`、`project.root` 与 `adr.root` 当前没有运行证据，不得凭空重建。

## 7. 后续 GitHub 同步流程

1. 完成 learn-agent checkpoint，并确认 `pending_writeback: null`。
2. 获取 `origin/main`，确认远端没有未整合提交。
3. 只暂存 contract、manifest template，以及 manifest 解析出的现存学习资产。
4. 使用 Conventional Commits 提交。
5. 推送到 `origin/main`，并验证本地 `HEAD` 与 `origin/main` 相同。

## 8. 可复制到新聊天的最短指令

```text
请读取并遵循：
https://raw.githubusercontent.com/Reminnd/Learn/main/LEARNING_CONTINUATION_CONTRACT.md

再从 GitHub main 分支读取 .learn-agent/progress/current.md 和当前
note_pointer，验证 integrity.status=healthy、pending_writeback=null 后，
从 return_to 指定的问题继续。一次只问一题，不依赖旧聊天记录。
```
