# LangChain 与 Agent 基础 / Chapter 04

# Tool Registry 与工具工程化

## 本章定位

本章属于 `stage-01`。

教学时只加载 manifest 的 `state.current`、本章当前小节与已解析的验收契约；不要加载其他章节全文。

## 学习目标

- 统一注册工具
- 理解 Tool 生命周期
- 加入 timeout/retry/risk 等元数据

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

- 工具冲突
- 连续失败
- 副作用
- 权限与审计
- 结果过大

教学时不要只列出这些问题；需要至少选择最重要的问题进行“复现 → 原因 → 方案 → Trade-off → 框架实现”。

## 原理与框架映射重点

- ALL_TOOLS dict → registry
- LangChain tools → LangGraph ToolNode
- 应用逻辑 → Harness Tool Policy

必要时读取：

- `shared/framework-map.md`
- `shared/glossary.md`
- `shared/qa-rubric.md`（仅用于反馈）
- `shared/chapter-contract.md` 与 `shared/mastery-rubric.md`（仅在练习、Q&A 或掌握判定时）

## Project Track 集成提示

- 如果 `project_track_status != active`：本章只作为可复用能力学习，不绑定任何长期项目，不使用旧的默认项目。
- 如果 `project_track_status == active`：结合用户已经选定的真实项目，说明本章能力应落在哪个模块，并设计一个最小可验收增量。
- 重要架构选择达到 ADR 条件时，先解析 manifest 的 `adr.root`，再记录 ADR。

## 验收契约

````yaml
chapter_id: stage-01-04-tool-registry-engineering
prerequisites: ["stage-01-03-tool-basics"]
required_exercises:
  - id: EX1
    task: "围绕Tool Registry 与工具工程化，实现最小原理版并用框架表达同一能力"
    acceptance:
      - "产出可运行代码或可执行伪代码，展示：统一注册工具"
      - "能复现或具体分析工程问题：工具冲突"
      - "能解释并验证框架映射：ALL_TOOLS dict → registry"
questions:
  - id: Q1
    prompt: "为什么需要这项能力：统一注册工具"
    critical: true
    acceptance:
      - "给出核心因果关系，而不是只复述定义"
      - "说明至少一个适用边界或失败条件"
  - id: Q2
    prompt: "如何验证这项原理—框架映射：ALL_TOOLS dict → registry"
    critical: true
    acceptance:
      - "明确原理侧与框架侧的对应对象"
      - "说清输入、输出与关键数据流"
  - id: Q3
    prompt: "遇到该工程问题时如何定位并权衡方案：工具冲突"
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


