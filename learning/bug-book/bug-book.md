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
