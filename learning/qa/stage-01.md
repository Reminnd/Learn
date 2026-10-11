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

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-7-attempt-1-ledger:start -->
- L1-CHECK-7 / attempt 1: passed — 正确说明 `request_messages`、`assistant_message`、`new_history` 的职责，并给出 `history + user_input → request_messages → model → assistant_message → new_history` 的完整数据流。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-7-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-8-attempt-1-ledger:start -->
- L1-CHECK-8 / attempt 1: passed — 正确将手写 `Message(role="user")` / `Message(role="assistant")` 映射为 LangChain `HumanMessage` / `AIMessage`。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-8-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-9-attempt-1-ledger:start -->
- L1-CHECK-9 / attempt 1: needs_review — 已识别 `SystemMessage` 类型，但构造未写完整，且未说明 `SystemMessage` 与 `HumanMessage` 的职责区别。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-9-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-9-attempt-2-ledger:start -->
- L1-CHECK-9 / attempt 2: passed — 正确写出 `SystemMessage(content="Answer briefly.")`，并区分 `SystemMessage` 的系统级行为/上下文指令职责与 `HumanMessage` 的用户输入职责。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-9-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-10-attempt-1-ledger:start -->
- L1-CHECK-10 / attempt 1: passed — 正确预测 `ChatPromptTemplate.invoke(...)` 后得到 `SystemMessage(content="Answer in Chinese.")` 与 `HumanMessage(content="Explain Agent.")`；额外空格不影响结论。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-10-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-11-attempt-1-ledger:start -->
- L1-CHECK-11 / attempt 1: passed — 正确区分 `prompt.invoke(...)` 只构造可供模型使用的 Prompt/Messages，而 `(prompt | model).invoke(...)` 会继续调用 model 并返回模型生成的消息。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-11-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-12-attempt-1-ledger:start -->
- L1-CHECK-12 / attempt 1: passed — 正确判断复用同一个 Runnable `chain` 不会自动提供跨调用记忆；若未显式传入 `history`/state 或接入状态管理机制，两次 invoke 在对话状态上仍独立。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-12-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-13-attempt-1-ledger:start -->
- L1-CHECK-13 / attempt 1: needs_review — 回答 `6` 只覆盖第 3 轮结束后的 history 长度，未按要求给出第 1、2、3 轮三个长度。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-13-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-13-attempt-2-ledger:start -->
- L1-CHECK-13 / attempt 2: passed — 正确给出第 1、2、3 轮结束后的 history 长度为 `2, 4, 6`，并掌握每轮新增两条 Message 时的线性增长规律。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-13-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-14-attempt-1-ledger:start -->
- L1-CHECK-14 / attempt 1: passed — 正确说明完整 history 持续增长会提高输入 token、成本和延迟，并持续占用 context window；补充纠正为 prompt cache 命中率不会仅因 history 变长就必然下降。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-14-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-15-attempt-1-ledger:start -->
- L1-CHECK-15 / attempt 1: passed — 正确选择 `Summary + recent history` 以提高早期重要偏好的长期保留概率，并指出当旧信息与当前任务关联性弱时，持续携带 summary 会造成额外输入与处理开销；补充 Trade-off 为摘要还存在生成/维护成本与细节失真风险。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-L1-CHECK-15-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q1-attempt-1-ledger:start -->
- Canonical Q1 / attempt 1: needs_review — 已给出有效边界/失败条件（schema 未校验、Tool 参数不符合要求、model 输出可能错误），但“理解数据流为何能帮助开发和排障”的核心因果关系表达不足；需补充分层输入/输出职责使故障可定位。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-Q1-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q1-attempt-2-ledger:start -->
- Canonical Q1 / attempt 2: passed — 能沿 Prompt、Messages、Model、Tool/Application 的数据传递路径用断点式检查定位第一个异常位置；结合 attempt 1 已给出的失败条件，正式 Q1 两项 acceptance 均满足。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-Q1-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-1-ledger:start -->
- Canonical Q2 / attempt 1: needs_review — 已正确映射原理侧 `model` ↔ LangChain `chat_model`，并正确说明两边输入 Message 序列、输出 assistant message / `AIMessage`；但关键数据流错误地把 `AIMessage` 当成运行时变量并再次传回 model。需仅复检正确数据流方向。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-2-ledger:start -->
- Canonical Q2 / attempt 2: needs_review — 已把两条数据流终点写到 `assistant_message` / `AIMessage`，但仍把具体 Message 类型误当成连续处理层；需按“输入变量 → Prompt 构造 → Messages → 模型 → 输出消息”的抽象层级再复检。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-3-ledger:start -->
- Canonical Q2 / attempt 3: needs_review — 原理侧已基本正确；LangChain 侧仍把 `chain.invoke(...)` 描述成接收已构造的 messages。若使用 `chain = prompt | model`，`chain.invoke(...)` 接收的是原始运行时变量，Prompt→Messages→Model 由链内部完成。下一次只复检 LangChain 数据流。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-3-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-4-ledger:start -->
- Canonical Q2 / attempt 4: passed — 正确写出 LangChain 数据流 `user input / variables → ChatPromptTemplate → Messages → chat_model.invoke(messages) → AIMessage`。结合前序 attempts 已正确保留的对象、输入、输出与原理侧映射，正式 Q2 acceptance 全部满足；Q1/Q2 两个 critical question 均已通过。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-Q2-attempt-4-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch01-Q3-attempt-1-ledger:start -->
- Canonical Q3 / attempt 1: passed — 给出可执行排查顺序：先检查 history 增量机制、summary 与重复写入，再检查本轮 Messages/history 累积是否异常，确认增长正常后再选择上下文控制策略；并指出 `summary + recent history` 的 Trade-off 是长对话旧内容摘要后可能失真。用户同时请求继续学习 sliding window。正式笔记：stage-01/01-llm-message-prompt-langchain.md。
<!-- learn-agent:evidence:stage-01-ch01-Q3-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-1-attempt-1-ledger:start -->
- L2-CHECK-1 / attempt 1: needs_review — 已识别 `"199"` 是 `str`，但误认为没有异常处理时不会因类型错误中断；已说明 `TypeError` 的传播、未捕获异常导致执行失败，以及 `str * int` 的字符串重复行为。正式笔记：stage-01/02-structured-output.md；待同概念复检。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-1-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-1-attempt-2-ledger:start -->
- L2-CHECK-1 / attempt 2: passed — 正确预测 `str + int` 抛出 `TypeError`，无捕获时后续语句不执行；2.1 小节理解复检通过，下一步进入 2.2 Pydantic Schema 与类型校验。笔记：stage-01/02-structured-output.md。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-1-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-1-ledger:start -->
- L2-CHECK-3 / attempt 1: needs_review — 已认识到 Field(gt=0) 拒绝 -20 并抛出 ValidationError；漏掉程序继续执行的输出，把继续运行错误地归因于抛出异常，需复检 try/except 执行流程。正式笔记：stage-01/02-structured-output.md。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-2-attempt-1-ledger:start -->
- L2-CHECK-2 / attempt 1: passed — 区分 Pydantic 默认类型转换和 strict 模式拒绝字符串到整数转换。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-2-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-2-ledger:start -->
- L2-CHECK-3 / attempt 2: needs_review — ACD 预测正确；raise/except 控制流理解待复检，已解释为什么跳过 B。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-3-ledger:start -->
- L2-CHECK-3 / attempt 3: needs_review — 能判断 raise 导致 B 跳过、except TypeError 不匹配，误认为异常未捕获仍执行 D；正确结果只有 A 和 ValueError traceback。待同概念复检。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-3-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-4-ledger:start -->
- L2-CHECK-3 / attempt 4: passed — 正确回答 A、E、D，理由是 ValueError 被匹配 except 捕获，随后继续执行 D。进入 Pydantic e.errors() 结构化校验错误。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-4-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-4-attempt-1-ledger:start -->
- L2-CHECK-4 / attempt 1: needs_review — 识别 price gt=0 的 greater_than 错误，但遗漏 currency 无默认值时 required 的 missing 错误。已讲解 Pydantic v2 required vs default vs nullable，待复检。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-4-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-4-attempt-2-ledger:start -->
- L2-CHECK-4 / attempt 2: passed — 正确回答 ProductA 的 currency 必填、ProductB 因 currency="CNY" 默认值可省略；已完成针对性复检。下一步 FastAPI 请求体校验。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-4-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-5-attempt-1-ledger:start -->
- L2-CHECK-5 / attempt 1: passed — 已正确判断 FastAPI 请求体不符合 Field(gt=0) 时不会进入 create_product 函数体，默认返回 HTTP 422。进入 LangChain Structured Output 的原理与框架映射。笔记：stage-01/02-structured-output.md。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-5-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-6-attempt-1-ledger:start -->
- L2-CHECK-6 / attempt 1: needs_review。回答将ProductIn与AIMessage合为单一对象；已澄清默认返回ProductIn实例、include_raw=True返回raw和parsed。待L2-CHECK-6 attempt 2复检。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-6-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-6-attempt-2-ledger:start -->
- L2-CHECK-6 / attempt 2: passed — 正确判断product是ProductIn实例，.price可读、无content字段时.content报AttributeError；进入Structured Output解析错误处理。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-6-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-1-ledger:start -->
- L2-CHECK-7 / attempt 1: needs_review — 已识别 Pydantic 拒绝 price="abc"，但误认为没有 parsed 键，建议检查 raw 的 price。已纠正 parsed=None、parsing_error 保留错误且 raw 未校验；需复检从 parsed 读取业务值的条件。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-2-ledger:start -->
- L2-CHECK-7 / attempt 2: partial — 选择parsed不为None的方案B正确，但未充分说明raw非空与校验成功的区别，继续追问数据校验与业务后果。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-3-ledger:start -->
- L2-CHECK-7 / attempt 3: needs_review — 已认识到"abc"类型不适合价格计算，仍误认为绕过校验必然抛异常；已指出未经校验数据可能静默进入业务并污染价格字段。下一步复检静默错误案例。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-3-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-4-ledger:start -->
- L2-CHECK-7 / attempt 4: needs_review（部分正确）— 正确预测 append 保存 "abc" 不抛异常，解释仍把不报错与无法数学运算混在一起；已纠正 append 不进行校验或运算，接下来复检实际执行步骤。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-4-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-6-teaching-gap-ledger:start -->
- L2-CHECK-7 / attempt 6: not_assessed — 用户表示没有专门学过 model_validate；已补教用法，不作答错评价，后续练习。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-6-teaching-gap-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempts-7-8-ledger:start -->
- L2-CHECK-7 / attempt 7: partial — 对price="abc"正确解释ValidationError及except打印校验失败，但未回答列表是否新增；继续补充正常分支。
- L2-CHECK-7 / attempt 8: passed — 对price=199正确预测保存成功并给出包含price=199、默认currency=CNY的ProductIn数据，结合前序append不校验的结论，已证明先校验再保存的控制流。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempts-7-8-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-8-ledger:start -->
- L2-CHECK-8 attempt 1: needs_review — 两次尝试与两条输出判断正确，误认为有两个列表元素。
- L2-CHECK-8 attempt 2: passed — 正确判断三个候选响应在第二项通过后break，实际append仅一次，最终一个ProductIn对象。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-8-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-9-attempt-2-ledger:start -->
- L2-CHECK-9 / attempt 2: passed — HTTP 503可能由暂时服务器问题造成，有限重试可能恢复；相同price=-20在gt>0约束不变时校验持续失败，应直接返回错误。开始Backoff。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-9-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-10-attempt-1-ledger:start -->
- L2-CHECK-10 / attempt 1: passed — 最多3次模型调用，第1次失败等待1秒，第2次失败等待2秒，累计等待3秒，第3次失败后停止；明确补充等待次数是2次。下一节幂等性。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-10-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-idempotency-checks11-12-qa:start -->
- L2-CHECK-11 / attempt 1: passed — 已识别订单实际成功但响应超时会触发重复调用，最大重试次数不等于无重复副作用。
- L2-CHECK-12 / attempt 1: passed — req_001重复请求复用订单；req_002新请求创建另一笔；最终总计两笔。继续并发安全教学。
<!-- learn-agent:evidence:stage01-ch02-idempotency-checks11-12-qa:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-1-ledger:start -->
- L2-CHECK-13 / attempt 1: needs_review — 答案注意到两个并发操作可能没有固定全局先后，但将其称为消息列表，未给出两个请求都在写入前完成check的交错顺序；已解释A检查→B检查→A创建→B创建的check-then-act竞态，待复检。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-1-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-2-ledger:start -->
- L2-CHECK-13 / attempt 2: needs_review — 正确指出A先前检查到req_001不存在，但误以为检查和创建写在同一个函数便具有原子性。已说明并发交错执行仍可能产生重复副作用；需要进一步复检。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-2-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-3-guided-explanation-ledger:start -->
- L2-CHECK-13 / attempt 3: needs_review。用户表示不清楚同一函数为何不能保证原子性；已补教并发请求可交错执行，接下来检查if不会自动重新执行。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-3-guided-explanation-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-4-ledger:start -->
- L2-CHECK-13 / attempt 4: passed（更正）— 用户实际回答“直接继续执行”，正确判断if分支不会自动重新检查。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-4-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-14-attempt1-mysql-unique-ledger:start -->
- L2-CHECK-14 / attempt 1: passed — 正确判断MySQL UNIQUE约束拒绝重复插入，不会自动返回已有订单。下一步SQLAlchemy IntegrityError后的session.rollback与查询；需保留L2-CHECK-13 attempt 5薄弱点。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-14-attempt1-mysql-unique-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-15-attempts1-3-ledger:start -->
- L2-CHECK-15 attempt 1: partial — 指出rollback恢复Session可用，事务回滚范围由教学补充。
- L2-CHECK-15 attempt 2: partial — 判断未提交库存会被rollback撤销，但未给原因。
- L2-CHECK-15 attempt 3: passed — 独立事务A已commit的库存修改不能被事务B rollback撤销，回答及原因完整。
- L2-CHECK-13 attempt 4: evidence correction — 实际回答“直接继续执行”，先前标为错误是记录偏差，已纠正。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-15-attempts1-3-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-5-ledger:start -->
- L2-CHECK-13 / attempt 5: passed（局部复检）— 对exists=False; if not exists: exists=True; print(...)判断会输出，结合之前“直接继续执行”的正确回答，验证了if进入分支后不会因为变量变化自动重查。后续返回Structured Output Chapter 02的EX1正式练习。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-5-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-steps1-2-qa-batch:start -->
- EX1 Step 1 / attempt 1: passed — 独立使用`json.loads(raw_text)`和`Product.model_validate(data)`处理JSON文本。
- EX1 Step 2 / attempt 1: needs_review — `Product.model_validate(data)`正确，但捕获异常的类名写成`Validationerror`而非`ValidationError`，大小写导致NameError；需针对性复检。
<!-- learn-agent:evidence:stage01-ch02-EX1-steps1-2-qa-batch:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-step2-attempt2-ledger:start -->
- EX1 Step 2 / attempt 2: needs_review（部分正确）— 正确判断price="abc"触发校验失败分支，但将`e.errors()`整体错误地说成dict，需理解其为list且元素为dict，安排同概念复检。
<!-- learn-agent:evidence:stage01-ch02-EX1-step2-attempt2-ledger:end -->
