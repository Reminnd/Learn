<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-1-attempt-1:start -->
# Chapter 02：Structured Output（结构化输出）

```yaml
schema_version: 2
stage_id: stage-01
chapter_id: 02-structured-output
lifecycle_status: active
learning_status: learning
last_updated: 2026-10-10
```

## 2.1 为什么需要结构化输出

用户让 Agent 从商品描述提取价格。自然语言回答（如“售价199元”）不等于可直接安全计算的程序数据。JSON 便于字段访问，但 `json.loads()` 只负责 JSON 语法解析，不强制 `price` 的业务数值类型。

```python
import json
raw = '{"price": "199", "currency": "CNY"}'
data = json.loads(raw)
assert isinstance(data["price"], str)
```

- `data["price"] + 10` 会抛出 `TypeError`，若未捕获异常，执行路径会因异常中断；
- `data["price"] * 2` 会返回字符串 `"199199"`，不会产生希望的数值 `398`；
- 下一步引入 Pydantic 的 Schema 和类型校验，之后映射到 LangChain Structured Output 以及 FastAPI 的输入/输出边界。

## L2-CHECK-1 / attempt 1

状态：needs_review（局部知识检查，不是章节 mastery 判定）。

- 已掌握：`"199"` 是 Python `str` 而不是 `int`，不能视为已经完成数值解析。
- 需修正：用户认为未加入异常处理时“不会报错中止”；正确行为是类型不兼容的加法抛出 `TypeError`，若异常一直未被捕获，则当前执行路径失败。
- 特别提醒：类型不符并不总能产生异常；字符串重复运算就是无异常的业务错误示例。

下一步：L2-CHECK-1 / attempt 2，同概念复检，待答对后继续 Pydantic。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-1-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-1-attempt-2:start -->
## L2-CHECK-1 / attempt 2

状态：passed。用户正确说明 `price = "199"` 是 `str`，表达式 `price + 10` 抛出 `TypeError`；由于没有异常捕获，后续 `print("程序执行完毕")` 不会执行。与 attempt 1 的误解相同的核心概念已完成复检。

## 2.2 Pydantic v2：Schema 与校验

下一步引入 `BaseModel`、字段类型声明、`model_validate` 和 `ValidationError`，解释 Pydantic 默认可转换的 lax validation 和 strict mode。围绕商品价格案例建立原理版与企业实现版的对应，不把“合法 JSON”混同于“业务类型已被保证”；后续再映射到 FastAPI 与 LangChain。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-1-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-1:start -->
## 2.3 ValidationError 与异常捕获

商品数据业务边界通过 Pydantic BaseModel 与 Field(gt=0) 定义正数价格：

```python
from pydantic import BaseModel, Field, ValidationError
class Product(BaseModel):
    price: int = Field(gt=0)
    currency: str
try:
    product = Product.model_validate({"price": -20, "currency": "CNY"})
    print("校验成功")
except ValidationError as e:
    print("校验失败")
    print(e.errors())
print("程序继续执行")
```

这次校验会抛出 `ValidationError`，由匹配的 `except` 捕获。依次打印“校验失败”、包含价格字段 `greater_than` 约束不满足的结构化错误列表以及“程序继续执行”。

### L2-CHECK-3 / attempt 1

状态：needs_review。用户正确指出 `price=-20` 会导致 ValidationError，并进入 except；但漏掉 except 后的“程序继续执行”，并把“为什么不直接中止”的原因归结为“异常抛出了”，而不是异常已被 `except ValidationError` 捕获。

下一步：同概念复检 L2-CHECK-3 / attempt 2，区分抛出和捕获后代码的执行位置，再推进 `e.errors()` 结构、FastAPI 422 的边界与 LangChain 结构化输出。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-2-attempt-1:start -->
## L2-CHECK-2 / attempt 1
状态：passed。正确回答 Pydantic 默认模式把字符串 "199" 转为整数 199；strict=True 不允许隐式转换，校验失败。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-2-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-2:start -->
## L2-CHECK-3 / attempt 2
状态：needs_review。用户正确预测 ACD，但问 raise ValueError("test") 和 except ValueError 含义，以及为什么不打印 B。已讲解 raise 抛出异常时跳过 try 剩余语句，找到匹配的 except 后打印 C，然后继续打印 D。待判断异常处理类型不匹配的情形。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-3:start -->
## L2-CHECK-3 / attempt 3
状态：needs_review（部分正确）。用户正确解释 raise ValueError 时 B 不执行，except TypeError 类型不匹配因此 C 不执行；但错误预测输出 AD，未认识到未捕获 ValueError 传播并阻止执行随后 print("D")。正确执行为输出 A，然后出现未捕获 ValueError traceback（顶层脚本条件）。已讲解匹配异常处理器决定能否继续执行后续语句。下一步 L2-CHECK-3 / attempt 4 对比多个 except 分支并解释为何 D 能输出。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-3:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-4:start -->
## L2-CHECK-3 / attempt 4
状态：passed。用户正确预测 raise ValueError、依次有 except TypeError/except ValueError 时输出 A、E、D，并说明根因是 ValueError 被成功捕获。相比上次误判未捕获异常后仍执行 D，已正确区分“匹配捕获后继续”与“未捕获异常传播”。异常控制流知识检查完成。

## 2.4 Pydantic ValidationError.errors()
`e.errors()` 返回含每一项错误详情的列表。常见键：`loc`（错误字段位置）、`type`（机器可读错误码）、`msg`（给人看的描述）、`input`（导致错误的原始输入）、可选 `ctx`（约束上下文）。`Field(gt=0)` 遇到 -20 的错误码为 `greater_than`，字段位置为 `('price',)`。接下来练习从错误列表中提取字段和错误码，之后映射 FastAPI 请求校验及 LangChain Structured Output。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-3-attempt-4:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-4-attempt-1:start -->
## L2-CHECK-4 / attempt 1
状态：needs_review，部分正确。用户识别 price=-20 违反 Field(gt=0)，但误认为 currency 不写 required=True 即可省略，只预测一项错误。Pydantic v2 中没有提供默认值的字段就是 required，故此输入会产生两条错误：`('price',) greater_than` 与 `('currency',) missing`。

补充规则：
```python
class Product(BaseModel):
    price: int = Field(gt=0)
    currency: str               # required

class ProductWithDefault(BaseModel):
    price: int = Field(gt=0)
    currency: str = "CNY"       # not required, default CNY
```

与可空注解区分：`currency: str | None` 仍 required，只是值可以为 None；`currency: str | None = None` 才是可不传。下一步进行同一核心规则的 targeted retest，之后推进 errors() 与 FastAPI。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-4-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-4-attempt-2:start -->
## L2-CHECK-4 / attempt 2
状态：passed。用户正确回答 ProductA 因 currency 无默认值而必填，缺失字段产生 ValidationError；ProductB 有默认值 currency="CNY"，输入仅 price=199 也能校验成功。

## 2.5 FastAPI 请求体验证
Pydantic BaseModel 可声明 FastAPI 请求体 Schema。FastAPI 在运行 endpoint 主体前验证请求；字段不合格时默认返回 HTTP 422，并附带错误详情。
示例：ProductIn 的 price 定义为 Field(gt=0)，currency 定义为默认 "CNY"。POST /products 请求 {"price": -20} 会在请求体校验阶段失败，不会执行 endpoint 函数体。
下一步 L2-CHECK-5：判断 HTTP 返回码及函数是否执行。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-4-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-5-attempt-1:start -->
## L2-CHECK-5 / attempt 1
状态：passed（局部知识检查）。用户正确判断客户端 POST JSON {"price": -20} 不会执行 FastAPI create_product() 函数体；因为 price 的 Field(gt=0) 校验失败，FastAPI 默认返回 HTTP 422。currency 提供默认值，不属于缺失错误。理解了请求体验证在 endpoint 主体之前发生。

## 2.6 LangChain Structured Output：原理与框架映射

最小原理：模型原始输出文本 → json.loads 解析 JSON → Product.model_validate 校验 Schema → 业务侧使用 Product 实例。任一步都可能失败，错误应被捕获/分类，不能假定模型输出永远符合业务。

框架对应：对支持该功能的已配置聊天模型使用 model.with_structured_output(Product)，再调用 structured_model.invoke(用户任务文本)。成功时结果是经过解析/校验的 Product 实例。具体机制取决于 provider 与方法，可能是原生 JSON Schema 约束或 tool calling。当前官方 LangChain Models 文档确认 Pydantic schema 的 with_structured_output 用法。

Agent 对应：LangChain create_agent(response_format=Product) 可将结构化结果保存在 state["structured_response"]；provider-native 与 tool-calling 两种策略需结合模型能力选择。Schema 验证通过不代表抽取内容一定事实正确。

下一步 L2-CHECK-6：检查 with_structured_output(Product) 在成功返回时结果对象类型，并比较手动 JSON 解析与框架封装的数据流。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-5-attempt-1:end -->
