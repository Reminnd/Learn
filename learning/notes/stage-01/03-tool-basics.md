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

<!-- learn-agent:evidence:stage01-ch03-checks1-2-batch-20261011:start -->
## L3-CHECK-1 / attempt 1
状态：passed。学员回答“没有，因为只是生成了请求但还未调用函数”，正确区分LLM提出Tool Call与运行时实际执行handler。

## L3-CHECK-2 / attempt 1
状态：needs_review。学员写result=handler(args)，直接将整份args字典当作一个位置参数传给sku；对应get_stock中inventory[sku]因字典不可哈希而抛TypeError。应使用handler(**args)，相当于get_stock(sku="KB-001")。

## L3-CHECK-2 / attempt 2
状态：passed（概念复检，类型术语已补充）。学员回答“关键字参数，'KB-001'”，正确识别使用**args后的关键字传参方式和实参值；但对“Python数据类型”未明确说str，教师补充sku实际类型为str。这个操作相当于get_stock(sku="KB-001")，输出库存12。

## 3.3 下一节：LangChain @tool
通过@tool将原生函数转换为可供模型注册的LangChain工具；docstring用作description，函数名作为name，签名注解可推断参数Schema；真正执行仍需要运行时调用tool.invoke({"sku":"KB-001"})，仅声明或bind_tools不执行。下一步L3-CHECK-3识别装饰器工具的name、description、parameters和handler。
<!-- learn-agent:evidence:stage01-ch03-checks1-2-batch-20261011:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECKS3-5-batch-20261011:start -->
## L3-CHECK-3 / attempt 1
状态：passed。用户正确判断@tool声明和包装get_stock工具本身不会执行库存查询，真正查询发生在get_stock.invoke({"sku":"KB-001"})时；说明已理解工具定义与handler执行的分离。

## L3-CHECK-4 / attempt 1
状态：passed。针对get_stock.invoke({})缺少必填sku的情况，用户正确判断LangChain根据参数Schema在进入handler之前校验失败，handler不会执行；异常属于Pydantic参数ValidationError，不是库存业务错误。

## L3-CHECK-5 / attempt 1
状态：passed（错误类型名称由教师补充）。面对get_stock.invoke({"sku":"KB-999"})，用户回答“能，会进入handler。但是找不到”，准确识别sku字符串字段满足Schema、工具逻辑会执行、库存字典中该键不存在；教师指出库存通过inventory[sku]直接索引时最终抛KeyError（而不是ValidationError）。

## 3.4 区分校验与业务错误
- 参数缺失（{}）→ 工具Schema校验失败 → handler不执行 → ValidationError。
- 参数格式正确但业务SKU不存在（{"sku":"KB-999"}）→ 校验通过→执行库存查询→Python KeyError。
- 正确SKU（{"sku":"KB-001"}）→ 返回整数12。

下一步L3-CHECK-6 / attempt1：为get_stock增加显式异常处理，捕获KeyError并返回有稳定字段的业务错误结果，而不是把Python traceback原样交给调用端。随后讨论LangChain ToolException、参数错误与可观测性，整章EX1和Q1/Q2/Q3尚未正式验收。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECKS3-5-batch-20261011:end -->
