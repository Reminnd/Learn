# Context / Token Budget Policy（上下文 / Token 预算策略）

目标：不是把可用 Context Window（上下文窗口）塞满，而是只让值得影响当前判断的信息进入 Working Context（工作上下文）。可变资产通过 storage manifest 定位；不要把只读 skill 包中的种子状态当成运行状态。

## 1. Hot / Warm / Cold 分层

### Hot Context — 当前轮直接加载

- storage manifest 的所需 key，以及 `state.current` 中的会话状态、当前位置、`return_to`、完整性摘要与下一步。
- 当前笔记的摘要、易错点、Q&A、复习卡片或 `last_section` 附近。
- 当前章节正在使用的小节；首次进入、练习、Q&A 或判定掌握时再加载验收契约。
- 当前问题直接涉及的代码、错误和约束。

### Warm Context — 先检索，命中后局部加载

- 当前主题相关的 Bug Book、代码能力证据、ADR、框架映射。
- 当前 Stage 的 Q&A Ledger 中经主题检索命中的少量条目。
- `curriculum/index.md` 中与定位或切章有关的部分。
- `shared/model-router.md`：只在进入新章节、档位缺失、用户询问模型，或可能切换 Claude Code + DeepSeek 时读取。
- `shared/session-persistence.md`：只在恢复异常、手动 checkpoint、暂停/完成、写入失败或状态冲突时读取。
- `shared/storage-adapters.md`：只在 manifest 缺失、首次选择/切换后端或配置同步时读取。
- `shared/learning-state-machine.md`：只在 schema 迁移、状态冲突、恢复或掌握判定时读取。
- `shared/mastery-rubric.md` 与 `shared/chapter-contract.md`：只在练习、Q&A、补考、切章或掌握判定时读取。

### Cold Context — 默认不加载

- 历史聊天记录、历史章节全文、全部历史笔记、全部 Q&A Ledger、全部 Bug Book、全部 ADR。
- 尚未学习的课程正文、旧项目资料、与当前问题无关的工具输出。

Cold Context 需要跨章综合、项目整合或明确追溯历史时，才通过检索临时提升为 Warm / Hot。

## 2. 默认软预算

能获得实际 Token 时，预算同时受比例和绝对值约束，取更小者：

- 课程持久化资料的启动加载：目标不超过可用上下文的 `10%` 或约 `8k tokens`。
- 当前轮完整工作集：通常不超过可用上下文的 `20%` 或约 `32k tokens`。
- 超过任一软门槛时，先检索、裁剪和压缩；任务正确性确实需要时可以临时扩大，并说明原因。

无法获得实际 Token 时：

- 明确标注“估算”，使用文件字符数、字节数和内容类型做相对判断。
- 中文、英文与代码的 Token/字符比不同，不把简单字符换算冒充精确 Token。

## 3. 加载纪律

1. 先读 manifest 所需 key 与状态，再定位当前笔记和章节的小节；不要默认读取整份章节或完整 manifest。
2. 跨窗口恢复以 manifest + `state.current` 为 Bootstrap；不读取旧聊天来重建状态。
3. 已写入 `chapter_model_profile` 后，同一章节不重复读取模型路由表。
4. Q&A Ledger 只保留单句结论和正式笔记指针；详细解释只保留在课程笔记。
5. 大于约 4k tokens 的工具结果先提取结论、证据位置和待办，再决定是否保留原文。
6. 对话增长时，把稳定结论增量写回笔记或进度；不要靠重复携带整段历史维持连续性。
7. 同一事实只保留一个权威来源；持久化协议、状态 schema、mastery 规则分别只在对应 shared 文件维护。
8. 大上下文窗口只表示“能装下”，不表示“值得装入”。

## 4. 压力升高时的降级顺序

1. 当前笔记只保留摘要、易错点、Q&A、复习卡片和 `last_section` 附近。
2. 当前章节只保留正在讲解的小节及其直接依赖。
3. Q&A Ledger / Bug Book / Code Ability / ADR 只检索当前主题条目。
4. 长工具结果压缩为结论、关键证据和可复查位置。
5. 历史章节只读复习卡片或总结。
6. 只有跨章综合题或项目整合才临时扩大范围，完成后回落。

## 5. Token 使用报告

用户询问 Skill 的 Token / Context 占用时：

- 分开报告固定入口、当前进度、当前章节片段、当前笔记片段和条件文件。
- 能测实际 Token 就给实际值；否则给字符/字节数与明确的估算范围。
- 同时给出“正常继续课程”和“跨章/项目重场景”两种占用。
- 若 `SKILL.md` 膨胀，优先迁移低频规则到 `shared/`，并确保入口写明读取触发条件。
