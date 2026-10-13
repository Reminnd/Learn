# LangChain 与 Agent 基础 / Chapter 05

# Agent Loop：智能体运行循环

## 本章定位

本章属于 `stage-01`。

教学时只加载 manifest 的 `state.current`、本章当前小节与已解析的验收契约；不要加载其他章节全文。

## 学习目标

- 理解 model→tool→observation→model 循环
- 手写最小 Agent Loop
- 理解框架 Agent 在封装什么

## 强制教学顺序

```text
真实问题
 ↓
最小原理版
 ↓
运行流程
 ↓
LangChain / LangGraph 对应实现
 ↓
手写版 vs 框架版
 ↓
工程问题
 ↓
解决策略 + Trade-off
 ↓
企业级改造
 ↓
测试 / 安全 / 可观测性
 ↓
练习
 ↓
Q&A
```

## 本章核心工程问题

- 死循环
- max_turns
- max_tool_calls
- 超时
- 成本失控

教学时不要只列出这些问题；需要至少选择最重要的问题进行“复现 → 原因 → 方案 → Trade-off → 框架实现”。

## 原理与框架映射重点

- while loop → LangChain Agent
- 控制循环 → LangGraph execution
- 运行限制 → Harness Runtime Policy

必要时读取：

- `shared/framework-map.md`
- `shared/glossary.md`
- `shared/qa-rubric.md`（仅用于反馈）
- `shared/chapter-contract.md` 与 `shared/mastery-rubric.md`（仅在练习、Q&A 或掌握判定时）

## 补充范式与源码对照（不新增验收项）

- **ReAct（P0）**：对应“模型选择动作/工具 → 执行 → Observation（工具返回）→ 更新上下文并再次决策”。分析可见的工具调用与执行事实，不要求暴露模型隐藏的内部思考文本。
- **Tool-Calling Agent与ReAct的区别**：Tool Calling主要是模型/应用的接口能力，ReAct是循环式推理与行动策略；使用工具调用不一定等于完整ReAct实现。
- **Workflow vs Agent**：固定`prompt → validate → output`链路可由代码编排；当下一步工具由模型动态决定时才需要Agent Loop。比较开销、终止条件和错误传播。
- **真实项目阅读点**：寻找模型请求、`tool_calls`解析、Registry查找、handler、观察结果回传、`max_turns`/取消和退出条件；追踪一次真实链路，不按函数名称推断范式。
- 案例和P0/P1分级按需参照[Agent范式映射](../agent-paradigm-map.md)与[项目源码学习法](../../shared/project-source-learning.md)；本章EX/Q&A/mastery契约保持不变。

## Project Track 集成提示

- 如果 `project_track_status != active`：本章只作为可复用能力学习，不绑定任何长期项目，不使用旧的默认项目。
- 如果 `project_track_status == active`：结合用户已经选定的真实项目，说明本章能力应落在哪个模块，并设计一个最小可验收增量。
- 重要架构选择达到 ADR 条件时，先解析 manifest 的 `adr.root`，再记录 ADR。

## 验收契约

````yaml
chapter_id: stage-01-05-agent-loop
prerequisites: ["stage-01-04-tool-registry-engineering"]
required_exercises:
  - id: EX1
    task: "围绕Agent Loop：智能体运行循环，实现最小原理版并用框架表达同一能力"
    acceptance:
      - "产出可运行代码或可执行伪代码，展示：理解 model→tool→observation→model 循环"
      - "能复现或具体分析工程问题：死循环"
      - "能解释并验证框架映射：while loop → LangChain Agent"
questions:
  - id: Q1
    prompt: "为什么需要这项能力：理解 model→tool→observation→model 循环"
    critical: true
    acceptance:
      - "给出核心因果关系，而不是只复述定义"
      - "说明至少一个适用边界或失败条件"
  - id: Q2
    prompt: "如何验证这项原理—框架映射：while loop → LangChain Agent"
    critical: true
    acceptance:
      - "明确原理侧与框架侧的对应对象"
      - "说清输入、输出与关键数据流"
  - id: Q3
    prompt: "遇到该工程问题时如何定位并权衡方案：死循环"
    critical: false
    acceptance:
      - "给出可执行的排查顺序"
      - "说明至少一个方案 Trade-off"
mastery:
  threshold: 80
  dimension_floor_ratio: 0.60
  critical_questions: [Q1, Q2]
  required_exercises: [EX1]
```

掌握判定与补考统一使用 `shared/mastery-rubric.md`；不得仅凭“通过后”或总分印象标记 `mastered`。


