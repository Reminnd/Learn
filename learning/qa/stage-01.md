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

<!-- learn-agent:evidence:stage01-ch02-EX1-step2-attempt3-ledger:start -->
- EX1 Step 2 / attempt 3: passed（局部检查）— 正确回答e.errors()的容器为list，首个错误对象为dict。随后进入EX1 Step 3 LangChain with_structured_output框架实现；完整EX1需实际运行与框架映射验证。
<!-- learn-agent:evidence:stage01-ch02-EX1-step2-attempt3-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-step3-attempt1-ledger:start -->
- EX1 Step 3 / attempt 1: passed — 正确独立写出with_structured_output(Product)与structured_model.invoke(...)，理解返回Product实例；仍需实际运行及错误用例验证，不代表整章mastered。
<!-- learn-agent:evidence:stage01-ch02-EX1-step3-attempt1-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-step4-offline-principle-run-20261011-ledger:start -->
- EX1 Step 4: passed（已观察学习者提交的运行stdout）— Case1 PASS并生成整数199及currency CNY；Case2按预期校验拒绝，e.errors()是list且错误type=int_parsing。下一步无API LangChain PydanticOutputParser/RunnableLambda框架验证，完整EX1尚未正式通过。
<!-- learn-agent:evidence:stage01-ch02-EX1-step4-offline-principle-run-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-step5-deepseek-live-api-passed-ledger:start -->
- EX1 Step 5 / real DeepSeek API: passed — 用户提交真实stdout：raw_type AIMessage；parsed_type Product；product={'price': 199, 'currency': 'CNY'}；parsing_error None。之前401认证问题已排除。EX1实际实现与运行路径齐备，转入概念验收Q1/Q2/Q3；仍不得标记Chapter02 mastered。
<!-- learn-agent:evidence:stage01-ch02-EX1-step5-deepseek-live-api-passed-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-Q1-attempt1-20261011-ledger:start -->
- Chapter02 Q1 / attempt1: needs_review（方向正确，原因不全）— 用户认识到Schema校验与字段缺失、错误语义数据风险；尚未说明普通语言答案措辞/格式不固定令程序解析脆弱，且“确保”表述太绝对。目标复检自然语言格式变化为何使split或正则不可靠。
<!-- learn-agent:evidence:stage01-ch02-Q1-attempt1-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-Q1-attempt2-20261011-ledger:start -->
- Chapter02 Q1 / attempt2: needs_review — 用户回答“可能没有采用实际价格”属于语义准确性风险，但未命中固定split解析自由文本为什么会失败的格式原因。已给A/C无分隔符导致IndexError、B残留“元”的反例；下轮以分隔符不匹配的列表长度复检。
<!-- learn-agent:evidence:stage01-ch02-Q1-attempt2-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-Q1-attempt3-guided-20261011-ledger:start -->
- Chapter02 Q1 / attempt3: partial — 正确判断未找到分隔符时split返回单元素列表、长度为1，但仍询问split的分隔原理；已讲解精确匹配规则。
<!-- learn-agent:evidence:stage01-ch02-Q1-attempt3-guided-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-Q1-attempt4-pass-20261011-ledger:start -->
- Chapter02 Q1 / attempt4: passed（指导式复检）— 针对缺少分隔符的单元素列表访问[1]，学习者正确判定抛出"找不到元素"类异常；补充精确类型IndexError。结合早先Schema字段缺失/语义误提取风险答案，Q1综合判定通过，进Q2。不是对完整原理的独立首轮答案。
<!-- learn-agent:evidence:stage01-ch02-Q1-attempt4-pass-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-Q2-attempt1-20261011-ledger:start -->
- Q2 attempt1: needs_review — A输入JSON文本、最终Product判断正确；B提示词输入正确，但把默认解析输出误说成AIMessage（实际默认Product，include_raw=True时raw才是AIMessage）；下一题针对性测试返回类型，再验收完整数据流。
<!-- learn-agent:evidence:stage01-ch02-Q2-attempt1-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-Q2-attempt2-20261011-ledger:start -->
- Q2 / attempt2: needs_review — 学习者认为调用结果是Product实例（对），却预测type(...).__name__按数量变成dict/list（错）；已讲解实例类型和model_dump字典区别，下一题对照两个类型名。
<!-- learn-agent:evidence:stage01-ch02-Q2-attempt2-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-Q2-attempt3-model-dump-confusion-20261011-ledger:start -->
- Q2 / attempt3: needs_review — Product实例类型答对，但对model_dump()返回值答为AIMessage，并表示不清楚；已解释Pydantic model_dump产生dict，不涉及LLM调用。下一题转向字典实际访问而非重复类型名，随后回到Q2映射。
<!-- learn-agent:evidence:stage01-ch02-Q2-attempt3-model-dump-confusion-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-Q2-attempt4-20261011-ledger:start -->
Q2 attempt4: 选择了正确的字典读取方式。Q2仍未完成整体验收。
<!-- learn-agent:evidence:stage01-ch02-Q2-attempt4-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-Q2-attempt5-local-validation-20261011-ledger:start -->
Q2 attempt5：A、B输入与Product返回答对，B模型调用位置答对。A的Pydantic本地校验不是LLM调用。复检继续。
<!-- learn-agent:evidence:stage01-ch02-Q2-attempt5-local-validation-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-Q2-attempt6-passed-20261011-ledger:start -->
- Q2 attempt6: passed（指导复检）— 用户正确指出model.invoke向DeepSeek发送请求，json.loads解析JSON，Product.model_validate本地Schema校验。结合attempt5对A/B输入输出和B调用位置的回答，原理—框架映射关键题通过；进入Q3，整章mastered尚未判定。
<!-- learn-agent:evidence:stage01-ch02-Q2-attempt6-passed-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-Q3-attempt1-20261011-ledger:start -->
- Q3 attempt1: needs_review — 提出有限调用LLM重试、达到3次上限后报错，排查方向为JSON格式→输入内容→代码。未先查Pydantic int_parsing的字段/原始值，也未给API成本、延迟、修复可能性的Trade-off；本例JSON合法而Schema失败，待针对性复检。
<!-- learn-agent:evidence:stage01-ch02-Q3-attempt1-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch02-Q3-attempts2-3-ledger-20261011:start -->
- Q3 attempt2: 部分正确。A有商品价格可尝试有限重试，B无价格应返回缺失错误；未论证费用与延迟。
- Q3 attempt3: Trade-off通过。说明A有修复可能且重试次数受限控制成本，B无源价格证据故重试徒增API费用和延迟。Q3整体仍缺独立排查错误的顺序，继续attempt4。
<!-- learn-agent:evidence:stage01-ch02-Q3-attempts2-3-ledger-20261011:end -->

<!-- learn-agent:evidence:stage01-ch02-final-mastered-qa-20261011:start -->
Chapter 02 Q3 attempt4: passed (price字段、abc非整数、按模型输出/Schema/原文排查)。Q3 attempt3已说明有限重试成本与延迟。EX1可执行原理版与真实DeepSeek API结果齐备。Q1、Q2指导式复检通过。依据章节契约五维评分19+16+18+17+12=82/100，达到80分与各项硬门槛，综合验收通过。
<!-- learn-agent:evidence:stage01-ch02-final-mastered-qa-20261011:end -->

<!-- learn-agent:evidence:stage01-ch03-checks1-2-qa-batch-20261011:start -->
- L3-CHECK-1 attempt1: passed — Tool Call指令不是实际执行handler。
- L3-CHECK-2 attempt1: needs_review — handler(args)将字典作为一个位置参数传入，而非展开sku关键字。
- L3-CHECK-2 attempt2: passed（指导）— 正确指出**args形成关键字实参sku="KB-001"；教师补充sku类型str。转入@tool。
<!-- learn-agent:evidence:stage01-ch03-checks1-2-qa-batch-20261011:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECKS3-5-batch-20261011-ledger:start -->
- L3-CHECK-3 / attempt1: passed — @tool定义不调用handler，get_stock.invoke触发库存查询。
- L3-CHECK-4 / attempt1: passed — invoke({})缺sku，参数Schema在执行handler之前报ValidationError。
- L3-CHECK-5 / attempt1: passed（教师补充精确错误名）— 有效str类型的不存在SKU可通过Schema并进入handler，inventory[sku]因缺少键抛KeyError。进入业务错误处理小练习。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECKS3-5-batch-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch03-check6-check7-20261011-ledger:start -->
L3-CHECK-6通过：业务库存键不存在是KeyError，不是输入ValidationError。L3-CHECK-7部分正确：get_price改为查询价格正确，get_stock用“查询商品详情”仍含糊。下次复检库存工具说明。
<!-- learn-agent:evidence:stage01-ch03-check6-check7-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-7-attempt2-ledger:start -->
- L3-CHECK-7 / attempt2: passed — 将get_stock description准确改为“查询商品库存数量”，区分价格与库存职责。进入3.6 DeepSeek bind_tools真实API观察，模型返回Tool Call不代表Python handler已执行。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-7-attempt2-ledger:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-8-live-deepseek-pass-20261011-ledger:start -->
- L3-CHECK-8: passed — 用户真实调用DeepSeek，获得AIMessage，其tool_calls正确包含get_stock、args sku=KB-001，content为空。尚未运行Python工具；进入3.7手写Runtime。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-8-live-deepseek-pass-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-9-attempt1-20261011-ledger:start -->
- L3-CHECK-9 / attempt1: needs_review — 识别call["args"]字典正确，但对@tool包装的LangChain StructuredTool直接使用selected_tool(**call["args"])；应采用selected_tool.invoke(call["args"])。下一题复检工具对象与普通函数调用区别。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-9-attempt1-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-9-attempt2-qa-20261011:start -->
- L3-CHECK-9 attempt2: needs_review — 重复使用selected_tool.invoke(**call["args"])并认为其输出为ToolMessage；应使用invoke(call["args"])得到整数12，完整ToolCall输入可触发框架生成ToolMessage。安排attempt3。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-9-attempt2-qa-20261011:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-9-attempt3-pass-20261011-ledger:start -->
- L3-CHECK-9 attempt3: passed — 正确指出get_stock.invoke(args)返回int和12；主动询问handler(**args)与Tool.invoke(args)的区别，已按函数签名及invoke(input)解释。下一步ToolMessage关联与回传。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-9-attempt3-pass-20261011-ledger:end -->

<!-- learn-agent:evidence:stage01-ch03-toolmsg-a1-qa:start -->
- L3-CHECK-10 attempt1: needs_review. User knows ToolMessage tool_call_id identifies a tool call, but supplied arbitrary 001; need to reuse the model's call["id"].
<!-- learn-agent:evidence:stage01-ch03-toolmsg-a1-qa:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK10a2a3-11-ledger:start -->
- L3-CHECK-10 attempt2: needs_review — call[id]缺少字符串引号。
- L3-CHECK-10 attempt3: passed — 正确使用call["id"]读取原始模型工具调用ID。
- L3-CHECK-11: passed — 用户真实DeepSeek运行输出工具结果12，最终自然语言答复KB-001库存12，闭环成功。当前仍仅支持一次Tool Call。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK10a2a3-11-ledger:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK12-14-ledger-20261012:start -->
- L3-CHECK-12: passed — len(tool_calls)==2导致!=1为真，抛RuntimeError，工具均未执行。
- L3-CHECK-13: passed（语法提醒）— 应使用for call in response.tool_calls: 遍历所有调用；[0]只获取第一条。
- L3-CHECK-14: passed — messages.extend(tool_messages)使多个ToolMessage作为独立消息元素，而非append所产生的列表嵌套。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK12-14-ledger-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-15-qa-20261012:start -->
L3-CHECK-15: passed. User ran DeepSeek multi-tool test with get_stock=12 and get_price=199; model gave correct final answer. Next: tool exceptions.
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-15-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-check16-18-qa-20261012:start -->
- L3-CHECK-16 passed: handler KeyError without try/except stops subsequent price tool.
- L3-CHECK-17 passed: use except KeyError to isolate missing SKU.
- L3-CHECK-18 attempt1 needs_review: unknown tool name in tools_by_name[name] raises KeyError outside try. Contrast dict.get returning None. Retest next.
<!-- learn-agent:evidence:stage01-ch03-L3-check16-18-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-check18a2-19a1-qa-20261012:start -->
- L3-CHECK-18 attempt2: passed — 工具名未知时dict.get(...)返回None，打印UNKNOWN_TOOL。
- L3-CHECK-19 attempt1: needs_review — 正确判定continue使未知工具无ToolMessage；误以为DeepSeek会不断重试。缺失关联工具结果可能导致请求校验失败；应给该call["id"]返回失败ToolMessage后继续。
<!-- learn-agent:evidence:stage01-ch03-check18a2-19a1-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK19a2-20-21-ledger-20261012:start -->
Checks 19, 20, 21 passed. ToolMessage ID, ValidationError, and diagnostic logging.
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK19a2-20-21-ledger-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK22-attempt1-qa-20261012:start -->
L3-CHECK-22 attempt1: needs_review. Correct risk: oversized review ToolMessage uses context and dilutes key points. Suggested batching/vector similarity need a strategy for overall theme coverage and a tradeoff discussion. Next: risks of only returning frequent pros/cons themes.
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK22-attempt1-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-check22-a2-rare-angle-20261012-qa:start -->
L3-CHECK-22 attempt2: partial. Provide specific example next.
<!-- learn-agent:evidence:stage01-ch03-check22-a2-rare-angle-20261012-qa:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK22-attempt3-ledger-20261012:start -->
- L3-CHECK-22 attempt3: passed — 举出无线键盘“续航”这一可能低频但影响购买决策的评价维度，充分说明压缩高频主题会遗漏关键信息的Trade-off；转入Chapter03 Q1正式验收。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK22-attempt3-ledger-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q1-a1-qa-20261012:start -->
- Chapter03 Q1 / attempt1: needs_review. 学员能解释name、description、handler的主要用途以及请求与执行分离；但将parameters泛称为元数据，未明确它是输入Schema，也尚未举出定义错误如何导致失败的具体案例。下一题Q1 attempt2：补充一个实际故障示例。
<!-- learn-agent:evidence:stage01-ch03-Q1-a1-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q1-a2-input-vs-output-qa-20261012:start -->
- Chapter03 Q1 attempt2: needs_review — 举例把parameters输入Schema当作返回值int类型验证，并误以为ToolMessage接收str就必然报错。正确区分输入sku约束、handler输出以及ToolMessage序列化；下一次Q1 attempt3只举一个会被get_price输入Schema拒绝的调用及错误阶段。
<!-- learn-agent:evidence:stage01-ch03-Q1-a2-input-vs-output-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q1-attempt3-ledger-20261012:start -->
- Chapter03 Q1 attempt3: passed（critical）— 用户给出get_price.invoke(12)作为错误输入例子，结合先前L3-CHECK-20清楚区分Pydantic输入校验失败与handler未执行的证据，及Q1 attempt1对name、description和handler作用的解释，达到Q1全部验收要求。下一题Q2原理与@tool映射。
<!-- learn-agent:evidence:stage01-ch03-Q1-attempt3-ledger-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q2-attempt1-qa-20261012:start -->
- Chapter03 Q2 attempt1: needs_review — 正确区分普通函数**args与@tool.invoke(args)，但尚未说明@tool元信息、输入Schema、模型工具选择与运行验证；Q2 attempt2复检新增能力。
<!-- learn-agent:evidence:stage01-ch03-Q2-attempt1-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q2-attempt2-20261012-qa:start -->
- Chapter03 Q2 attempt2: needs_review — 认识单参数Tool.invoke可传字符串（当前LangChain支持），但把args_schema与model.with_structured_output混同；需复检输入校验与模型输出校验的区别，并补全@tool生成元信息与运行时调用。
<!-- learn-agent:evidence:stage01-ch03-Q2-attempt2-20261012-qa:end -->

<!-- learn-agent:evidence:stage01-ch03-Q2-3and4-ledger-20261012:start -->
- Chapter03 Q2 attempt3: passed — args_schema管Tool输入，with_structured_output管LLM结构化输出。
- Chapter03 Q2 attempt4: passed（critical）— 学员串联description→Tool Call→按name路由→invoke/args_schema→handler返回199→ToolMessage回传；教师补充查表由手写Runtime而非bind_tools自动执行。结合此前raw_get_price(**args)、get_price.invoke(args)及真实DeepSeek实测，Q2正式通过。下题Q3参数错误排查与Trade-off。
<!-- learn-agent:evidence:stage01-ch03-Q2-3and4-ledger-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q3-a1-review-20261012-qa:start -->
- Q3 attempt1 needs_review: 有错误日志→call→query排查思路，了解有限重试的Token成本和无效风险；未对照Tool args_schema，也未修复product_id/sku键名不匹配。复检直接原因与修复。
<!-- learn-agent:evidence:stage01-ch03-Q3-a1-review-20261012-qa:end -->

<!-- learn-agent:evidence:stage01-ch03-Q3-attempt2-qa-20261012:start -->
- Chapter03 Q3 attempt2: needs_review — 识别args不匹配，但把product_id字段名错误说成str类型不符，并提出严格校验；实际"KB-001"是字符串，缺失必填sku导致ValidationError。下次复检正确args字典。
<!-- learn-agent:evidence:stage01-ch03-Q3-attempt2-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q3-a3-sku-value-qa-20261012:start -->
Q3 attempt3: partial. Schema passes but handler cannot find SKU 001.
<!-- learn-agent:evidence:stage01-ch03-Q3-a3-sku-value-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q3-a4-ledger-20261012:start -->
Chapter03 Q3 passed. Correct call args sku=KB-001, price 199. Combined diagnostic and retry tradeoff evidence. EX1 next.
<!-- learn-agent:evidence:stage01-ch03-Q3-a4-ledger-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-EX1-p1-a1-qa-20261012:start -->
- Chapter03 EX1 Part1 attempt1: needs_review — correct tool name and description, but parameters=sku: str is not valid nested dict data and handler="raw_get_price" stores a string rather than a Python callable. Next: repair these two fields.
<!-- learn-agent:evidence:stage01-ch03-EX1-p1-a1-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-EX1-p1-a2-qa-20261012:start -->
- Chapter03 EX1 Part1 attempt2: needs_review — valid {"sku": str} type map and correct raw_get_price function reference. Missing explicit requiredness in custom Tool parameters; next attempt3 needs both str type and required flag.
<!-- learn-agent:evidence:stage01-ch03-EX1-p1-a2-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-EX1-part1-a3-ledger-20261012:start -->
- Chapter03 EX1 Part1 attempt3: passed — correctly identified True for requiredness. Teacher clarified Python dict syntax "required": True (not required=True). Original Tool declaration now complete; EX1 runtime validation, dispatch, and @tool mapping remain.
<!-- learn-agent:evidence:stage01-ch03-EX1-part1-a3-ledger-20261012:end -->

<!-- learn-agent:evidence:ch03-ex1-required-membership-a1-qa-20261012:start -->
EX1 Part2 attempt1 needs_review: reading args['sku'] is not a key-existence test. Use field not in args.
<!-- learn-agent:evidence:ch03-ex1-required-membership-a1-qa-20261012:end -->

<!-- learn-agent:evidence:ch03-ex1-required-pass-type-check-qa-20261012:start -->
- EX1 Part2 attempt2: passed — existing sku key means field not in args is False and code prints PASS.
- EX1 Part3 attempt1: needs_review — student used isinstance(...) without not in if condition for raising TypeError, reversing valid and invalid cases. Retest next.
<!-- learn-agent:evidence:ch03-ex1-required-pass-type-check-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-EX1-type-check-a2-qa-20261012:start -->
- EX1 Part3 attempt2: passed — correctly predicts PASS from not isinstance(valid_sku, str) == False. Proceeds to original runtime handler execution.
<!-- learn-agent:evidence:stage01-ch03-EX1-type-check-a2-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-ex1-handler-a1-passed-qa-20261012:start -->
- EX1 Part4 attempt1: passed — using handler(**args) to call original Python function gets 199. Next integrated EX1 exercise to combine requiredness/type validation and handler, then verify mapping to LangChain @tool.
<!-- learn-agent:evidence:stage01-ch03-ex1-handler-a1-passed-qa-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-ex1-integrated-attempt1-hardcoded-20261012-qa:start -->
EX1 integrated attempt1 needs_review: required/type checks and dispatch correct, but latest version hardcodes return 199 after ignoring the handler's result. Retest dynamic return.
<!-- learn-agent:evidence:stage01-ch03-ex1-integrated-attempt1-hardcoded-20261012-qa:end -->
