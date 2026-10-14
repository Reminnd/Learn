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
