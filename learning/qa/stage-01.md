<!-- learn-agent:evidence:stage-01-ch05-qa-reconstruction:start -->
# Stage 01 Q&A Ledger

## Chapter 05

- Q1: needs_reconstruction — 原通过记录的领域证据缺失，需重新回答。
- Q2: pending。
<!-- learn-agent:evidence:stage-01-ch05-qa-reconstruction:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-1-attempt-1-ledger:start -->
- L1-CHECK-1 / attempt 1: needs_review — Message 职责正确；Prompt 边界偏窄；Chat Model 输入输出方向写反。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-1-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-1-attempt-2-ledger:start -->
- L1-CHECK-1 / attempt 2: passed — 正确给出 Prompt builder 与 Chat Model 的数据流方向；补充精确类型为 `list[Message]`。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-1-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-2-attempt-1-ledger:start -->
- L1-CHECK-2 / attempt 1: needs_review — Message 改写思路正确；缺少两类丢失语义的解释；第一项有重复引号和全角括号。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-2-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-2-attempt-2-ledger:start -->
- L1-CHECK-2 / attempt 2: passed — 正确指出 role 与 metadata 丢失，并提交语法合法的结构化 Message 列表。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-2-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-3-attempt-1-ledger:start -->
- L1-CHECK-3 / attempt 1: passed — 正确区分定义、调用与 list[Message] 返回类型。笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-3-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-4-attempt-1-ledger:start -->
- L1-CHECK-4 / attempt 1: passed — 正确预测两次运行时变量替换后的 user message 内容。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-4-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-5-attempt-1-ledger:start -->
- L1-CHECK-5 / attempt 1: passed — 正确指出应用侧 `history` 保存第一轮对话，第二轮必须继续传入更新后的 `history`；模型本身不会跨独立调用自动保存该历史。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-5-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-6-attempt-1-ledger:start -->
- L1-CHECK-6 / attempt 1: passed — 正确判断第二轮传入空 `history` 会切断此前对话，模型本次输入中不再包含第一轮名字信息。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-6-attempt-1-ledger:end -->
