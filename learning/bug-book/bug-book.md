<!-- learn-agent:evidence:bug-stage-01-ch01-chat-model-direction:start -->
## Chat Model 数据流方向混淆

- 症状：曾把 Chat Model 解释成根据 Message 生成供 model 使用的输入。
- 错误模型：认为 Chat Model 位于消息构造器和真正模型之间。
- 根因：混淆了 Prompt 的输入构造职责与 Chat Model 的推理调用职责。
- 修复：Prompt builder 接收用户输入和模板变量，产生 `list[Message]`；Chat Model 接收 `list[Message]`，产生 Assistant Message。
- 避免：解释组件时同时说出输入类型与输出类型。
- 状态：resolved；证据为 L1-CHECK-1 attempt 2。
<!-- learn-agent:evidence:bug-stage-01-ch01-chat-model-direction:end -->

<!-- learn-agent:evidence:bug-stage-01-ch01-python-delimiters:start -->
## Python 字符串与全角括号混用

- 症状：曾写出 `content=" "Answer briefly."）`，Python 无法解析。
- 错误模型：视觉上相似的全角标点可以作为 Python 代码分隔符，或字符串前多一个引号不影响解析。
- 根因：字符串定界符不配对，并混入中文全角右括号。
- 修复：使用配对英文引号与半角括号。
- 避免：代码放入 fenced code block，并使用英文半角引号、逗号和括号。
- 状态：resolved；证据为 L1-CHECK-2 attempt 2。
<!-- learn-agent:evidence:bug-stage-01-ch01-python-delimiters:end -->

<!-- learn-agent:evidence:bug-stage-01-ch02-python-unhandled-typeerror:start -->
## 未捕获 TypeError 的执行行为误解

- 症状：判断 `json.loads` 得到字符串价格后，认为不添加异常处理也不会报错中止。
- 错误模型：把缺少 `try/except` 理解为不会有错误中断。
- 根因：混淆“异常是否产生”与“异常是否被捕获”；同时未区分 JSON 语法解析与业务类型校验。
- 修复：`str + int` 发生 `TypeError`；若未捕获则失败。还需识别 `str * int` 虽合法却不是数值计算。
- 避免：先确定实际类型，定义 Schema；在系统边界使用 Pydantic 校验，并合理捕获/映射异常。
- 状态：resolved；L2-CHECK-1 attempt 2 已正确预测未捕获 TypeError 导致后续语句不执行。
<!-- learn-agent:evidence:bug-stage-01-ch02-python-unhandled-typeerror:end -->

<!-- learn-agent:evidence:bug-stage-01-ch02-raise-vs-except:start -->
## 混淆抛出异常与捕获异常

- 症状：预测 Field(gt=0) 校验失败后只输出 except 内两行，遗漏 except 后的输出；认为程序不会终止是“因为异常抛出了”。
- 错误模型：误以为异常的抛出本身能让程序继续。
- 根因：未区分 `raise` 引发控制流中断与 `except` 捕获匹配异常后继续执行。
- 修复：Pydantic 抛 ValidationError 后跳入 except；当 except 正常结束，继续执行其后语句。 
- 避免：沿代码逐行标出引发异常的位置、捕获入口与捕获块之后的下一条语句。
- 状态：resolved；L2-CHECK-3 attempt 4 已正确解释匹配 except 后继续执行。
<!-- learn-agent:evidence:bug-stage-01-ch02-raise-vs-except:end -->

<!-- learn-agent:evidence:bug-stage-01-ch02-unhandled-valueerror:start -->
## 未捕获的 ValueError 不会继续正常执行
- 症状：预测 raise ValueError、只有 except TypeError 时输出 AD。
- 错误模型：异常不匹配只跳过 except 分支，后续正常代码仍会执行。
- 根因：遗漏未捕获异常的向外传播及其对当前执行流程的中断作用。
- 修复：只有匹配的 except 捕获并正常处理后，try/except 后的语句才在同一执行流程中继续执行；否则异常继续传播。
- 避免：逐步标记异常类型、匹配的处理器、是否已捕获，再判断代码执行。
- 状态：resolved；L2-CHECK-3 attempt 4 正确将 D 的执行归因于异常被捕获。
<!-- learn-agent:evidence:bug-stage-01-ch02-unhandled-valueerror:end -->

<!-- learn-agent:evidence:stage-01-ch02-exception-misconception-resolved:start -->
- 异常处理复检证据：L2-CHECK-3 attempt 4 已正确判断类型匹配的 except 捕获 ValueError 后输出 AED，随后执行正常代码。先前两类误解已完成针对性复检。
<!-- learn-agent:evidence:stage-01-ch02-exception-misconception-resolved:end -->

<!-- learn-agent:evidence:bug-stage-01-ch02-required-fields:start -->
## Pydantic 默认必填字段的判断误区
- 症状：认为 currency: str 未标注 required=True，缺失 currency 不产生校验错误。
- 错误模型：只有显式写 required 才需要输入。
- 根因：没有区分字段类型注解、默认值与允许 None 三项独立维度。
- 修复：Pydantic v2 未提供默认值的字段默认为 required；str = "CNY" 是非必填；str | None 无默认值时仍然必填但可空。
- 避免：读 Schema 时先检查是否有显式默认值，再检查类型与约束。
- 状态：resolved；L2-CHECK-4 attempt 2 已正确解释字段默认值及必填规则。
<!-- learn-agent:evidence:bug-stage-01-ch02-required-fields:end -->

<!-- learn-agent:evidence:bug-stage-01-ch02-required-fields-resolved:start -->
- 状态更新证据：L2-CHECK-4 attempt 2 已正确说明默认值允许省略字段，缺少默认值的 currency 必填。
<!-- learn-agent:evidence:bug-stage-01-ch02-required-fields-resolved:end -->

<!-- learn-agent:evidence:bug-stage-01-ch02-structured-result-type:start -->
## Structured Output返回类型混淆
- 症状：误认为with_structured_output(ProductIn)默认返回包含ProductIn的AIMessage。
- 错误模型：把模型原始消息和经过解析验证的对象视为一个。
- 根因：没有区分ChatModel输出和Structured Output包装层的输出。
- 修复：默认返回ProductIn；include_raw=True返回dict，分别提供raw、parsed和parsing_error。
- 避免：检查Runnable的对外返回类型，理解解析阶段。
- 状态：resolved；L2-CHECK-6 attempt 2正确区分ProductIn对象与AIMessage。
<!-- learn-agent:evidence:bug-stage-01-ch02-structured-result-type:end -->

<!-- learn-agent:evidence:bug-stage-01-ch02-structured-result-type-resolved:start -->
- 复检结论：L2-CHECK-6 attempt 2正确解释with_structured_output(ProductIn)默认返回ProductIn，不能当作AIMessage使用.content。
<!-- learn-agent:evidence:bug-stage-01-ch02-structured-result-type-resolved:end -->

<!-- learn-agent:evidence:bug-stage-01-ch02-raw-vs-parsed-on-validation-failure:start -->
## Structured Output 解析失败后直接使用 raw
- 症状：认为 include_raw=True 解析失败没有 parsed 键，应直接读取 raw.price。
- 错误模型：把模型原始响应 raw 当作已经通过 Schema 校验的数据。
- 根因：混淆 parsed 缺失与 parsed=None，也没有区分原始响应与可用于业务的数据。
- 修复：结果字典包含 parsed，解析失败时为 None；parsing_error 保存错误；raw 仅供诊断。只有检查 parsed 不为 None 后才能读取 parsed.price。
- 避免：始终在业务使用前检查解析结果，明确错误路径并限制重试，避免原始数据绕过校验。
- 状态：resolved；L2-CHECK-7 attempts 7–8 已正确区分校验失败不保存与校验成功保存，并掌握 append 不自动校验的边界。
<!-- learn-agent:evidence:bug-stage-01-ch02-raw-vs-parsed-on-validation-failure:end -->

<!-- learn-agent:evidence:bug-stage-01-ch02-raw-vs-parsed-validation-review-20261010:start -->
- 修正补充：raw可以绕过校验进入后续应用，错误不一定以异常呈现；可能被文本字段接受、发生字符串重复运算等静默错误。需通过新场景复检，而不能仅凭“会抛出异常”判断安全。
<!-- learn-agent:evidence:bug-stage-01-ch02-raw-vs-parsed-validation-review-20261010:end -->

<!-- learn-agent:evidence:bug-stage-01-ch02-raw-vs-parsed-attempt4-review:start -->
- 本轮补充：不能以错误字符串不会参与正确数学运算解释 append 为什么不报错；直接原因是该代码没有执行数值操作，也没有 Schema 校验。保存成功与业务价格有效是不同条件。
<!-- learn-agent:evidence:bug-stage-01-ch02-raw-vs-parsed-attempt4-review:end -->

<!-- learn-agent:evidence:bug-stage-01-ch02-raw-vs-parsed-resolved-after-validation:start -->
- 复检：无效价格raw={"price":"abc"}经Pydantic验证失败，不进入append；有效价格raw={"price":199}通过验证后才添加ProductIn实例，currency使用默认CNY。结合之前“append本身不校验”，完成raw与validated数据边界复检。
<!-- learn-agent:evidence:bug-stage-01-ch02-raw-vs-parsed-resolved-after-validation:end -->

<!-- learn-agent:evidence:bug-stage01-ch02-retry-save-count-resolved:start -->
## 重试尝试次数与保存次数混淆
- 症状：初次把2次尝试等同于2次append。
- 错误模型：每次循环尝试均会保存一项。
- 根因：忽略了except中的continue会跳过append。
- 修复：逐轮判断ValidationError、continue、append、break实际路径。
- 避免：分开计数尝试、通过校验与保存次数。
- 状态：resolved，L2-CHECK-8 attempt 2正确说明第二次成功后break，最终只保存1项。
<!-- learn-agent:evidence:bug-stage01-ch02-retry-save-count-resolved:end -->

<!-- learn-agent:evidence:bug-stage01-ch02-concurrency-message-list-confusion:start -->
## 并发请求与消息列表顺序混淆
- 症状：将请求A、B的竞态问题解释成“消息列表不处于先后关系”。
- 错误模型：认为没有消息顺序就是订单重复的直接原因。
- 根因：没有跟踪两个独立请求各自的检查与创建步骤，以及跨请求执行的交错顺序。
- 修复：A检查无记录→B检查无记录→A创建→B创建；检查与创建不具原子性，重复副作用就可能发生。
- 避免：并发问题用事件时间线写出每个参与者的读与写；明确状态共享边界，考虑数据库唯一约束与事务。
- 状态：open；等待 L2-CHECK-13 attempt 2 复检。
<!-- learn-agent:evidence:bug-stage01-ch02-concurrency-message-list-confusion:end -->

<!-- learn-agent:evidence:bug-stage01-ch02-same-function-not-atomic:start -->
## 同一函数不自动构成原子操作
- 症状：认为if检查与后续创建在同一Python函数内，所以是一个不可分割的原子操作。
- 错误模型：函数封装提供跨线程、跨进程和跨服务的并发互斥。
- 根因：未区分代码结构与线程/服务执行的交错调度、数据库事务原子性。
- 修复：A检查不存在之后、A创建之前B可以检查并创建；A不会自动重新检查，仍可能执行创建。单纯同函数不足以保证幂等。
- 避免：用时间线分析多个请求对共享状态的读写，利用数据库唯一约束/事务或等价协调保证业务唯一性。
- 状态：open；待L2-CHECK-13 attempt 3复检。
<!-- learn-agent:evidence:bug-stage01-ch02-same-function-not-atomic:end -->

<!-- learn-agent:evidence:bug-stage01-ch02-atomicity-if-auto-recheck:start -->
- 误区：以为if条件在共享数据变化后会自动重判。
- 纠正：if仅在执行到条件时判定，进入分支后不会自行跳回。需显式再检查才能得到新值。
- 状态：resolved（更正）；用户正确表示A会从if判断后的暂停位置继续执行，不自动重判。
<!-- learn-agent:evidence:bug-stage01-ch02-atomicity-if-auto-recheck:end -->

<!-- learn-agent:evidence:stage01-ch02-if-controlflow-evidence-correction:start -->
- 记录更正：用户在L2-CHECK-13 attempt 4实际回答“直接继续执行”，正确判断if不会自动重判；此前误记为错误。可继续用简单代码巩固并发检查与创建的边界。
<!-- learn-agent:evidence:stage01-ch02-if-controlflow-evidence-correction:end -->

<!-- learn-agent:evidence:bug-stage01-ch02-EX1-ValidationError-case:start -->
## Pydantic ValidationError大小写误写
- 症状：EX1中导入ValidationError，却在except中使用Validationerror。
- 错误模型：异常类名大小写不影响Python查找。
- 根因：标识符大小写不匹配，真正发生ValidationError时，except求值会触发NameError。
- 修复：使用`except ValidationError as e:`，保留打印e.errors()。
- 避免：核对导入名及捕获名一致，实际运行Schema错误用例验证处理分支。
- 状态：open；等待EX1 Step 2 attempt 2复检。
<!-- learn-agent:evidence:bug-stage01-ch02-EX1-ValidationError-case:end -->

<!-- learn-agent:evidence:bug-stage01-ch02-validationerror-errors-list:start -->
## Pydantic ValidationError.errors() 数据结构误解
- 症状：认为`print(e.errors())`输出一个字典。
- 错误模型：一个ValidationError对象对应单个字典，不会聚合多个字段错误。
- 根因：混淆返回列表和列表中每个错误的字典。
- 修复：`e.errors()`返回列表，常见为`[{"type": ..., "loc": ..., "msg": ..., "input": ...}]`；多字段失败可能有多个元素。
- 避免：用`type(...)`和`len(...)`检查容器，再访问`errors()[0]["type"]`。
- 状态：resolved；EX1 Step2 attempt3 正确区分e.errors()整体为list、每个错误项为dict。
<!-- learn-agent:evidence:bug-stage01-ch02-validationerror-errors-list:end -->

<!-- learn-agent:evidence:bug-stage01-ch02-validationerror-errors-list-resolved:start -->
- 复检证据：EX1 Step2 attempt3用户正确答出列表、字典，表示已理解Pydantic错误列表与内部字典的区别。
<!-- learn-agent:evidence:bug-stage01-ch02-validationerror-errors-list-resolved:end -->
