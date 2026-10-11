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

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-1:start -->
## L2-CHECK-13 / attempt 1
状态：needs_review，部分理解。学习者回答“因为消息列表中两个不处于先后关系？”，有意识到并发时不同请求可能没有固定串行顺序，但混淆了 Agent 的 Message List 与两个并发 HTTP/Tool 请求的执行调度。

纠正：竞态条件与 Message List 无关。请求A内部“检查后创建”有自身顺序，请求B也一样；两个请求之间的步骤可能交错，发生 A检查 → B检查 → A创建 → B创建。两个请求在任何一个创建动作完成前都读取到幂等键不存在，因此均继续尝试创建，导致重复业务副作用。check-then-act不是单一原子操作；需要数据库唯一约束、事务或等价协调，而非只依靠Python字典的先检查再写。

下一步：L2-CHECK-13 / attempt 2，针对“先A检查、再B检查、之后才创建”的时间顺序复检，解释为何两个请求可能都执行创建。此局部检查通过不等于章节mastered。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-1:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-2:start -->
## L2-CHECK-13 / attempt 2
状态：needs_review，局部正确。用户知道A之前检查req_001不存在，但断言“检查和创建在同一函数里实现，属于同一原子操作”，这是新的核心误解。

纠正：函数调用的代码可以包含多条独立操作；在并发线程、多个进程或服务实例环境中，一个请求执行完检查到开始创建之间，另一个请求可以检查并完成创建。可能的时间线为A检查不存在→B检查不存在→B创建→A基于原先结果创建；A并不会因为B创建而自动重新做检查。函数封装本身不提供原子性，简单dict最终只有一个key也不能证明外部订单创建/扣款等副作用没有执行两次。

需要数据库唯一约束与事务等协调来实现适合场景的幂等保障，不能仅靠把检查和创建写进同一个Python函数。

下一步：L2-CHECK-13 / attempt 3，明确复检A检查之后、A创建之前，B是否可以完成创建；判断原始检查是否自动刷新。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-2:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-3-guided-explanation:start -->
## L2-CHECK-13 / attempt 3：并发执行原理补教
状态：needs_review / 引导讲解。用户直接询问“为什么？我不太清楚了”，说明目前未掌握函数内部的检查/创建并发原子性；不以用户提问本身推断其已通过复检。

解释：相同函数的两次调用属于两次独立的执行。不同线程/进程或FastAPI worker可以在时间上交错处理；同一个函数只表示代码相同，不代表串行或原子性。共享数据库示例中，A读到req_001不存在之后可能被调度暂停；B也读到不存在并创建；A随后从if判断之后的位置继续，会依旧尝试执行insert，if不会自动重新检查。简单Python内存字典不等于跨进程可靠共享存储，演示应以共享数据库为背景。数据库唯一约束、合适的事务处理或等价机制才能对重复订单作有保障的协调。

下一步：L2-CHECK-13 / attempt 4，缩小为单一问题：A在if条件已判真、B插入后恢复执行时，A会自动重新判断还是直接继续执行insert？确认数据流后再讨论数据库唯一性约束。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-3-guided-explanation:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-4:start -->
## L2-CHECK-13 / attempt 4
状态：passed（记录更正）。用户实际回答“直接继续执行”，正确认识到if不会自动重判；旧记录将正确答案错记为“自动重新执行”。

纠正：Python的if条件只在控制流运行到该判断语句时求值；当条件为真进入if分支后，程序执行分支中下一条语句，中间状态即使变化也不会自动跳回if重新检查。在请求A检查订单不存在之后，B可能创建，A恢复时会按既有控制流继续尝试insert；若数据库设置唯一约束，重复insert可能失败，但这不是if自动重查。

针对性简化：不用并发，先执行flag=False；if not flag: 将flag=True，随后print("entered")仍会执行。只有循环返回判断点或显式重新检查时才会重新评估条件。

下一步L2-CHECK-13 attempt 5：仅考查if内部变量发生变化后，本轮分支是否继续执行，之后再映射回数据库唯一约束。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-4:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-14-attempt1-mysql-unique:start -->
## L2-CHECK-14 / attempt 1
状态：passed。用户正确预测：MySQL InnoDB表中设置UNIQUE(request_id)后，如果已有已提交订单req_001，后续重复INSERT会被唯一约束阻止并返回错误；数据库不会自动将历史订单作为应用层结果返回。

## 2.11.3 MySQL + SQLAlchemy错误处理（局部教学）
在Python企业服务中，SQLAlchemy的IntegrityError负责表示底层DBAPI的完整性约束异常。session.add(order)将ORM对象加入Session；session.commit()期间可能执行INSERT，遇到重复键可能抛IntegrityError。捕获后需要session.rollback()以恢复Session状态，再使用select(Order).where(Order.request_id == ...)查询历史订单，并比对原请求商品参数。同request_id不同商品不应静默复用旧订单。若遇到其他完整性错误，不能未经分类便统一当作幂等命中。
即使唯一约束防止数据库重复记录，也不等于外部扣款、发送消息等非数据库副作用自动幂等。生产方案还需合适事务、错误分类和外部副作用防护。
下一题：L2-CHECK-15，SQLAlchemy Session提交时触发IntegrityError后，为什么在同一Session继续查询前需要rollback。
提醒：仓库中L2-CHECK-13 attempt 5（if条件重判误区）仍未通过，本次MySQL学习不会自动消除该薄弱点，后续需要复检。
参考：https://docs.sqlalchemy.org/en/20/orm/session_basics.html；https://docs.sqlalchemy.org/en/20/core/exceptions.html
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-14-attempt1-mysql-unique:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-15-attempts1-3:start -->
## L2-CHECK-15 事务复检
- attempt 1: partial。用户正确指出IntegrityError后rollback使Session恢复可用；需要补充事务内未提交修改撤销的概念。
- attempt 2: partial。正确判断同一事务中尚未提交的库存减少会被rollback撤销，但未说明原因。
- attempt 3: passed。正确回答事务B rollback不会撤销事务A已经commit的库存，并明确理由是不能回滚其他已提交事务。

事务边界总结：未提交的库存修改和创建订单若在同一事务内，失败回滚可以撤销两者；事务A已提交的库存变更，不受事务B rollback影响。SQLAlchemy在失败后需rollback才能继续使用原Session。仓库旧的L2-CHECK-13 attempt 4实际回答是“直接继续执行”，已做记录更正；后续用单线程if简单复检。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-15-attempts1-3:end -->

<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-5:start -->
## L2-CHECK-13 / attempt 5
状态：passed（局部复检）。用户对以下Python程序正确预测输出“创建订单”：
```python
exists = False
if not exists:
    exists = True
    print("创建订单")
```
此前在并发A/B执行问题中已正确回答“A直接继续执行”。结合两项证据，说明用户能够正确追踪if条件只在执行到时判断，进入分支之后变量变化不会自动重新判断。这仍不等于用户独立实现了数据库并发幂等，后续Stage 01 Tool工程章节可继续巩固。

## Chapter 02正式验收准备：EX1
按照curriculum/stage-01/02-structured-output.md，必做EX1要求：最小原理版解析并验证LLM结构化输出；使用LangChain框架表达同一能力；能复现Schema验证失败并解释处理方案。此前小节练习虽已掌握若干概念，但还不是独立完成EX1。接下来使用商品价格案例，以Pydantic BaseModel构建Schema，逐步实现原理版与框架版，随后正式Q1/Q2/Q3。
下一步：EX1第1步，定义Product Schema，并验证 raw={"price":"199"} 或 raw={"price":"abc"}。
<!-- learn-agent:evidence:stage01-ch02-L2-CHECK-13-attempt-5:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-step1-attempt1:start -->
## Chapter 02 EX1 Step 1 / attempt 1
状态：passed（练习步骤，非完整EX1验收）。用户独立填写 `data = json.loads(raw_text)` 与 `product = Product.model_validate(data)`，正确映射JSON文本解析与Pydantic对象校验。示例输入为raw_text='{"price": "199"}'，Product定义price:int=Field(gt=0)与currency:str="CNY"。
<!-- learn-agent:evidence:stage01-ch02-EX1-step1-attempt1:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-step2-attempt1:start -->
## Chapter 02 EX1 Step 2 / attempt 1
状态：needs_review（局部语法错误，未完成该步骤）。用户正确调用`Product.model_validate(data)`，并在try中打印成功提示，except中计划打印失败提示与`e.errors()`。但把导入的`ValidationError`误写成`Validationerror`（小写e）。Python区分大小写；当model_validate因为price="abc"抛出ValidationError时，except类型表达式的错误名字将产生NameError，因此未按预期进入处理器。修复是`except ValidationError as e:`，后续只需针对性复检程序控制流与错误输出，不重复已经通过的Step 1。完整EX1仍需框架版实现、失败分析与验收。
<!-- learn-agent:evidence:stage01-ch02-EX1-step2-attempt1:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-step2-attempt2:start -->
## Chapter 02 EX1 Step 2 / attempt 2
状态：needs_review（部分正确）。本轮在明确已将异常处理器类型修正为ValidationError的前提下，用户正确预测price="abc"不能通过Pydantic的int校验，将输出“校验失败”。但用户回答`print(e.errors())`返回字典；真实Pydantic v2中`ValidationError.errors()`返回`list[dict]`（列表，每项错误信息是字典），即使只有一条错误，也仍在列表中。校验失败时其典型元素包含type="int_parsing"、loc=("price",)、msg和input="abc"。需复检容器类型后再进入LangChain框架版，EX1目前尚未完整验收通过。
下一题EX1 Step 2 / attempt 3：预测`type(e.errors()).__name__`与`type(e.errors()[0]).__name__`的输出，确认列表与内部字典的区别。
<!-- learn-agent:evidence:stage01-ch02-EX1-step2-attempt2:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-step2-attempt3:start -->
## Chapter 02 EX1 Step 2 / attempt 3
状态：passed（局部理解复检）。用户按顺序回答“列表，字典”，正确理解`type(e.errors()).__name__`输出`list`、`type(e.errors()[0]).__name__`输出`dict`；Pydantic ValidationError.errors()整体为list[dict]。说明解析错误信息结构的先前误区已解决。此前Step2的ValidationError大小写曾有拼写错误，整体验收之前仍应运行完整的异常处理代码；单个知识检查不等于EX1已完成。

## Chapter 02 EX1 Step 3：LangChain Structured Output框架实现
原理版流程：LLM文本 → JSON语法解析 → Pydantic校验 → Product实例。
框架版：先使用支持结构化输出的ChatModel执行`model.with_structured_output(Product)`得到Runnable，再执行`structured_model.invoke(prompt)`；成功且include_raw=False时返回经过Schema解析验证的Product实例。框架封装输出结构约束及解析校验过程，不应认为必然直接调用`json.loads()`，具体机制依赖模型服务的原生Schema能力或Tool Calling。若provider/模型不支持特定结构化输出方法，需要调整配置或换兼容模型。
本节练习：独立编写with_structured_output与invoke两行，再对比原理版输入、输出与失败处理。参考LangChain当前官方BaseChatModel.with_structured_output文档。
<!-- learn-agent:evidence:stage01-ch02-EX1-step2-attempt3:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-step3-attempt1:start -->
## EX1 Step 3 / attempt 1
状态：passed（局部框架代码检查）。用户独立正确填写：
```python
structured_model = model.with_structured_output(Product)
product = structured_model.invoke("这款键盘售价199元")
print(product.price)
```
框架映射：`with_structured_output(Product)`声明结构化结果Schema并返回可调用Runnable；真正执行模型调用的是`invoke(...)`。支持Pydantic Schema的兼容聊天模型在调用成功、默认`include_raw=False`时返回经过校验的Product实例。这里仍是假设model已配置成功且provider支持结构化输出，不是实际执行结果。

下一步EX1 Step 4：进行原理版的真实本地运行与失败用例验证，以及具备支持模型环境时的框架版运行。不能仅凭代码片段认定整个EX1 accepted/mastered。
参考：https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel/with_structured_output
<!-- learn-agent:evidence:stage01-ch02-EX1-step3-attempt1:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-step4-offline-principle-run-20261011:start -->
## Chapter 02 EX1 Step 4：原理版实际运行
状态：passed（原理版实际运行）。学习者提交了在其Python环境运行原理版代码的完整标准输出：
```text
Case 1: PASS
{'price': 199, 'currency': 'CNY'}
Case 2: FAIL
list
int_parsing
```
Case1证明输入JSON中的字符串"199"在Pydantic默认校验模式下可转为整数199，currency使用CNY默认值；Case2证明"abc"不满足int要求，捕获ValidationError后e.errors()返回list，错误type为int_parsing。Case2的FAIL是预期校验拒绝，而非代码执行失败。本次输出与前述测试代码吻合；输出由学习者提供，未远程执行学习者本机代码。

## Chapter 02 EX1 Step 5：无API框架输出解析验证
根据仓库environment/framework-baseline.md，Stage01依赖CPython3.11及langchain-core==1.6.2，没有Provider SDK或API Key。先通过LangChain PydanticOutputParser和RunnableLambda模拟模型生成的文本，验证Runnable组合与解析错误路径，不实际调用LLM。
最小路径：RunnableLambda模拟返回JSON文本 → PydanticOutputParser(pydantic_object=Product) → 成功返回Product实例；错误输入如price="abc"会抛出OutputParserException。此测试是“框架解析层离线验证”，不能替代真实提供商模型with_structured_output(Product)的调用测试。
参考LangChain官方参考：https://reference.langchain.com/python/langchain-core/output_parsers/pydantic/PydanticOutputParser 及 https://reference.langchain.com/python/langchain-core/runnables/base/RunnableLambda
下一步：学习者在其环境中运行EX1 Step 5离线Parser链，并提交完整stdout；随后对照with_structured_output的模型能力与实现路径，做EX1验收准备。
<!-- learn-agent:evidence:stage01-ch02-EX1-step4-offline-principle-run-20261011:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-step5-deepseek-api-route:start -->
## EX1 Step 5：DeepSeek实际API测试路线
用户明确表示已经申请DeepSeek API，允许使用真实API进行本章结构化输出测试，因此本次Step5不再要求先做离线RunnableLambda模拟。安全边界：API密钥只输入用户自己的Python进程或环境变量，不在聊天或仓库中存储；申请密钥并不证明账户已充值、调用已成功。

依据2026-10-11查询的DeepSeek官方文档，DeepSeek当前Chat Completions模型ID为deepseek-flash及deepseek-v4-pro。本次低成本练习采用deepseek-flash，明确禁用Thinking模式，并以LangChain ChatDeepSeek的with_structured_output(Product,method="function_calling",include_raw=True)检查raw、parsed、parsing_error。Python依赖langchain-deepseek；根据当前仓库environment/framework-baseline.md，原Stage01环境不含Provider SDK，因此本次属于可选真实API集成，不修改既有环境基线文件。

下一步：学习者在本机PyCharm/uv中安装langchain-deepseek，使用getpass或进程环境变量设置DEEPSEEK_API_KEY；运行真实模型调用，提交去敏的实际stdout/报错。尚未观察到真实API运行输出，EX1和Chapter02均不能标记mastered。
官方来源：https://api-docs.deepseek.com/quick_start/pricing/ 与 https://reference.langchain.com/python/langchain-deepseek/chat_models/ChatDeepSeek/with_structured_output。
<!-- learn-agent:evidence:stage01-ch02-EX1-step5-deepseek-api-route:end -->

<!-- learn-agent:evidence:stage01-ch02-EX1-step5-deepseek-live-api-passed:start -->
## EX1 Step 5 / DeepSeek API真实结构化输出成功
状态：passed（真实模型调用及输出校验）。此前学习者执行ChatDeepSeek实际请求时遇到HTTP 401 invalid API key，定位为认证配置问题（可能误带引号或已有无效环境变量）。指导重新输入密钥并去除首尾无意引号后，本轮用户提交实际运行成功的stdout：

```text
raw_type: AIMessage
parsed_type: Product
product: {'price': 199, 'currency': 'CNY'}
parsing_error: None
```

所用测试程序采用`ChatDeepSeek`、`with_structured_output(Product, method="function_calling", include_raw=True)`、`structured_model.invoke(...)`，Product的price为正整数、currency默认为CNY。结果展示模型响应`raw`是AIMessage、解析结果`parsed`为Product对象、`parsing_error=None`。据此确认真实API调用成功，结构化输出并通过Pydantic校验。此结果是单次成功，不代表模型未来不会输出错误；原理版的price="abc"校验失败已由EX1 Step4真实本地运行验证。不能把API认证401与Pydantic解析校验失败混为一谈。

原理版JSON解析+Pydantic正反例，以及框架版真实DeepSeek调用均有用户运行证据。接下来进入EX1解释与Chapter02正式Q&A：Q1自然语言解析为何不稳定及边界；Q2原理与LangChain的输入输出映射；Q3诊断Schema校验失败及方案Trade-off。待正式验收后方可判断Chapter02 mastered，当前仍learning。未记录任何真实API密钥。
<!-- learn-agent:evidence:stage01-ch02-EX1-step5-deepseek-live-api-passed:end -->

<!-- learn-agent:evidence:stage01-ch02-Q1-attempt1-20261011:start -->
## Chapter 02 Q1 / attempt 1：自然语言解析不稳定与Schema边界
状态：needs_review，核心因果链尚不完整。学习者回答大意是“结构化输出与Pydantic Schema能确保price字段数据结构正确；但price字段可能缺失、与其他数据混淆或LLM取错数据包”。这正确指出了Schema对数据结构的验证作用，以及字段缺失和语义性提取错误的可能性。尚未独立说出LLM普通自然语言输出的格式与措辞不稳定，会使固定字符串规则或位置解析失效。应纠正绝对化说法：Schema校验只能判断模型所给数据是否满足指定类型/范围/必需字段等约束，不能强制每次生成有效结构，也不能验证商品信息真实性。例如真实价格199而模型误提取299，price:int gt=0仍可能通过校验。

已给出以上解释。下一题Q1/attempt2仅检查普通自然语言文本格式变化导致固定解析方法不可靠的原因。答对后按Q1验收契约汇总评价，再进入Q2原理—框架映射。
<!-- learn-agent:evidence:stage01-ch02-Q1-attempt1-20261011:end -->

<!-- learn-agent:evidence:stage01-ch02-Q1-attempt2-20261011:start -->
## Chapter 02 Q1 / attempt 2
状态：needs_review。针对自然语言示例A“这款键盘售价199元”、B“价格：199元”、C“当前优惠价为¥199”，固定规则`text.split("价格：")[1]`为何不可靠，学习者回答“因为可能没有采用实际价格”。这一回答正确识别LLM可能给出错误的实际价格（语义性错误），但没有解释本题核心：同样的price在不同自然语言措辞里字段标记不稳定，文本A和C都缺少子串“价格：”，调用split只得到1个元素，读取[1]产生IndexError；文本B可分割但提取结果仍是“199元”而不是int。

教学已明确区分“自由文本格式不稳定→固定解析策略脆弱”与“LLM价格语义提取错误→格式合法但数据不真实”；需要让学习者独立判断分隔符不匹配时`split`产生列表长度，才能判定关键Q1掌握。下一题Q1/attempt3仅对`len("售价：199元".split("价格："))`进行检查，并说出原因。不能标Q1 passed，也不能标Chapter 02 mastered。
<!-- learn-agent:evidence:stage01-ch02-Q1-attempt2-20261011:end -->
