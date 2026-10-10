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
