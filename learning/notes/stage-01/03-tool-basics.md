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

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-9-attempt3-pass-20261011:start -->
## L3-CHECK-9 / attempt 3：Tool.invoke(args)的返回值
状态：passed（两项类型复检）。用户正确回答本地`result=get_stock.invoke({"sku":"KB-001"})`依次打印`int`和`12`，确认向经过@tool包装的LangChain工具传入args字典，能够得到handler的整数返回结果。用户主动追问为什么此前普通Python函数要用`handler(**args)`，此处却只需`invoke(args)`。解释：普通函数的签名形如get_stock(sku:str)，`**args`把{"sku":"KB-001"}展开成`sku="KB-001"`；LangChain工具的invoke(input)接收单个输入对象，故直接传入参数字典，再由框架进行Schema校验及调用handler。写`invoke(**args)`会把sku当作invoke关键字，无法提供应有的input参数。
结果类型的边界：`get_stock.invoke({"sku":"KB-001"})`直接返回int 12；随后显式`ToolMessage(content="12",tool_call_id=call["id"])`产生给模型回填的工具消息。若使用完整ToolCall结构作为invoke输入，框架也支持创建关联的ToolMessage；本次仅练习参数字典路径。
下一步3.8：工具调用结果与tool_call_id关联，手动生成ToolMessage并在消息列表中交给DeepSeek。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-9-attempt3-pass-20261011:end -->

<!-- learn-agent:evidence:stage01-ch03-toolmsg-a1-notes:start -->
L3-CHECK-10 attempt1: partial. Learned that ToolMessage must reuse call["id"], not a chosen number. Next: ID matching retest.
<!-- learn-agent:evidence:stage01-ch03-toolmsg-a1-notes:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK10a2a3-11-live-success:start -->
## L3-CHECK-10 / attempt 2
状态：needs_review。学生从call字典读取ID时写call[id]，未使用字符串键；Python id在该作用域对应内置函数，直接用该函数对象查字典会KeyError。应当写call["id"]。

## L3-CHECK-10 / attempt 3
状态：passed。学生独立正确写出print(call["id"])，能够取得模型生成的原始工具调用ID，随后在ToolMessage(content=str(result),tool_call_id=call["id"])复用。

## L3-CHECK-11 / attempt1：实际DeepSeek工具执行闭环
状态：passed（用户实际运行验证）。Python运行时执行模型选出的get_stock并在终端打印tool_result: 12（贴出的此行随后混入部分终端提示符）；ToolMessage以call["id"]关联工具结果；第二次DeepSeek模型调用成功生成最终回答：“SKU 为 **KB-001** 的键盘当前库存数量是 **12**。”
证实AIMessage(tool_calls)→Python本地handler执行→ToolMessage→DeepSeek最终回答的完整单工具往返。尚未证明可处理任意多个Tool Call；本次代码显式要求len(response.tool_calls)==1，否则抛RuntimeError。

## 3.10 下一练习：多个工具调用
模型若同时选择get_stock和get_price产生2条tool_calls，当前硬编码单次调用示例会先触发len != 1的RuntimeError，没有执行任何handler。生产Runtime应安全遍历全部调用、按允许列表匹配工具名、验证参数并逐条生成与原ID匹配的ToolMessage，最后整体回传模型。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK10a2a3-11-live-success:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK12-14-batch-20261012:start -->
## L3-CHECK-12 / attempt 1：多工具调用边界
状态：passed。模型若返回两条Tool Call，则len(response.tool_calls)!=1为True，代码会主动raise RuntimeError。若没有捕获该异常，之后的工具执行逻辑不会运行，因此两条工具调用都没有被执行。学员准确识别了程序异常与模型选择工具是不同阶段。

## L3-CHECK-13 / attempt 1：遍历所有Tool Call
状态：passed（书写细节已提示）。学员写for call in response.tool_calls并解释response.tool_calls[0]仅取第一个元素，不能遍历全部调用。教师提醒for语句需要末尾冒号。正确实现for call in response.tool_calls: 逐次按name选出白名单工具、用invoke(args)执行并按各自call["id"]创建ToolMessage。

## L3-CHECK-14 / attempt 1：独立ToolMessage回填
状态：passed。学员在append和extend之间正确选择extend。对messages=[HumanMessage(...),AIMessage(tool_calls)]使用messages.extend(tool_messages)可将每个ToolMessage对象依次加入平面消息序列，避免append(tool_messages)形成嵌套列表而无法直接当作LangChain消息序列处理。

## 3.12 下一工程练习：多工具查询的实际验证
在已经跑通的单Tool Call闭环上，将question扩展为同时查询KB-001的库存与价格。删除恰好一个调用的硬限制，按response.tool_calls逐条执行，并将对应的ToolMessage全部回传。应观察DeepSeek是否同一次返回两个Tool Call；如只返回一个，不能假定模型一定并行调用，应进一步学习多轮Agent Loop与安全退出控制。未知工具名应通过白名单检查，参数和业务异常后续独立处理。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK12-14-batch-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-15-real-two-tools-20261012:start -->
L3-CHECK-15: passed. DeepSeek chose get_stock and get_price in one response. Tool results 12 and 199 were returned; model answered KB-001 stock 12 and price CNY199. Next: tool error isolation.
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK-15-real-two-tools-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-check16-18-20261012:start -->
## L3-CHECK-16 to 18
- L3-CHECK-16 passed: when get_stock invokes unknown inventory SKU KB-999, handler raises KeyError; without exception handling, get_price never runs.
- L3-CHECK-17 passed: user correctly identified except KeyError as a way to catch the handler's missing SKU.
- L3-CHECK-18 attempt1 needs_review: user believed unknown tool name produces no KeyError because no corresponding tool exists. Correction: tools_by_name[call["name"]] immediately raises KeyError on a missing key; because this lookup is before try, the inner except KeyError cannot catch it. tools_by_name.get(...) instead returns None. Next: recheck missing-key handling and try boundaries.
<!-- learn-agent:evidence:stage01-ch03-L3-check16-18-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-check18a2-19a1-notes-20261012:start -->
## L3-CHECK-18 / attempt2：通过
用户正确回答tools_by_name.get("delete_product")返回None；随后if selected_tool is None打印UNKNOWN_TOOL。确认其已能区分dict.get与索引运算抛KeyError的差异。此前工具名不存在时是否抛异常的误区已复检。

## L3-CHECK-19 / attempt1：部分正确
给定多个tool_calls，若遇未知工具直接continue，不生成ToolMessage，用户正确指出delete_product没有对应结果；但错误预测DeepSeek“会不断发起重试”。需要指出：提交缺少结果消息的历史可能被API拒绝（例如400 tool_call_id未匹配），不是模型必然重新发起调用，更不会自动无限重试。规范做法是为每条Tool Call产出对应tool_call_id的ToolMessage，未知工具反馈简短错误消息（如content="UNKNOWN_TOOL",status="error"），继续其他工具。下一题让学员补全未知工具分支，复检ToolMessage关联ID和continue位置。
<!-- learn-agent:evidence:stage01-ch03-check18a2-19a1-notes-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK19a2-20-21-batch-20261012:start -->
L3-CHECK 19, 20, 21 passed. Correct ID mapping, ValidationError, and broad exception logging risks. Next: large ToolMessage.
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK19a2-20-21-batch-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK22-attempt1-20261012:start -->
L3-CHECK-22 attempt1: needs_review. Student correctly identifies context bloat and attention dilution from 5000 raw reviews; tentatively suggests batching or vector similarity. Batching alone does not lower total input size; top-k vector search fits focused questions but risks biased coverage for broad pros/cons. Recommend aggregating positive/negative themes, counts and supporting examples before returning a compact ToolMessage. Next: identify tradeoff of lost minority details from compression.
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK22-attempt1-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-check22-a2-rare-angle-20261012:start -->
L3-CHECK-22 attempt2: needs_review. Learner noted that review aggregation can lose fresh minority perspectives, but did not provide a concrete example. Recheck requests one specific low-frequency concern affecting purchasing decisions.
<!-- learn-agent:evidence:stage01-ch03-check22-a2-rare-angle-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-L3-CHECK22-attempt3-pass-20261012:start -->
## L3-CHECK-22 / attempt3：passed
学员举出“续航”作为5000条无线键盘评价归纳时可能被高频主题掩盖的低频但重要缺点。正确实例化了信息压缩Trade-off：更低Token、延迟和上下文成本，代价是丢失罕见而购买决策关键的差评（例如实际电池续航短、需频繁充电）。可以在主题频次汇总之外额外保留严重/新颖低频评价及来源。此前attempt1已掌握上下文占用问题，attempt2提出“丢失新角度的信息”，现在补充了具体例子；本检查正式通过。

下一步：进入Chapter03本章验收题Q1→Q2→Q3，结合已通过的真实DeepSeek单工具与双工具运行证据再审查EX1契约；不得仅凭L3-CHECK通过就宣布全章mastered。
<!-- learn-agent:evidence:stage01-ch03-L3-CHECK22-attempt3-pass-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q1-a1-partial-20261012:start -->
## Chapter03 Q1 / attempt1：部分通过，待复检
正式验收Q1要求解释Tool name、description、parameters、handler四要素存在的因果关系，并指出一个具体边界或失败条件。用户回答：“name明确调用tool工具的函数名或者api名，description供LLM区分与请求调用tool，parameters该tool需要的元数据，handler真正的调用tool，将请求与调用隔离开，方便检验”。
正确：name用于对外标识和Runtime查找Tool；description帮助LLM在库存/价格工具中挑选；handler承载由Runtime执行的业务代码；模型工具请求与实际执行区分开，可在执行前进行校验。
待澄清：name是向模型公开并可由Runtime路由的工具标识符，不一定等于底层Python函数名或外部API地址；parameters是可执行输入Schema（sku:str、必需性、类型、约束等），不是一般元数据；handler是执行业务逻辑或调用外部API的实现，由Runtime触发，不由模型直接执行。
缺失：用户尚未举出任一要素设计不当导致的具体失败案例，Q1契约要求明确适用边界/失败条件。下题只复检一个具体失败例子；回答完整后才可判Q1 passed。
本轮另讨论企业评论分析：保留全量带ID原文，去重脱敏，主题/情感/严重度分析，分层抽样与低频严重风险单独保留，按来源ID回溯；仅将聚合主题、频次、少数风险和证据引用发至ToolMessage，关注低频问题召回率、事实准确、Token成本；向量检索适合聚焦问题，不替代全量主题计数。
<!-- learn-agent:evidence:stage01-ch03-Q1-a1-partial-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q1-a2-input-vs-output-20261012:start -->
## Chapter03 Q1 / attempt2：needs_review
学员选择get_price工具举例，认为parameters没有要求返回int，因此handler可以返回字符串，通过校验但ToolMessage出错。此例提出了输出数据类型与后续处理的真实风险，但错误地把Tool的输入parameters/args_schema与handler返回值校验合并。Tool的parameters描述输入字段、必填/类型/约束，如get_price(sku:str)要求sku字符串；它不负责要求返回int。Python返回注解->int通常不会由运行时自动强制校验。显式ToolMessage(content=str(result))会把整数价格转成字符串，这是正常行为，不会因为字符串形式本身自动报错。真正需要输出格式保证时可对工具result使用Pydantic单独验证。Q1仍缺精确归因的失败案例，下一次attempt3请给出get_price.invoke(...)输入不符合Schema的具体例子，并说明哪个阶段失败。
官方参考：https://reference.langchain.com/python/langchain-core/tools/structured/StructuredTool 和 https://reference.langchain.com/python/langchain-core/tools/convert/tool
<!-- learn-agent:evidence:stage01-ch03-Q1-a2-input-vs-output-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q1-attempt3-passed-20261012:start -->
## Chapter03 Q1 / attempt3：passed（critical）
学员提供有效输入校验失败示例：`get_price.invoke(12)`，直接传入整数而不是需要的工具输入Schema字典（如`{"sku":"KB-001"}`）。LangChain @tool对象使用BaseTool.invoke(input)接收str/dict/ToolCall，错误类型/结构在进入get_price handler前的工具输入解析/Pydantic模型校验中失败，通常产生ValidationError。结合先前L3-CHECK-20已经正确解释缺少sku时ValidationError发生在Schema阶段、handler未执行，以及Q1 attempt1准确解释name/description/handler与请求执行分离，此例已经满足Q1关键题：四要素的原因、可执行边界与失败情况。Q1正式判passed，不重复索要此前已经答过的因果解释。
更正细节：get_price.invoke(12)输入本身类型/结构不合规范，与handler返回价格的int类型检查无关；需要输出校验时应独立实施Pydantic校验。ToolMessage(content=str(result))接受文本形式是正常行为。
下一题正式章节Q2（critical）：对照普通Python函数及@tool包装的Tool对象，明确name、description、args_schema、handler映射，输入/输出与调用的完整路径，并描述可以验证的一项测试。
<!-- learn-agent:evidence:stage01-ch03-Q1-attempt3-passed-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q2-attempt1-invoke-only-20261012:start -->
## Chapter03 Q2 / attempt1
状态：needs_review（部分正确）。学员回答“普通Python函数需要**args，@tool直接传入args即可”，已抓住同一args字典传入普通Python函数时需要关键字参数展开（raw_get_price(**args)），而LangChain工具对象通过get_price.invoke(args)将字典作为一个input。教师补充两者结果均为199。尚未说明@tool除handler外增加的name、description、args_schema/输入验证、模型bind_tools工具声明与Runtime执行接口等映射，以及如何用测试验证。下一题只问新增能力为什么支持LLM工具调用；随后补充调用路径和验证。
<!-- learn-agent:evidence:stage01-ch03-Q2-attempt1-invoke-only-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q2-attempt2-20261012:start -->
## Chapter03 Q2 / attempt2：needs_review
用户回答“args_schema配置了with_structed_moel可进行pydantic校验；.invoke()可直接传入字符串且不用进行关键字参数转化”。核查当前LangChain文档确认，单参数get_price(sku:str)的@tool对象既可invoke({"sku":"KB-001"})也支持invoke("KB-001")，字符串映射到第一个参数Schema字段；多参数工具应统一使用字典输入。args_schema由@tool默认推断自函数签名，或显式配置Pydantic输入模型，调用时执行输入校验；model.with_structured_output(SomePydanticModel)则用于解析/验证LLM自身的结构化输出，两者是不同环节，不需要组合使用。学员理解invoke无需展开关键字参数，但混淆两类Schema机制，也未解释name/description供LLM选择工具、handler由Runtime实际调用和验证两种版本结果一致的完整链路。
下一题Chapter03 Q2 attempt3：直接对比args_schema和with_structured_output分别验证什么，采用get_price(sku:str)的参数示例回答。
参考：https://reference.langchain.com/python/langchain-core/tools/base/BaseTool 和 https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel/with_structured_output
<!-- learn-agent:evidence:stage01-ch03-Q2-attempt2-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q2-attempt3and4-passed-20261012:start -->
## Chapter03 Q2 / attempt3：passed
学员正确区分场景A使用Tool的args_schema校验SKU输入，场景B使用model.with_structured_output()解析/验证LLM生成的Pydantic Product对象；已纠正混淆两类Schema机制的误解。

## Chapter03 Q2 / attempt4：passed（critical题总体通过）
学员独立串联用户查询KB-001价格、DeepSeek参考已注册工具description挑选工具并生成Tool Call、Runtime根据name获取目标工具、通过.invoke(...)触发args_schema输入校验后调用handler返回199、构造ToolMessage并回传模型。这与之前已运行验证的真实DeepSeek单工具和双工具实验构成完整的数据流证据。
细节订正：model.bind_tools只向LLM呈现工具声明，不会自动完成name→Python工具对象路由；在本次手写Runtime中是tools_by_name[call["name"]]负责白名单查找。ToolMessage须用原始call["id"]关联模型发出的调用；本细节已在L3-CHECK-10和19通过。
两次复检合并达到正式Q2验收：映射原理侧raw_get_price(**args)至LangChain @tool包装对象get_price.invoke(args)，掌握输入/输出及关键数据流；实际运行结果get_price为199，API回填成功。正式Q2判passed，Q1已passed；Q3及EX1待按章节契约评估。
<!-- learn-agent:evidence:stage01-ch03-Q2-attempt3and4-passed-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q3-a1-review-20261012:start -->
## Chapter03 Q3 / attempt1: needs_review
学员排查顺序为“查看error输出锁定错误字段→查看call→查看query”，有分阶段检查的意识，但漏掉对照get_price.args_schema核对输入字段。提出“有限重试”的恢复策略，准确说明额外Token成本及可能仍然失败的风险；尚未指出product_id与必填sku不匹配，也未给出字段修正或向模型返回参数错误的具体根因修复。仅重试不改变参数可能反复收到同一ValidationError。下一题聚焦错误参数名与直接修复方案。Q1、Q2 critical已通过；Q3未验收。
<!-- learn-agent:evidence:stage01-ch03-Q3-a1-review-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q3-attempt2-field-vs-type-20261012:start -->
## Chapter03 Q3 / attempt2 — needs_review
学生认为get_price的Tool Call {"product_id":"KB-001"}“与str不匹配，严格校验”。这里传入的值"KB-001"本身是str，真正错误是参数名字不符合get_price(sku:str)要求，缺少必填字段sku（若额外字段不允许，还可能报多余字段）。类型严格校验无法解决键名错误；在Pydantic输入Schema阶段会因sku缺失而抛ValidationError，handler并未执行。下一题Q3 attempt3请学员自行写正确的call["args"]字典，使get_price按SKU正常运行，再完成Q3总结与EX1验收。
<!-- learn-agent:evidence:stage01-ch03-Q3-attempt2-field-vs-type-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q3-a3-sku-value-20261012:start -->
Q3 attempt3: needs_review. The input sku is a valid string, but the product key 001 is not in the prices dictionary. Handler raises KeyError after Schema validation.
<!-- learn-agent:evidence:stage01-ch03-Q3-a3-sku-value-20261012:end -->

<!-- learn-agent:evidence:stage01-ch03-Q3-attempt4-passed-20261012:start -->
Q3 passed: corrected args to sku=KB-001 and obtained 199. EX1 next.
<!-- learn-agent:evidence:stage01-ch03-Q3-attempt4-passed-20261012:end -->
