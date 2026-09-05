<!-- learn-agent:evidence:stage-01-ch02-section01-json-schema-boundary:start -->
# Structured Output：结构化输出 — 课程笔记

## Metadata

- stage_id: `stage-01`
- chapter_id: `02-structured-output`
- schema_version: `2`
- lifecycle_status: consolidated
- learning_status: mastered
- last_updated: 2026-08-21

## 1. 为什么需要结构化输出

自然语言适合人阅读，但下游程序需要稳定的字段名、类型、必填项和取值范围。模型即使返回看起来像 JSON 的文本，也可能带 Markdown 代码围栏、额外解释、字段改名、缺少字段或类型错误。

## 2. 两道校验边界

第一道是 JSON 语法解析：json.loads(raw_text) 只验证文本是否为合法 JSON，并返回 Python dict/list；失败通常是 JSONDecodeError。

第二道是 Schema（模式/结构契约）校验：检查字段是否存在、类型是否正确、值是否在允许范围内。合法 JSON 不等于合法业务数据。

## 3. Pydantic 最小模型

Pydantic 是 Python 的运行时数据校验库。BaseModel 用类声明数据结构；类型标注如 score: int 既帮助阅读，也参与运行时校验。Literal 表示只能从指定值中选择；Field 可声明范围与字段说明。

```python
import json
from typing import Literal
from pydantic import BaseModel, Field, ValidationError

class Review(BaseModel):
    summary: str
    sentiment: Literal["positive", "negative", "neutral"]
    score: int = Field(ge=1, le=5)

raw_text = '{"summary": "很好用", "sentiment": "positive", "score": 5}'

data = json.loads(raw_text)
review = Review.model_validate(data)
```

运行数据流：模型文本 → json.loads → Python dict → Review.model_validate → 已校验的 Review 对象。json.loads 成功后，Pydantic 仍可能因字段缺失、类型错误或范围错误抛出 ValidationError。

## 4. LangChain 映射

当前 LangChain ChatModel 可使用 model.with_structured_output(Review) 绑定 Pydantic Schema，再 invoke 得到已解析的 Review。不同供应商可能使用原生 JSON Schema、函数/工具调用或 JSON mode；具体能力依模型集成而异。

```python
structured_model = model.with_structured_output(Review)
review = structured_model.invoke("提取评论：很好用，5 分")
```

框架减少手写解析胶水，但 Schema 校验失败、重试、原始响应保留和版本兼容仍需 Harness 处理。需要同时保留原始 AIMessage 时，可按模型集成支持情况使用 include_raw=True。

## 5. 首节结论

1. 自然语言文本不是稳定的程序接口。
2. JSON 解析只保证语法，不保证业务 Schema。
3. Pydantic 把字段、类型和约束变成可执行契约。
4. LangChain Structured Output 将 Schema 绑定到模型调用，但失败治理仍属于 Harness。

## 6. Q&A

Q1 待回答：为什么 json.loads 成功仍不足以让下游程序安全使用数据？
<!-- learn-agent:evidence:stage-01-ch02-section01-json-schema-boundary:end -->

<!-- learn-agent:evidence:stage-01-ch02-Q1-attempt-1-and-validation-errors:start -->
## Q1 attempt 1 与校验失败处理

Q1 通过：json.loads 成功只说明 JSON 语法可解析，不说明字段类型匹配或数据内容满足下游业务标准。补充失败边界包括必填字段缺失、枚举值未知、数值越界和字段版本不兼容。

### Pydantic 默认转换与严格模式

Pydantic 默认会尝试把可转换输入规范化，例如 score="5" 可能得到整数 5。优点是兼容常见脏数据；代价是可能掩盖上游格式漂移。需要拒绝隐式转换时，可调用 Review.model_validate(data, strict=True)，或在模型配置中启用 strict。

```python
from pydantic import ValidationError

try:
    review = Review.model_validate(data, strict=True)
except ValidationError as exc:
    for error in exc.errors():
        print(error["loc"], error["type"], error["msg"])
```

ValidationError 的错误项可提供 loc（错误位置）、type（错误类型）、msg（说明）和 input（问题输入）等信息。Harness 不应只记录“解析失败”，还应记录 Schema 版本、字段位置、错误类型、模型/供应商和重试次数，同时避免把敏感原始数据完整写入日志。

### 手写版与 LangChain 映射

手写链：模型调用 → AIMessage.content 字符串 → json.loads → dict → Review.model_validate → Review 对象。

框架链：model.with_structured_output(Review) 得到 structured_model；structured_model.invoke(input) 封装模型调用、结构化生成/解析与 Pydantic 校验，正常输出 Review 对象。include_raw=True 时可同时得到 raw AIMessage、parsed 对象和 parsing_error，便于可观测性与降级处理。具体结构化方法可能是供应商原生 JSON Schema、函数/工具调用或 JSON mode。

Q2 待回答：with_structured_output(Review) 对应手写链中的哪些步骤；调用时输入什么，正常输出什么？
<!-- learn-agent:evidence:stage-01-ch02-Q1-attempt-1-and-validation-errors:end -->

<!-- learn-agent:evidence:stage-01-ch02-session-summary-20260820:start -->
## 2026-08-20 学习小结

### 已掌握

- 生产级 Agent 不能只保存单一对话字符串；消息历史还需要容纳 Tool/MCP/Skill 的调用输入与输出，以及 token 消耗等调用元数据。
- Prompt 构造阶段得到 ChatPromptTemplate；运行时输入字典经 prompt 生成 ChatPromptValue，其内部包含格式化后的消息序列；ChatModel 正常返回 AIMessage。
- 消息历史可按关联程度选择滑动窗口、摘要压缩或归档检索，各自存在遗忘、摘要失真、额外 token 与存储/检索成本。
- json.loads 只验证 JSON 语法并产出 dict，不能保证字段类型、必填项、取值范围和业务规则满足下游 Schema。
- Pydantic model_validate 负责结构与业务约束校验；默认类型转换提高兼容性，strict=True 可避免隐式转换掩盖上游数据漂移。
- LangChain 的 model.with_structured_output(Review) 可封装结构化生成、解析和 Pydantic 校验；include_raw=True 可保留 raw、parsed 与 parsing_error。

### 当前薄弱点

- 仍需用自己的话完整说明 with_structured_output 对应手写链中的哪些步骤，以及 invoke 的输入和正常输出。
- 尚未完成 Pydantic strict 模式与 ValidationError 的代码练习。
- 后续间隔复习 ChatPromptTemplate（组件对象）与 ChatPromptValue（运行输出）的区别。

### 下次从这里继续

Q2：model.with_structured_output(Review) 对应手写方案中的哪些步骤？调用 structured_model.invoke(...) 时输入什么，正常输出什么？
<!-- learn-agent:evidence:stage-01-ch02-session-summary-20260820:end -->

<!-- learn-agent:evidence:stage-01-ch02-Q2-attempt-1-output-contract:start -->
## Q2 attempt 1：Structured Output 输出契约

作答中正确识别了概念映射：AIMessage.content → JSON/结构化解析 → dict → Pydantic 校验 → Review 对象；也正确指出 invoke 的输入可以是用户文本或消息。需要校准的是：框架不一定真的逐字执行 AIMessage.content + json.loads，具体实现可能使用供应商原生 JSON Schema、函数调用或 JSON mode，这里是能力层面的对应。

默认调用：

```python
structured_model = model.with_structured_output(Review)
result = structured_model.invoke(user_input)
# result 是 Review 对象
```

保留原始消息：

```python
structured_model = model.with_structured_output(Review, include_raw=True)
result = structured_model.invoke(user_input)
# result 是包含 raw、parsed、parsing_error 的字典
```

因此不能笼统地说 structured_model.invoke 总是同时输出 AIMessage 与结构化对象；输出契约取决于 include_raw。Q2 状态：待针对性复检。
<!-- learn-agent:evidence:stage-01-ch02-Q2-attempt-1-output-contract:end -->

<!-- learn-agent:evidence:stage-01-ch02-Q2-pass-and-schema-failure-triage:start -->
## Q2 复检通过与 Schema 失败排查

Q2 复检通过：默认 `model.with_structured_output(Review).invoke(input)` 返回 `Review` 对象；配置 `include_raw=True` 时返回字典，主要包含 `raw`、`parsed`、`parsing_error`。至此能够区分原理侧对象、框架侧对象、输入和两种输出契约。

### 三层失败定位

1. 模型调用层：超时、限流、鉴权或供应商错误，尚未取得可处理输出。
2. JSON/结构化解析层：输出不是合法结构，无法得到 dict 或结构化参数。
3. Schema 校验层：已经得到结构数据，但字段缺失、类型错误、枚举非法、数值越界或 Schema 版本不匹配。

### Pydantic `ValidationError` 与 `try/except`

`Review.model_validate(...)` 校验失败时会抛出 `ValidationError`。使用 `try/except` 把正常路径与失败路径分开：`try` 中只处理校验成功后的业务对象，`except ValidationError as exc` 中读取结构化错误并决定后续动作。不要用宽泛的 `except Exception` 把网络、程序 Bug 和 Schema 错误混在一起。

```python
from pydantic import ValidationError

try:
    review = Review.model_validate(data, strict=True)
except ValidationError as exc:
    for error in exc.errors():
        location = error["loc"]
        error_type = error["type"]
        message = error["msg"]
        print(location, error_type, message)
```

`exc.errors()` 返回错误项列表，而不是单个错误。一次校验可能同时发现多个字段问题，因此必须遍历全部错误；只读取第一项会丢失诊断信息。每个错误项常见字段：

- `loc`：错误位置，通常是元组，表达从根对象到失败值的路径。例如 `('author', 'email')` 表示嵌套对象 `author.email`，`('items', 2, 'score')` 表示列表 `items` 的第 3 项中的 `score`。可用于生成字段级提示、日志和前端错误映射。
- `type`：稳定、机器可判断的错误类别，例如 `missing`、`literal_error`、`int_type`、`less_than_equal`。程序分支应优先依据它，而不是匹配可能变化、可能本地化的自然语言消息。
- `msg`：给开发者阅读的错误说明，适合日志和调试，不适合作为主要程序分支条件。
- `input`：触发错误的原始输入片段；排障有用，但写日志前必须脱敏。

### 优先按 `error["type"]` 分类

```python
actions = []

for error in exc.errors():
    error_type = error["type"]

    if error_type == "missing":
        actions.append("retry_model")
    elif error_type in {"int_parsing", "string_pattern_mismatch"}:
        actions.append("repair_then_validate")
    elif error_type in {"literal_error", "less_than_equal"}:
        actions.append("fail_fast")
    else:
        actions.append("degrade_or_escalate")
```

这只是动作路由示意，真实策略还必须结合字段业务含义、数据能否无歧义恢复、风险等级和重试预算。同一种 `type` 在不同业务中可能对应不同动作；例如普通摘要字段缺失可以重试，支付金额字段缺失通常应严格失败。修复后必须再次执行完整 Schema 校验，不能绕过验证直接交给下游。

### 可执行排查顺序

先保留请求 ID、模型/供应商、Schema 名称与版本；再判断失败层；若为 Schema 失败，遍历 `errors()` 中的全部 `loc/type/msg/input`；随后优先按 `type` 将问题归为缺失、类型、范围、枚举或版本问题；最后才在重试、确定性修复、严格失败和降级输出之间选择。日志应对敏感 `input` 脱敏。

### 根据错误类型选择工程动作

- 重试模型：适合模型偶发漏字段、格式漂移，或需要重新理解自然语言才能补全的内容。将脱敏后的 `loc`、`type` 与约束反馈给重试提示，并设置次数上限；代价是更多 token、延迟和费用。确定性的 Schema 版本不兼容不应盲目重试。
- 确定性修复：只适合明确、无歧义、可重复的转换，例如裁剪空白、受控别名映射，或从已有结构化字段唯一推导。修复后重新校验；不能猜测缺失的业务事实，也不能用默认值掩盖上游质量问题。
- 严格失败：适合支付、权限、身份、合规等关键字段，以及枚举越界、约束冲突或未知版本。保护正确性，但需要清晰错误、监控告警和人工处理路径。
- 降级输出：适合非关键能力，可以返回部分结果、原始文本或明确的 fallback；必须携带降级状态，让下游知道数据未通过完整验证，绝不能伪装成正常的 `Review` 对象。

核心原则：业务内容缺失不能随意自动补；只有无歧义的格式问题才适合确定性修复。先分类错误，再选择动作，并记录为什么这样处理。
<!-- learn-agent:evidence:stage-01-ch02-Q2-pass-and-schema-failure-triage:end -->

<!-- learn-agent:evidence:stage-01-ch02-Q3-pass-and-ex1-start:start -->
## Q3 通过：Schema 错误分类与处理决策

作答能够遍历 `ValidationError.errors()`，按 `missing`、`literal_error`、`less_than_equal` 分类；能够通过复现和日志锁定缺失字段，回看输入，再决定是否重试；并明确重试会增加 token、延迟与费用。满足 Q3 的排查顺序与 Trade-off 验收要求。

```python
for error in exc.errors():
    if error["type"] == "missing":
        print("缺少字段")
    elif error["type"] == "literal_error":
        print("枚举非法")
    elif error["type"] == "less_than_equal":
        print("数值超过最大值")
```

### 从错误说明升级为机器动作

`decide_action()` 的返回值应是程序能够稳定判断的动作标识，而不是只给人阅读的提示文本。动作标识构成 Harness 内部的控制协议，例如：

- `retry_model`：重新请求模型生成。
- `repair_then_validate`：按确定性规则修复，然后重新执行 Schema 校验。
- `fail_fast`：立即失败，不猜测、不让未验证数据进入下游。

```python
def decide_action(error_type):
    if error_type == "missing":
        return "retry_model"
    elif error_type == "literal_error":
        return "fail_fast"
    elif error_type == "less_than_equal":
        return "repair_then_validate"
    return "fail_fast"
```

上面只是策略映射示例，不是所有业务的固定答案。同一种 Pydantic 错误在不同业务规则下可能对应不同动作。

### 开发者日志与程序控制流分层

`error["loc"]`、`error["type"]`、`error["msg"]` 等信息用于开发者日志、排障和可观测性；`action` 用于程序控制流。两者应同时保留，但职责不同：日志解释“哪里错、为什么错”，动作决定“程序下一步做什么”。

```python
action = decide_action(error["type"])

logger.warning(
    "schema validation failed",
    extra={
        "loc": error["loc"],
        "type": error["type"],
        "msg": error["msg"],
        "action": action,
    },
)

if action == "retry_model":
    data = call_model_again()
elif action == "repair_then_validate":
    data = repair_data(data)
elif action == "fail_fast":
    raise SchemaPolicyError(error)
```

日志中的原始输入或摘要必须按敏感级别脱敏，不能为了排障泄露隐私数据。

### `repair_then_validate` 的强制闭环

确定性修复不能绕过 Schema。正确流程必须是“确定性修复 → `Review.model_validate(..., strict=True)` 重新校验 → 通过后才进入下游”：

```python
if action == "repair_then_validate":
    repaired_data = repair_data(data)
    review = Review.model_validate(repaired_data, strict=True)
    send_to_downstream(review)
```

不能在手动修改字典后直接交给下游，因为修复代码本身也可能产生新错误，或只修复了多个错误中的一个。若重新校验仍失败，应再次进入错误分类与策略决策，而不是假装修复成功。

### 确定性修复的业务边界

只有存在明确、无歧义、可审计的业务规则时，才允许 `repair_then_validate`。例如业务契约明确规定“评分超过 5 时截断为 5”，才能执行 `score = min(score, 5)`。若没有该规则，`8` 可能表示模型误解了评分体系，擅自改成 `5` 会掩盖上游问题。

因此：

- 能从现有数据按唯一规则推导或规范化：`repair_then_validate`。
- 需要模型重新理解、抽取或补全：`retry_model`。
- 关键字段无法安全推断，或错误不允许容错：`fail_fast`。

### 完整处理数据流与状态机视角

```text
模型输出
  ↓
JSON / 结构化解析
  ↓
Review.model_validate(..., strict=True)
  ├─ 通过 → 已校验对象 → 下游
  └─ 失败 → ValidationError.errors()
               ↓
            错误分类
               ↓
            策略决策 decide_action()
               ├─ retry_model → 重新生成 → 回到解析与校验
               ├─ repair_then_validate → 确定性修复 → 严格重新校验
               └─ fail_fast → 终止并报告
```

这里已经不再是单个 `if/elif` 的错误提示，而是由“状态 + 事件 + 转移”组成的小型状态机：生成、解析、校验、分类、重试、修复、失败和成功都是状态或转移。后续当重试次数、降级路径、人工审核和可观测性增加时，可以进一步显式建模为状态机或 LangGraph 工作流。

### EX1 入口

下一步完成无 API Key 的最小代码练习：用 Pydantic 复现字段缺失、枚举非法和数值越界；输出结构化错误；实现返回 `retry_model`、`repair_then_validate`、`fail_fast` 的受控处理决策；验证修复后必须再次执行严格 Schema 校验；最后写出 `with_structured_output(Review)` 的框架映射。
<!-- learn-agent:evidence:stage-01-ch02-Q3-pass-and-ex1-start:end -->

<!-- learn-agent:evidence:stage-01-ch02-EX1-pass-and-mastery:start -->
## EX1 通过与 Chapter 02 掌握判定

### EX1 证据

提交代码使用 `json.loads` 区分自然语言输出与合法 JSON，使用 Pydantic `Review.model_validate(..., strict=True)` 复现并分类 `missing`、`literal_error` 和 `less_than_equal`，通过 `decide_action` 给出处理方向，并将手写链映射到 `model.with_structured_output(Review)`。还原聊天转义后的代码通过 `py_compile`；当前解释器因未安装 Pydantic 在导入阶段停止，这属于环境依赖，不是代码语法或练习逻辑失败。本章契约允许可运行代码或可执行伪代码，因此 EX1 三项 acceptance 全部通过。

映射表述校准：更精确地说，框架封装模型结构化生成、对 `AIMessage.content`/工具参数的结构化解析以及 Schema 校验，具体内部机制不保证总是字面执行 `json.loads`。

### 掌握评分（88/100）

- 概念理解：23/25。能区分 JSON 语法合法与业务 Schema 合法，并理解 Structured Output 的价值。
- 因果与数据流解释：18/20。能描述 Prompt/Model 输出链以及 JSON → dict → Pydantic 对象的数据流。
- 应用与框架映射：18/20。能映射手写解析到 `with_structured_output`，并区分默认输出与 `include_raw=True`。
- 调试与故障排查：17/20。能复现解析失败与三类 Schema 错误，按错误类型输出定位信息和处理策略。
- 迁移、边界与 Trade-off：12/15。能说明重试的 token、延迟、费用代价，并区分确定性修复与模型重试。

五个维度均达到 60% 下限；Q1、Q2 两道关键题最近有效作答通过；EX1 通过；未解决关键误解为 0；完整性为 healthy；章节验收契约合法。因此 `mastered=true`。
<!-- learn-agent:evidence:stage-01-ch02-EX1-pass-and-mastery:end -->

<!-- learn-agent:evidence:stage-01-ch02-validation-error-strict-dataflow-review:start -->
## 补充复习：`ValidationError`、严格模式与处理闭环

### 1. 用异常把校验结果分成两条路径

`Review.model_validate(data)` 校验失败时会抛出 Pydantic 的 `ValidationError`。`try/except ValidationError as exc` 的作用，是只捕获这一类 Schema 校验异常，并把成功路径与失败路径明确分开：

```python
from pydantic import ValidationError

try:
    review = Review.model_validate(data, strict=True)
except ValidationError as exc:
    for error in exc.errors():
        print(error["loc"], error["type"], error["msg"])
    # 记录日志，再按策略重试、修复或拒绝执行
else:
    # 只有校验成功的 Review 对象才能进入业务逻辑
    run_business_logic(review)
```

这里的 `exc` 是捕获到的异常对象。只捕获 `ValidationError`，可以避免把网络超时、程序 Bug 等其他异常误判成数据校验失败。

### 2. `exc.errors()` 是错误列表，一次校验可包含多个错误

`exc.errors()` 返回由多个错误字典组成的列表。Pydantic 会尽量收集一次校验中发现的所有问题，例如同一份数据可以同时缺少 `summary`、包含非法 `sentiment`，并且让 `score` 超出范围。因此必须遍历列表，不能假设一次只会有一个错误，也不应只处理第一项。

每个错误字典中的常用字段：

- `error["loc"]`：错误发生的位置或字段路径，通常是元组；嵌套对象和列表索引也会出现在路径中。它回答“哪里错了”。
- `error["type"]`：机器可判断的错误类别，例如 `missing`、`literal_error`、`int_type`、`less_than_equal`。程序做重试、修复或拒绝执行的分支判断时，应优先使用它。
- `error["msg"]`：供人阅读的错误说明，适合日志和调试；它可能随版本或语言变化，不适合作为稳定的程序分支条件。

错误项还可能包含 `input`。它有助于排障，但写日志前必须按数据敏感级别脱敏。

### 3. 默认类型转换与 `strict=True`

Pydantic 默认会对能够明确转换的值做类型转换，例如字段声明为 `int` 时，字符串 `"5"` 可能被转换成整数 `5` 后通过校验。这能提高系统对常见输入差异和脏数据的兼容性，但也可能掩盖上游本应输出数字却持续输出字符串的格式漂移。

`Review.model_validate(data, strict=True)` 会关闭这类隐式转换；声明为 `int` 的字段就必须收到真正的整数。工程上不是“严格永远更好”，而是按边界风险选择：

- 接口边界、支付、权限、合规和需要尽早暴露数据契约漂移的场景，优先严格校验。
- 低风险导入、历史数据兼容等场景可以允许受控转换，但应监控转换频率，避免兼容层长期掩盖上游问题。
- 如果需要修复，只允许执行明确、无歧义、可审计的转换；修复后必须再次完整校验。

### 4. 从模型输出到业务逻辑的完整数据流

```text
模型输出
  ↓
JSON / 结构化解析
  ↓
Pydantic Schema 校验
  ├─ 成功 → 已校验对象 → 进入业务逻辑
  └─ 失败 → ValidationError
               ↓
            exc.errors()：遍历全部 loc / type / msg
               ↓
            记录脱敏日志并按业务策略选择动作
               ├─ retry_model：带次数上限地重新生成，再次解析和校验
               ├─ repair_then_validate：确定性修复，再次完整校验
               └─ fail_fast：拒绝执行，阻止未验证数据进入下游
```

核心安全边界是：校验成功的模型对象才能进入业务逻辑；失败数据无论经过日志、重试还是修复，都不能绕过 Schema。一次失败可能包含多个字段错误，策略决策需要综合全部错误、字段的重要性、风险等级和重试预算。
<!-- learn-agent:evidence:stage-01-ch02-validation-error-strict-dataflow-review:end -->
