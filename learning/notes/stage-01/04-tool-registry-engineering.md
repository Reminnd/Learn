<!-- learn-agent:evidence:stage01-ch04-start-20261012:start -->
# Chapter 04：Tool Registry与工具工程化

```yaml
schema_version: 2
stage_id: stage-01
chapter_id: 04-tool-registry-engineering
lifecycle_status: active
learning_status: learning
last_updated: 2026-10-12
```

## 4.1 真实工程问题：多个Tool如何统一注册？

Chapter03已经证明LLM提出Tool Call与运行时执行handler是两件事，也实现过get_stock/get_price白名单分发。随着Tool数量上升，分散维护工具列表、参数、超时、权限和风险等级会造成重复代码、同名工具覆盖、失控调用。Tool Registry用一个明确的注册表把外部可调用名称映射到受控ToolSpec/handler及其策略元信息，而不是按LLM提供的字符串调用任意Python对象。

最小Python原理：

```python
def get_stock(sku: str) -> int:
    return {"KB-001": 12}[sku]

def get_price(sku: str) -> int:
    return {"KB-001": 199}[sku]

TOOL_REGISTRY = {
    "get_stock": {"handler": get_stock, "risk": "read_only"},
    "get_price": {"handler": get_price, "risk": "read_only"},
}

def invoke_registered(name: str, args: dict):
    spec = TOOL_REGISTRY.get(name)
    if spec is None:
        raise ValueError(f"Unknown tool: {name}")
    return spec["handler"](**args)
```

后续将映射LangChain工具集合和LangGraph ToolNode，并逐步考虑工具名冲突、失败隔离、Timeout/Retry/权限/审计和结果过大问题。

## L4-CHECK-1 / attempt 1（等待回答）

```python
registry = {}
registry["get_price"] = get_price_v1
registry["get_price"] = get_price_v2
```

问题：此时registry["get_price"]最终指向哪个handler？为什么这在Tool Registry中是一个风险？
<!-- learn-agent:evidence:stage01-ch04-start-20261012:end -->


<!-- learn-agent:evidence:stage01-ch04-ts06-prelude-20261014:start -->
## 2026-10-14：TS-06真实Registry源码先修 / 补课后续学提示

- 已通过的概念检查：Map`set`同名覆盖、`resolve`可能是`undefined`、TS`interface`与`implements`、可选属性/方法、callback执行时机和Closure；`toDisposable`旧句柄不应误删新entry。
- 真实源码Kimi Code：`IAgentToolRegistryService`是编译期类型接口；同名`createDecorator`常量提供运行时服务标识；`registerScopedService`将标识绑定到具体实现类；DI注册系统的重复绑定会拒绝意外覆盖。与Registry内部的工具`register/resolve`是不同两层。App/Session/Agent Scope中，Agent工具集合按作用域各自隔离；Scope并不自动等于安全沙箱。
- 用户在TS-06.5直接回答同名`get_price`两次注册，`resolve`得到`handler_v2`，根据`delete`+同键`set`覆盖；这覆盖了原`L4-CHECK-1`的**结果预测部分**，不应重复提问。
- **仍待原第04章4.1确认**：为什么同名工具无意覆盖在工程上危险？要求给一个具体失败场景，之后继续第04章EX/Q&A，未达mastery不得转第05章。新确认路线要求在第04章完成后先学FastAPI桥接，再讲Agent Loop。
<!-- learn-agent:evidence:stage01-ch04-ts06-prelude-20261014:end -->


<!-- learn-agent:evidence:stage01-ch04-L4-CHECK-1-risk-attempt2-20261014:start -->
## L4-CHECK-1 / 风险解释 attempt 2（needs_review）
- 学习者回答：“因为同名不代表内部实现相同，会因此而丢失tool。”
- **正确部分**：不同工具同名不保证handler逻辑相同；后注册项覆盖Map中的旧工具名绑定，可能失去通过该名称调用原handler的能力。
- **待补充**：未提供可核对的具体业务失败场景；纠正“工具被销毁”与“注册表键映射被覆盖”的概念区分。不重复询问最终取handler_v2这一已通过部分。
- **下一题**：以`get_price`原只读价格、第三方同名插件可能执行其他行为为背景，请学员举一个真实可发生的错误结果/副作用；回答后再推进4.1及第04章EX/Q&A。
<!-- learn-agent:evidence:stage01-ch04-L4-CHECK-1-risk-attempt2-20261014:end -->


<!-- learn-agent:evidence:stage01-ch04-L4-CHECK-1-passed-20261014-original-vs-transaction-price:start -->
## 2026-10-14：L4-CHECK-1 / 同名覆盖风险补答通过

- 题目：同名`get_price`被第三方插件覆盖后，举一个具体业务失败场景。
- 学员独立回答：“新工具：查询原价而不是实际价格，则返回的价格并不是实际价格、失真了。”
- **判定：passed（仅本检查题，不是第04章mastered）**。正确识别同名工具不同语义导致业务价格失真；此前已经正确预测`get_price`对应新handler（后注册覆盖）且理解旧映射被替换。更准确的表述是注册表名称映射失去指向旧handler的能力，不等于原函数对象被销毁。
- **下一教学单元：4.2同名工具冲突防护**。从Python最小`register`加入重复名称检测（拒绝覆盖）开始，再对照Kimi Code的Tool Registry可覆盖策略和DI Scoped Service重复注册保护；只提出一道设计权衡问题。此后继续第04章EX1、LangChain/LangGraph映射与正式Q&A，不自动跳到第05章。
<!-- learn-agent:evidence:stage01-ch04-L4-CHECK-1-passed-20261014-original-vs-transaction-price:end -->


<!-- learn-agent:evidence:stage01-ch04-L4-CHECK-2-policy-choice-passed-20261014:start -->
## 第04章4.2冲突防护策略：独立设计判断已通过

- **检查题**：Coding Agent第三方插件工具重名：A自动覆盖，B默认拒绝、仅明确授权后替换；需说明代价。
- **学生独立回答**：“B，每次替换需要二次确认。”
- **判定：passed（只是单题，不代表本章mastered）**：选择安全默认拒绝，识别了替换须显式授权与额外确认成本。教师补充：并非每次都必须人工弹窗确认；可通过授权策略/配置控制，敏感工具审批更加严格，操作需要审计。
- **下一学习位置**：4.3工具执行失败、超时与重试。先区分读操作的安全重试与带副作用工具的风险（幂等性），只问一个具体场景题；之后继续超时限额、异常处理、LangChain/LangGraph映射和EX1/Q&A。
<!-- learn-agent:evidence:stage01-ch04-L4-CHECK-2-policy-choice-passed-20261014:end -->
