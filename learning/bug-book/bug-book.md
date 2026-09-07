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
