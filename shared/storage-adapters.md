# Learning Persistence Adapters

本文件只在 storage manifest 缺失、首次选择后端、切换后端或配置同步目标时读取。普通教学只读取 manifest 的最小映射和 `state.current`。

## 1. 逻辑资产契约

Skill 只依赖以下逻辑资产，不依赖固定物理目录：

```yaml
state.current: 短学习状态 + 最新 checkpoint
notes.root: 正式课程笔记
notes.index: 笔记索引
qa.stage: 当前 Stage 的稀疏 Q&A Ledger
bugs.book: Bug Book
progress.code_ability: 代码能力证据
project.root: Project Track 与里程碑
adr.root: 架构决策记录
```

同一学习会话只能有一个 primary backend。Git、云盘或另一个工作区默认是显式 `sync_targets`，不要多后端同时写入后再猜测如何合并。

## 2. Manifest 最小结构

```yaml
version: 2
backend: local_workspace | obsidian_vault | chatgpt_workspace | git_repository | cloud_drive
backend_root: <真实根目录或环境逻辑根>
capabilities:
  persistent_read: true
  persistent_write: true
  local_path_exposed: true | false
  user_browsable: true | false
  versioned: true | false
paths:
  state.current: .learn-agent/progress/current.md
  notes.root: learning/notes
  notes.index: learning/notes/index.md
  qa.stage: learning/qa/stage-XX.md
  bugs.book: learning/bug-book/bug-book.md
  progress.code_ability: learning/progress/code-ability.md
  project.root: learning/project
  adr.root: learning/adr
sync_targets: []
```

路径含义由 backend 决定：`local_path_exposed=false` 时只是环境内部逻辑路径，不得表述为用户电脑上的真实目录。

manifest 是物理路径的唯一事实源。正文、章节、状态文件与笔记不得把上面的示例值当成 fallback。运行时必须用逻辑 key 解析；缺 key、规范化后越出 `backend_root`、能力不满足或目标不可访问时立即停止对应操作。

对于本地文件系统 backend，标准 manifest 位置是 `<backend_root>/.learn-agent/storage-manifest.yaml`。`Learn` Skill checkout 本身不得作为 `backend_root`；即使用户选择 `git_repository`，也必须使用与 Skill distribution 分离的 repository/workspace。

## 3. 后端选择

按以下顺序选择：

1. 当前环境可访问的既有 manifest。
2. 真实可写 local workspace；若根目录含 `.obsidian/`，使用 `obsidian_vault` profile，使 `learning/` 可由 Obsidian / VS Code 直接查看。
3. ChatGPT 或其他环境提供的持久化 workspace/file store，使用 `chatgpt_workspace`；逻辑路径保持一致，但不承诺本地可见。
4. Git repository 或 cloud drive 只有在当前环境具备可靠读写能力且用户选择后才作为 primary；否则只登记为 sync target。
5. 没有任何持久写能力时不伪造成功，返回最小待保存增量。

Codex、Claude Code 与 ChatGPT 若能访问同一个 backend，就共享同一学习状态；若不能，必须显式导出/同步，不能仅凭相同路径名假设数据已共享。

## 4. 本地、Obsidian 与 Seed Profile

控制面与可视资产分离：

- `.learn-agent/`：manifest、短状态、恢复指针；适合机器读取。
- `learning/`：笔记、Q&A、Bug Book、能力进度、项目与 ADR；适合 Obsidian / VS Code 阅读。
- `workspace/`：练习代码、事务 JSON 与其他可丢弃/可重建的工作区产物；不属于 Skill distribution。

Skill distribution 中的只读初始化资源统一位于 `seed/`：

```text
seed/state/      -> .learn-agent/progress/
seed/notes/      -> learning/notes/、learning/qa/、learning/bug-book/
seed/progress/   -> learning/progress/
seed/project/    -> learning/project/、learning/adr/
```

初始化时只复制缺失的种子资产，不覆盖已有文件。不要把课程正文或全部 shared 规则复制进 runtime。

本地 fresh runtime 使用：

```text
python scripts/setup_runtime.py --runtime-root <Skill 仓库之外的目录>
```

从 S01 之前的仓库布局迁移既有状态时使用：

```text
python scripts/setup_runtime.py --runtime-root <Skill 仓库之外的目录> --migrate-legacy
```

迁移只做当前已确认的数据搬迁：旧 `.learn-agent/` 保留为 control state，旧 `learning/` 迁到 runtime `learning/`，旧 `work/` 迁到 runtime `workspace/`，随后只补齐缺失 seed。若工作树已经不再包含旧 tracked runtime，脚本从已知 legacy ref 读取这些文件，因此不会要求把 active personal state 重新提交回 Skill distribution。

S01 前的 legacy 状态包含一次未完成的 Stage 01 Chapter 06 curriculum migration：它把后继路由指向从未创建的 `curriculum/stage-01/06-production-hardening.md`。迁移脚本只回滚这一个已确认的孤儿路由到 `curriculum/stage-02/01-state.md`，并把对应 runtime transaction 标为 `rolled_back`；不新增或重写课程。

## 5. 切换与同步

切换 primary backend 前：

1. 在旧后端执行 checkpoint。
2. 导出 manifest 与逻辑资产；能计算时记录文件数和哈希。
3. 写入新后端并验证 `state.current`、当前 note、Q&A 与 Bug Book 指针。
4. 更新新 manifest 后才继续课程；旧后端降级为只读 sync target 或归档。

未经用户明确要求，不自动上传本地笔记、配置云盘、提交 Git、覆盖 Obsidian Vault 或合并冲突。

## 6. Context 约束

- 正常恢复只加载 manifest 的 `version`、`backend`、`capabilities`、所需 `paths` key 和 `state.current`。
- 不把后端安装说明、云盘目录树、Git 历史或所有同步状态常驻上下文。
- 只有后端不可用、路径失效、用户切换工具或要求同步时，才读取本文件相关小节。
