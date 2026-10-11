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

<!-- learn-agent:evidence:stage01-ch03-check6-check7-20261011:start -->
## L3-CHECK-6 / attempt1
状态：passed。用户独立答出except KeyError，而非ValidationError，因为传入sku为合法字符串后已经通过参数Schema校验，库存字典索引不存在的键属于handler业务执行错误。返回稳定的ok/error字典可让调用方区分业务失败。

## L3-CHECK-7 / attempt1
状态：needs_review（部分正确）。面对get_price(sku)和get_stock(sku)使用相同description“查询商品信息”，用户意识到LLM可能分辨不清或不必要重复调用，get_price改为“查询商品价格”正确；但将get_stock改为“查询商品详情”仍过于宽泛，无法让LLM区分库存数量与价格、品牌、规格信息。工具description应明确动作、目标及返回范围，例如按SKU查询当前库存数量；笼统description可能选错工具或额外调用，却不保证一定发生重复调用。
下一题L3-CHECK-7 attempt2：仅改写get_stock的docstring，让模型明确只查询库存数量，与get_price的价格职责无歧义。之后再进入真实DeepSeek bind_tools调用。
<!-- learn-agent:evidence:stage01-ch03-check6-check7-20261011:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-7-attempt2-passed:start -->
## L3-CHECK-7 / attempt 2
状态：passed。学员按要求将get_stock的docstring从“查询商品详情”修改为“查询商品库存数量”，清楚将库存查询与get_price的价格查询区别开来。注解sku:str已经表明参数；工程增强写法可明确“根据商品SKU查询当前库存数量，不查询价格”，但不是本次通过的必要条件。

## 3.6 真实DeepSeek bind_tools 测试（待运行）
依据DeepSeek官方Tool Calls文档及LangChain ChatDeepSeek.bind_tools参考：
- @tool包装普通Python handler并发布name/description/args schema；
- ChatDeepSeek(model="deepseek-flash", extra_body={"thinking":{"type":"disabled"}})可使用bind_tools([get_stock,get_price], tool_choice="auto")把工具说明提供给模型；
- 仅执行model_with_tools.invoke(prompt)时，响应是AIMessage，可观察response.tool_calls的工具名和参数；tool_choice="auto"不保证一定提出工具调用；
- 本步骤只观察模型工具选择，不调用get_stock.invoke或get_price.invoke，因此没有执行库存查询；下一步再编写手动运行时与ToolMessage回填闭环。
真实API使用用户本机DEEPSEEK_API_KEY，不在GitHub或笔记中记录密钥。用户尚未提交此步骤的API实际输出；不得假定工具选择成功。
参考：https://reference.langchain.com/python/langchain-deepseek/chat_models/ChatDeepSeek/bind_tools 及 https://api-docs.deepseek.com/guides/tool_calls/。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-7-attempt2-passed:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-8-live-deepseek-pass-20261011:start -->
## L3-CHECK-8：真实DeepSeek Tool Calling
状态：passed（API运行验证）。用户在之前配置的ChatDeepSeek上运行`model.bind_tools([get_stock,get_price],tool_choice="auto")`并调用`invoke()`，实际提交stdout：`response_type: AIMessage`；`response.tool_calls`包含且仅显示`get_stock`，参数`{"sku":"KB-001"}`，包含tool_call id和type=tool_call；`response.content`为空。这证实本次模型正确选择库存而非价格工具，且生成机器可读的工具调用指令。**程序尚未执行handler**，不能把tool_calls当作库存已经被查询。
下一步3.7手写Runtime：建立受控白名单dict`{"get_stock":get_stock,"get_price":get_price}`；读取`response.tool_calls[0]["name"]`和`["args"]`，查到LangChain工具并用`tool.invoke(call["args"])`执行；拿到库存12。之后使用LangChain ToolMessage(content=str(result),tool_call_id=call["id"])回传同一对话，模型再生成最终答复。Tool Call若为空、多个、参数错误或未知工具名需要以后验证；不允许由LLM工具名直接执行任意Python代码。
参考LangChain： https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-8-live-deepseek-pass-20261011:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-9-attempt1-20261011:start -->
## L3-CHECK-9 / attempt 1
状态：needs_review。问题是在真实DeepSeek API返回tool_calls后，`selected_tool=tools_by_name[call["name"]]`是经过@tool装饰的LangChain工具对象；学员填写`result=selected_tool(**call["args"])`。
正确理解：call["args"]得到可供执行的工具参数字典；但selected_tool不是普通Python函数而是LangChain StructuredTool，其公开执行接口是`selected_tool.invoke(call["args"])`，会先处理Schema再调用底层handler。把工具对象当成普通函数直接使用**kwargs在当前LangChain环境中通常触发TypeError。
回顾：此前原生函数`handler(**args)`是正确的，因为handler是可调用Python函数；本章被@tool包装的get_stock应使用`get_stock.invoke({"sku":"KB-001"})`。这与是否实际调用DeepSeek无关，后续不需要再次调用远程模型即可本地复检。基于当前用户本机库存字典，正确执行后结果为整数12。
下一题L3-CHECK-9 / attempt 2：在明确是@tool包装的LangChain工具时，问应把参数字典传入哪一个接口、实际返回什么；经复检通过再进ToolMessage工具结果关联。
官方参考：https://reference.langchain.com/python/langchain-core/tools/structured/StructuredTool
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-9-attempt1-20261011:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-9-attempt2-20261011:start -->
## L3-CHECK-9 / attempt 2
状态：needs_review。教师已明确selected_tool为@tool包装的StructuredTool，`call["args"]`是{"sku":"KB-001"}，要求补全`result=selected_tool.invoke(???)`并预测输出。学习者又填入`result=selected_tool.invoke(**call["args"])`，同时预测输出是包含库存数量的ToolMessage。
纠正：`BaseTool.invoke(input)`需要一个输入参数；`selected_tool.invoke(call["args"])`把args字典整体作为唯一input交给LangChain工具，执行本地handler成功时直接返回int 12。写`invoke(**call["args"])`相当于`invoke(sku="KB-001")`，不会自动为input参数提供字典。ToolMessage是工具结果与某条tool_call_id关联后用于模型上下文的消息；如`ToolMessage(content=str(result),tool_call_id=call["id"])`可以显式构造。额外边界：LangChain工具若收到完整的ToolCall字典（含name、args、id、type="tool_call"），`selected_tool.invoke(call)`可自动包装返回ToolMessage；这与`invoke(call["args"])`直接返回int是两种不同输入模式。
下一题L3-CHECK-9 / attempt3：仅填补`selected_tool.invoke(???)`，给定args字典，要求写出正确输入表达式和返回类型与值。回答通过后再进入ToolMessage闭环，不一次考多项。
官方文档：https://reference.langchain.com/python/langchain-core/tools/base/BaseTool 及 https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-9-attempt2-20261011:end -->
