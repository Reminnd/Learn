<!-- learn-agent:evidence:stage01-ch03-chapter-start-20261011:start -->
# Chapter 03：Tool基础与LangChain @tool

```yaml
schema_version: 2
stage_id: stage-01
chapter_id: 03-tool-basics
lifecycle_status: active
learning_status: learning
last_updated: 2026-10-11
```

## 3.1 真实问题：LLM怎样读取业务系统中的最新库存？

商品调研Agent接到“键盘KB-001现在有多少库存”的自然语言问题。LLM无法仅凭文字回答可靠地知道当前系统里的实时库存。应通过业务函数查询当前数据，再把查询结果作为上下文交给LLM总结，而不是让模型猜数字。

最小原理版（纯Python，无LLM、无第三方依赖）：

```python
inventory = {"KB-001": 12, "MS-002": 0}

def get_stock(sku: str) -> int:
    """根据SKU读取当前库存数量。"""
    if sku not in inventory:
        raise ValueError("未知SKU")
    return inventory[sku]

print(get_stock("KB-001"))  # 12
```

## 3.2 Tool四部分及调用边界

- name = get_stock：可调用工具的标识。
- description = 根据SKU查询商品库存：帮助模型判断何时选用。
- parameters = sku（字符串）：要求模型提供哪个SKU。
- handler = get_stock函数：由Python执行真实查询、验证业务输入并返回结果。

典型Agent运行流：用户提问 → LLM按工具描述选择get_stock并给出sku参数 → Agent运行时解析工具调用 → 运行时执行get_stock("KB-001") → 工具返回12 → 模型可基于查询结果回答。

模型提出tool call的指令不等于Python函数已执行；只有运行时真正执行handler才得到可靠业务数据。后续先用纯Python手写最小调度，再映射langchain_core.tools.tool（@tool）与tool binding，研究参数错误、description误选工具和ToolMessage过大。不要将本章先绑定长期项目；商品场景只是局部可运行教学例子。

本章当前进度：新章开始；正式EX1及Q1/Q2/Q3均未验收。
下一题L3-CHECK-1 / attempt 1：LLM返回一条get_stock的tool call，但应用没有执行handler，能否获得真实库存？为什么？
<!-- learn-agent:evidence:stage01-ch03-chapter-start-20261011:end -->
