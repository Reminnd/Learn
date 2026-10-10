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

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-4:start -->
## L2-CHECK-7 / attempt 4
状态：部分正确，needs_review。用户正确预测 `products.append({"price": "abc"})` 不会抛出异常，并指出 "abc" 不适合数值计算，但未解释不报错的直接原因是示例仅执行字典构造与列表 `append()`，没有类型验证或算术运算。

正确的执行路径：`raw_price="abc"` → 创建保存原值的字典 → `products.append(...)` 接受字典并追加 → 输出“保存成功”。正常执行不能证明价格业务有效。错误原始价格可以在 Python 容器或接受字符串的存储中静默保留；进入数值运算时可能报错，也可能在某些操作下产生不符合业务含义的结果。

下一步 L2-CHECK-7 / attempt 5：只复检为什么 append 阶段不报错、以及需要在哪个边界执行 Pydantic 校验。保持章节 learning，不提前宣布 mastered。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-4:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-6-teaching-gap:start -->
## L2-CHECK-7 / attempt 6
状态：not_assessed。用户指出没有专门学过 model_validate 方法名，之前只是在示例里出现；本题不按错误答案计算。已明确补教：ProductIn.model_validate(raw) 返回校验成功的实例，失败抛出 ValidationError。只有校验成功才把 product append 到 products。
下一步复检 try/except/else 的执行结果。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-6-teaching-gap:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-7:start -->
## L2-CHECK-7 / attempt 7
状态：部分正确。用户确认 raw 中的 price="abc" 无法满足 ProductIn 的整数校验，model_validate 抛出 ValidationError 被 except 捕获，因此程序输出“校验失败”；未直接回答 products 是否新增，教学补充明确 products 仍为空，else 不执行。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-7:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-8:start -->
## L2-CHECK-7 / attempt 8
状态：passed。把 raw 改为 {"price": 199} 后，用户预测输出“保存成功”，并说明 products 包含 price=199、currency="CNY"，其中 currency 使用 Pydantic 默认值。结合前序用户指出 append 自身不进行校验的证据，已掌握“先 model_validate，成功后 append；失败时不保存原始数据”的边界。补充精确返回为 products=[ProductIn(price=199, currency="CNY")] 而不是装有 dict 的列表。

## 2.8 Structured Output Retry 最小原理
实际 Agent 的失败输出可能通过重新调用模型修复，但应该区分模型生成输出无效和固定用户输入非法。有限重试采用固定最多次数，每次新响应都需要独立执行 Schema 校验；验证通过才交给业务逻辑。
- 瞬时网络故障与限流：可以按策略限次重试并退避；
- 模型可修复的 JSON/Schema 错误：可以向模型反馈错误并请求修复；
- 固定无效输入或业务规则冲突：不能无限重试，应返回明确错误/请求用户修正；
- Schema 通过不证明事实正确。
LangChain Runnable.with_retry 会在指定异常类型抛出时重试，有 stop_after_attempt 和 retry_if_exception_type 等参数。若 include_raw=True 仅在结果中返回 parsed=None 而没有抛出异常，普通 with_retry 不会因此自动重试，业务层需显式判断或转换为可恢复错误。
下一步 L2-CHECK-8：读懂有限重试及 break 的分支流程。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-7-attempt-8:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-8-attempts-1-2:start -->
## L2-CHECK-8 重试控制流
- attempt 1: needs_review。正确推断两次尝试及先失败、再成功的输出，但将尝试次数误当保存元素数量，回答2个。
- attempt 2: passed。给出三项候选raw（abc，199，299）时，用户正确判断最终列表只有1个ProductIn，原因是第二次校验成功后执行break，第三项不再被处理；第一项异常触发continue，未执行append。

## 2.9 有界重试与失败分类
控制最大尝试次数，成功后立即停止；每次只让已通过Schema校验的输出进入业务。可恢复的网络或模型格式错误可以按策略重试；固定输入违反业务要求应直接返回校验错误，不应盲目无限重试。LangChain Runnable.with_retry 只在对应Runnable抛出异常时重试，并支持retry_if_exception_type、stop_after_attempt。尽量只对模型/易失败步骤加重试，避免把保存等副作用操作重复执行。
下一步 L2-CHECK-9：判断一次请求遇到HTTP 503和固定无效业务输入，哪些应该重试。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-8-attempts-1-2:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-9-attempt-2:start -->
## L2-CHECK-9 / attempt 2
状态：passed。用户正确区分HTTP 503可能由于临时服务不可用，有限重试后有可能恢复；固定不变的price=-20与Field(gt=0)业务约束冲突，重新校验相同输入不会改变失败结果，应向调用者返回校验错误并要求修正。精确边界：503不保证重试成功；price=-20仅在输入及约束均不变时属于确定性失败。

## 2.10 Backoff（退避）
在第1次请求失败后，下一次重试不应总是立即发生。Exponential Backoff（指数退避）使等待时间随重试次数增长，例如第1次失败等1秒、第2次失败等2秒、第3次失败等4秒；达到最大尝试次数就停止。可加入Jitter（随机抖动），避免很多客户端同一时刻一起重新请求。真实系统需要重试次数上限、时间上限与可重试错误分类；若响应给出合理的Retry-After，应考虑遵循服务端要求。
最小理解检查 L2-CHECK-10：最多调用3次，每次均返回503，等待间隔按1秒、2秒计算。确认调用次数、等待次数和是否继续第4次。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-9-attempt-2:end -->

<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-10-attempt-1:start -->
## L2-CHECK-10 / attempt 1
状态：passed。用户正确判断最多3次请求、累计等待3秒（1秒+2秒），第3次仍失败则不重试。补充：实际等待为2次而不是3次，因为重试上限包含首次尝试，达到上限后不需要再等待。

## 2.11 Idempotency（幂等性）初步
对会产生副作用的操作（如创建订单、扣款、写入数据）重试，可能出现“操作已成功但响应在网络中丢失”的不确定结果。幂等性要求相同操作的重复请求不会重复产生预期之外的业务效果，例如相同idempotency key只创建一个订单。示例思路为在持久化层按业务唯一请求ID做唯一性约束，并用原子事务检查已处理操作；仅用Python内存dict判断只适合本地演示，不足以应对并发、多实例或进程重启。对外部收费Tool尤其不能机械重试整个Agent Loop。
下一步：L2-CHECK-11 用订单Tool操作成功但响应超时的场景说明没有幂等保障时重复执行的风险。
<!-- learn-agent:evidence:stage-01-ch02-L2-CHECK-10-attempt-1:end -->

<!-- learn-agent:evidence:stage01-ch02-idempotency-checks11-12-batch:start -->
## L2-CHECK-11 / attempt 1
状态：passed。用户正确解释订单创建已成功但响应网络超时，Agent误以为失败而重试；若缺少幂等保护，最多3次尝试均实际成功可能生成3笔订单，即额外重复2笔。已区分请求超时和业务操作未执行的不同语义。

## L2-CHECK-12 / attempt 1
状态：passed。使用内存 orders 字典演示时，同一 request_id=req_001 重复调用返回已有订单，request_id=req_002 是新独立请求，因此三次调用只创建两笔订单。不同业务意图可创建相同商品的新订单，幂等键不能仅凭产品名推断。

## 2.11.2 并发请求下的幂等性
只用 if request_id in orders 的检查再创建订单，无法保证多个工作线程、进程或服务实例同时执行时的原子性。两个请求可能同时读到键不存在，并各自创建新订单。企业常通过数据库唯一约束和事务处理冲突；同时将请求参数摘要关联同一幂等键，防止不同请求内容误共用键。检查和写入应由可靠存储协调。
下一题 L2-CHECK-13：两个并发请求在检查幂等键时都观察到“不存在”，有什么风险？
<!-- learn-agent:evidence:stage01-ch02-idempotency-checks11-12-batch:end -->
