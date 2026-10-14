<!-- learn-agent:evidence:stage01-supplemental-20261013-plan-v1:start -->
# Stage 01｜新增知识专项补课记录（2026-10-13）

> 该文件位于manifest的`notes.root`之下，维护**已完成章节新增知识**的补课计划与后续答题证据；不是新的正式章节，不替代旧章已经提交的mastery记录。当前状态：**R01、R02、R03已通过**（2026-10-14，依据下列真实对话答题）。本补课只增加知识证据，不改变原第01–03章mastery与成绩。课程说明见[定向补课教材](../../../curriculum/stage-01/retroactive-review-20261013.md)（从仓库根目录引用：`curriculum/stage-01/retroactive-review-20261013.md`）。

## 补课队列（所有通过状态必须以后续用户回答的真实证据为准）

| 任务ID | 所属已完成章节 | 只补新增知识 | 状态 | 答题证据 |
|---|---|---|---|---|
| R01 | Stage 01/01（mastered=82） | Prompt Chaining与固定Workflow / Agent边界 | **passed** | A固定Workflow、B动态Agent；区分控制流与额外token、时延等开销 |
| R02 | Stage 01/02（mastered=82） | Pydantic与TS静态类型/AJV运行时Schema校验 | **passed** | 明确interface不足、须在Handler前运行时校验；纠正TS用AJV/Zod、Python用Pydantic |
| R03 | Stage 01/03（mastered=84） | Tool Calling与ReAct区分，Kimi Python Toolset源码 | **passed** | bind_tools+tool_calls不足；需Handler、ToolMessage、模型循环决策直至结束 |

- **优先顺序**：R01 → R02 → R03；一回合仅问一题，先讲新增知识再复检。
- **通过准则**：在没有直接展示标准答案的前提下，用户能独立解释关键因果关系、控制流以及至少一个适用或失败边界；如不通过只复检该任务。
- **学习证据分级**：阅读源码不等于独立编写；项目来源与作者归属不能凭项目访问记录推断。仅记录真实回答、阅读/运行行为，不凭计划本身生成passed/mastered。
- **当前正式章节与章节验收不变**：`stage-01/04-tool-registry-engineering`仍处于`learning`，第01–03章仍为completed；未来第05章ReAct完整循环不提前毕业。

## 原课程待答问题（补课结束后必须精确恢复）

```yaml
stage_id: stage-01
chapter_id: 04-tool-registry-engineering
chapter_file: curriculum/stage-01/04-tool-registry-engineering.md
note_pointer: stage-01/04-tool-registry-engineering.md
last_section: 4.1 Tool Registry统一注册与同名工具冲突
current_activity: learning
return_to:
  activity: knowledge_check
  topic: L4-CHECK-1 / attempt 1
  next_action: 回答重复注册get_price时会使用哪个handler，并说明风险。
next_action: L4-CHECK-1 attempt1：解释Registry同名工具覆盖并识别风险。
```

## 后续答题记录（2026-10-14：R01–R03已通过）

<!-- learn-agent:evidence:stage01-supplemental-r01-r03-passed-20261014:start -->
- **R01 passed**：用户独立判断“固定标题提取→翻译”为Workflow；依据模型在执行中是否动态选择行动判断Agent；能说出Agent引入token/延迟/非确定性成本。这是第01章新增知识，不重评82分。
- **R02 passed**：用户回答TypeScript的`interface Product { price: number }`配合`as Product`不能保证外部JSON字段为数字；Handler调用前需要Pydantic式的实际验证。教师补充准确区分Python=Pydantic、TypeScript=AJV/Zod；对应真实Kimi Code`compileToolArgsValidator`/`validateToolArgs`源码。仅证明概念理解，未独立编写TS validator。
- **R03 passed**：面对`bind_tools(...)`返回`tool_calls`但没有执行handler也没有回传ToolMessage的案例，用户独立回答“不算ReAct，缺执行Handler、工具结果作为ToolMessage回传、模型继续决定下一步直到结束”。读到真实Kimi CLI`KimiToolset.add/find`用于说明注册≠执行，未声称用户亲自运行该开源项目。
- **TS-0补习衔接**：本轮对话针对真实Kimi Code/Pi代码逐题学习了基本函数/返回类型、Promise/回调、interface/implements、Map、同名工具覆盖、IDisposable、闭包、DI服务标识/实现绑定、App/Session/Agent作用域；属源码阅读理解，不等于独立项目实现。TS运行时校验差异已通过R02。
- **恢复**：原formal chapter仍是Stage01/04，last_section=4.1；复用原`L4-CHECK-1`。在TS-06.5的独立作答中，用户已正确解释同名注册最终是`handler_v2`；**尚需独立说明“不受控同名覆盖”可能造成什么工程风险**，再继续正式EX/Q&A。不能重复要求预测`handler_v2`。
<!-- learn-agent:evidence:stage01-supplemental-r01-r03-passed-20261014:end -->
<!-- learn-agent:evidence:stage01-supplemental-20261013-plan-v1:end -->
