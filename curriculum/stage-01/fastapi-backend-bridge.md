# Stage 01/04 → 05 桥接单元：FastAPI 最小业务后端

> **采用日期**：2026-10-14。用户已明确确认“后端基础先行、Agent与后端交替深入”的学习路线。
>
> **性质**：Stage 01 第04章与第05章之间的**先修教学插曲**，不新增编号章节，不属于第41章，不改变 [40章唯一课程顺序](../index.md)、Stage 01/05的prerequisites、原本的EX/Q&A/mastery算法或任何已经提交的课程成绩。它属于**知识与项目实践安排**；正式课程完成进度仍以manifest解析出的committed `state.current`为准。未在此单元真正学习/回答/运行的知识不能因为制定了本计划而记为已掌握。

## 一、插入位置与恢复

```text
现有Stage 01/04（Tool Registry）
   └─按原章验收，直到mastered
     → [Bridge-FAPI：FastAPI最小服务]  ← 本文件（先教学，不提前算Stage13）
       → 现有Stage 01/05（Agent Loop + ReAct）
         → 以此前FastAPI服务作为一个可复用入口，逐步替换内部实现
           → Stage 02 LangGraph + SQL/数据库入门
             → 后续Agent/后端模块交替深入
```

**现有优先级**：如果用户还有已经激活的旧章补课（R01/TS-0/R02/R03），先按已经提交的学习状态与补课约定继续；完成后返回Stage01/04，不因为确认FastAPI计划而跳过第04章。第04章未mastered时，本文件仅可供预览，不把Bridge当作正式下一章。进入Stage01/05时，在讲ReAct/while-loop前先按需完成本桥接教学。

教学入口约定：
- 以用户**已确认的路线**为准，默认在第04章正式完成后、开始第05章新知识前安排该桥接单元。
- **不新增路由节点**：当正式路由已按`curriculum/index.md`进入Stage 01/05时，教学先加载本文件的相关小节，再恢复第05章正文；不伪造一个`stage-01-04.5`或`mastered`状态。
- 如需跨聊天记录桥接学习进度，仅在manifest定义的`notes.root`（按已提交的当前章节`note_pointer`）与`notes.index`做**有实际答题证据的增量记录**，保存最后学到的Bridge单元与下一个问题；复用既有`return_to`/checkpoint机制，不增添另一套进度数据库，也不覆盖第04章mastery。
- 不强制引入独立长期项目；允许使用可信的最小Price Tool示例，也可用用户提供的Vibe Coding代码作只读学习载体。源码未实际读取时，不声称找到了工程实现。

## 二、最小先修

- 已学Python函数、字典、异常、类型注解及Pydantic；已学GET/POST与HTTP/JSON的基本概念。
- 第04章将学Tool Registry、名称冲突、合法工具选择与handler调用。
- Python`async def`、`await`从最小例子逐步教；**不要把TypeScript Promise与Python协程对象说成同一种东西**。尚未学习数据库和React也能完成本桥接。
- FastAPI装配在本地可信开发环境、使用现有虚拟环境；先确认项目依赖和Python版本，再按实际环境使用`uv`或`pip`，不要求学习者重新搭建完整仓库。

## 三、学习大纲：四个小节，按实际学习速度推进

### B-FAPI-01｜Web服务最小模型

- **问题**：为什么`get_price(sku)`只是函数，HTTP客户端无法天然远程调用？
- **重点**：Client/Server、Request/Response、`app = FastAPI()`、`@app.get`、`@app.post`、路径操作函数、`/docs`、状态码。
- **源码对照**：`普通Python函数 → FastAPI路由装饰器 → JSON Response`；与之前手写`Tool Registry`分别承担什么职责？
- **小检查**：说出`@app.get("/health")`是定义路由还是立即处理请求；哪些输入来自用户HTTP请求？

### B-FAPI-02｜Pydantic请求/响应Schema与错误

- **问题**：为什么外部JSON不能直接信任并传给handler？
- **重点**：Request Body、`BaseModel`、`response_model`、请求体校验422、业务404、内部异常与敏感错误边界。
- **复用旧知识**：Python `Product.model_validate(...)` 与FastAPI自动请求校验的对应关系；TypeScript侧可与Kimi Code AJV/Zod比较，但不强迫提前掌握TS框架。
- **小检查**：区分“缺少必填sku字段→422”、“合法格式但SKU不存在→404”、“工具名未知→受控失败”分别由哪一层处理。

### B-FAPI-03｜业务分层、Dependency Injection与异步

- **问题**：HTTP路由能否直接承担Registry、业务判断、数据库连接与模型调用的全部职责？
- **重点**：Route/Service/Registry/Handler边界、`Depends`依赖注入的基本原理；`async def`适合真实异步I/O，普通`def`也可正常作为FastAPI路由；异常和取消的传播基础。
- **源码学习**：先看同一个`get_price`从`POST /tools/price`进入直到响应，不必立即上复杂DI容器、NestJS或微服务。
- **小检查**：路由的职责与Tool Registry有什么区别？为什么不能允许LLM随意提交Python字符串让路由直接`eval`？

### B-FAPI-04｜API测试与最小验收

- **重点**：`pytest`、FastAPI `TestClient`、`httpx`、`assert`；测试隔离、输入边界、负向路径。
- **最低验证案例**：`GET /health`成功；`POST /tools/price`合法请求得到正确业务值；缺参/类型错误得到422；合法但不存在的SKU得到受控404；工具执行错误不会泄漏内部敏感信息。
- **学习者可以**解释已有测试、预测结果、自己运行一小段可信代码，或逐步实现最小接口；**不要求把一个完整大型后端重新敲一遍**。
- **通过依据**：能正确描述一次请求的完整调用链，并提供上述至少正常、校验失败、业务失败三类可检查的测试/日志或逐步推演证据；这只是Bridge学习证据，不额外替代第04/05章正式mastery。

## 四、最小参考代码（讲解用途，不是已经执行的项目代码）

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

def get_price(sku: str) -> int:
    prices = {"KB-001": 199}
    return prices[sku]  # 不存在SKU抛KeyError，由HTTP层转换为业务404

tool_registry = {"get_price": get_price}  # 已学的最小白名单

class PriceRequest(BaseModel):
    sku: str

class PriceResponse(BaseModel):
    price: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tools/price", response_model=PriceResponse)
def price_endpoint(payload: PriceRequest) -> PriceResponse:
    handler = tool_registry.get("get_price")
    if handler is None:
        raise HTTPException(status_code=503, detail="Tool unavailable")
    try:
        return PriceResponse(price=handler(payload.sku))
    except KeyError:
        raise HTTPException(status_code=404, detail="SKU not found")
```

追踪：`HTTP POST → PriceRequest校验 → price_endpoint → tool_registry.get → get_price → PriceResponse → HTTP JSON`。真实生产系统应有完整日志、权限和错误处理；此例仅用于理解入门分层。**目前无Agent自动决策/模型调用；完成Stage01/05时再将Agent Loop嵌入这个服务。** 不允许对模型提交的任意代码执行`eval/exec`作为练习。

官方对应资料：
- https://fastapi.tiangolo.com/tutorial/first-steps/
- https://fastapi.tiangolo.com/tutorial/body/
- https://fastapi.tiangolo.com/tutorial/dependencies/
- https://fastapi.tiangolo.com/tutorial/testing/

## 五、后续“后端×Agent”螺旋递进，而非等Stage13才开始

| 教学位置 | 后端能力（适时补充） | Agent知识结合点 |
|---|---|---|
| 第04→05章桥接（本文件） | FastAPI路由、Schema、错误、最小DI与TestClient | 把`get_price`变成可调用HTTP工具服务 |
| Stage01/05 Agent Loop | `POST /agent/run`（先可用同步结果），请求/工具异常清晰返回 | ReAct式工具决策、迭代、限流与终止 |
| Stage02 LangGraph之后/期间 | SQL基础、PostgreSQL/MySQL、表结构、CRUD、SQLAlchemy/ORM、事务入门 | 持久保存用户任务、会话、Checkpoints；分清不同类型状态 |
| Stage03–06 Context/RAG/Planning/Memory | 数据模型与检索、异步HTTPX、慢请求/失败重试；按需早接SSE或只看其通信原理 | 检索结果、长任务、上下文与记忆 |
| Stage07–09 Multi-Agent/Deep Agents/Harness | JWT/鉴权概念、Redis缓存、基础SSE/stream、Docker本地部署与CI；依项目阶段实际需要提前 | 事件流、权限、任务协调、运行时策略 |
| Stage10–12 Advanced Track | MCP权限、安全沙箱、Observability/Evaluation深化 | 企业级Agent安全与可测量性 |
| **Stage13原课程（保留）** | **连接池、并发、多租户、缓存一致性、Worker/Queue、持久化重试、容器编排与故障隔离** | 将已经会做的最小Agent API升级为更可靠的企业服务 |

这里的“后端基础提前”**不是**把Stage13复制到Stage01，也不是让初学者提前实现Redis、K8s或完整安全认证。后续能力优先围绕真实问题渐进加入，需求不到不强行堆技术栈。

## 六、与TypeScript和真实源码阅读的协同

- TS-0（JS/TS语法、async/await、interface、泛型）可继续作为**阅读辅助**，但不要等学完React/NestJS才开始FastAPI。
- API请求Schema / `Pydantic` 对照 Kimi Code `AJV`；FastAPI `Depends` 对照TS `interface/Adapter`的抽象思想，但两者不是同一个机制。
- Coding Agent的核心循环用Pi/Kimi/DeepSeek示例；**FastAPI业务层**应在用户提供的后端工程或本最小示例中学习，不声称Pi CLI源码完整覆盖HTTP服务/数据库/鉴权。

## 七、验收与恢复保护

- 当前仓库可能仍处于旧章节专项补课与Stage01/04学习中；制定本Bridge不改变已提交位置、分数、`completed`或`pending_writeback`。
- 教学时一次只问一个问题；失败先纠正并复检，不把任一Bridge概念自动视为已掌握。
- Stage01/04完成 → 桥接B-FAPI-01..04 → Stage01/05的Agent Loop正式内容；若已经选定的项目包含合适FastAPI服务，可仅以该项目真实路由/测试满足对应桥接学习证据。
- 不自动创建长期Project Track；仅用真实学习证据驱动后续。
