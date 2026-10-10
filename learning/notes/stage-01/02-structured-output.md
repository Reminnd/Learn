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

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-6-attempt-1:start -->
## L2-CHECK-6 / attempt 1
状态：needs_review。用户回答“有ProductIn实例的AIMessage”，混淆原始AIMessage和Structured Output解析后的返回结果。

纠正：model.with_structured_output(ProductIn).invoke(...) 在调用成功、默认include_raw=False时直接返回ProductIn对象，可读取product.price。它不是外层AIMessage。只有显式设置include_raw=True时，结果才是包含raw、parsed、parsing_error的dict，其中raw是原始模型响应，parsed成功时是ProductIn实例。

后续复检：L2-CHECK-6 / attempt 2，比较result.price与result.content的可用性。参考LangChain官方BaseChatModel.with_structured_output文档。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-6-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-6-attempt-2:start -->
## L2-CHECK-6 / attempt 2
状态：passed。用户正确判断Pydantic结构化输出默认返回ProductIn实例，`product.price`可读出价格，而`product.content`在未定义该字段时抛出AttributeError。已区分原始AIMessage与解析后Pydantic返回值。

## 2.7 Structured Output失败模式
成功：`with_structured_output(ProductIn)`默认返回ProductIn；解析或Schema校验失败：默认`include_raw=False`时抛出解析相关异常。若设置`include_raw=True`，解析失败且模型请求本身成功时，返回的dict保留`raw`、`parsed=None`及非空的`parsing_error`，便于诊断。
边界：`include_raw=True`只捕获解析阶段错误；模型调用失败、网络超时等并不因此全部转成parsing_error。生产环境应限制重试次数，区分可恢复失败和不可恢复错误，避免日志记录敏感的原始响应。
参考：https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel/with_structured_output
下一步：L2-CHECK-7，预测解析失败时raw/parsed/parsing_error的表现。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-6-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-1:start -->
## L2-CHECK-7 / attempt 1
状态：needs_review（部分正确）。用户认识到 price="abc" 无法通过 Pydantic 校验，读取 price 仍会报错，但认为没有返回 parsed 键，并提议转而检查 raw 中的 price。正确情况：在 include_raw=True 且模型调用成功、解析失败时，返回字典仍含 parsed 键且值是 None，parsing_error 含错误信息，raw 保存原始（未校验）模型响应。

执行 `result["parsed"].price` 因 `None` 无 `price` 属性而抛出 `AttributeError`。不能绕开校验直接用 raw 中的无效数值做业务运算。安全路径是 `if result["parsed"] is not None: ...`，否则检查 parsing_error 并返回可控错误或按策略有限重试。

下一步 L2-CHECK-7 / attempt 2：复检正确的成功判定字段及错误处理，不提前标记该知识点掌握。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-1:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-2:start -->
## L2-CHECK-7 / attempt 2
状态：部分正确，需复检。用户正确选择方案B检查parsed是否为None，以避免对None访问.price造成AttributeError，但仅以“关于None的错误抛出”解释安全性，尚未说明raw存在不代表通过Schema验证，因此继续追问为何未经验证的raw不可做业务价格数据。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-3:start -->
## L2-CHECK-7 / attempt 3
状态：needs_review，部分正确。用户指出price="abc"是字符串，不具备数值价格的业务类型，传入数值计算可能抛出异常；但错误地认为这种数据“无法进入后续应用，仍旧会抛出异常”。真实系统若绕过Schema校验，原始字符串也可能被函数、数据库、日志或其他处理流程接收，甚至不报错但产生错误结果，例如"199"*2=="199199"。

本节核心边界：raw只是原始模型响应，不能凭raw非空判断抽取成功。应检查parsed是否非None，并在失败时使用parsing_error做错误分类；不得把未经验证的raw直接作为可信业务价格。下一步L2-CHECK-7 attempt 4检验无异常但发生数据污染的边界，随后继续可靠性工程与有限重试。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-3:end -->
