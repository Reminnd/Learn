# Learn

Learn 是面向 Python 基础学习者的企业级 Agent Harness 课程仓库。课程从最小原理出发，映射到 LangChain / LangGraph，并逐步覆盖工程化、可靠性与企业级架构能力。

## Quick Start

按以下唯一路径完成首次学习环境准备：

1. Clone 仓库并进入 checkout。

   ```text
   git clone https://github.com/Reminnd/Learn.git
   cd Learn
   ```

2. 阅读 [Stage 01 runtime baseline](environment/framework-baseline.md)；直接依赖以 [Stage 01 requirements](environment/requirements-stage-01.txt) 为准。
3. 创建并按当前 shell 的方式激活虚拟环境，然后安装依赖。

   ```text
   python -m venv .venv
   python -m pip install -r environment/requirements-stage-01.txt
   ```

4. 运行 [preflight](scripts/preflight.py)。

   ```text
   python scripts/preflight.py
   ```

5. 运行 [Stage 01 EX1](examples/stage-01/ex1_message_prompt_langchain.py)。

   ```text
   python examples/stage-01/ex1_message_prompt_langchain.py
   ```

6. 开始 [Stage 01 Chapter 01](curriculum/stage-01/01-llm-message-prompt-langchain.md)，之后按 [课程索引](curriculum/index.md) 的 canonical route 学习。

这条路径依次连接：clone → README → environment/runtime → preflight → EX1 → Stage 01 Chapter 01 → curriculum route。

## Stage 01 可执行基线

[Framework baseline](environment/framework-baseline.md) 定义 runtime assumptions，[requirements](environment/requirements-stage-01.txt) 定义直接依赖；[preflight](scripts/preflight.py) 与 [EX1](examples/stage-01/ex1_message_prompt_langchain.py) 构成进入首章前的可执行检查。

## Core Path

Core Path 覆盖 Stage 01–09。完整且唯一的章节顺序见 [课程索引](curriculum/index.md)。

## Advanced Track

Advanced Track 覆盖 Stage 10–14。完成 Core Path 后，由学习者明确选择是否进入；边界与顺序以 [课程索引](curriculum/index.md) 为准。

## Runtime initialization

首次使用“继续学习”前，在 checkout 外初始化 runtime：

```text
python scripts/setup_runtime.py --runtime-root ../Learn-runtime
```

[Runtime initialization script](scripts/setup_runtime.py) 会在指定目录建立 storage manifest，并由 manifest 定位真实的 `state.current`。checkout 内的 seed 不是学习者的真实 runtime state。

## 继续学习

Runtime 初始化后，对 Learn Agent 输入“继续学习”。[SKILL router](SKILL.md) 会通过 manifest 读取真实 `state.current`，并恢复已提交的学习位置与 continuation 信息。

Continuation 路径为：README → checkout 外 runtime initialization → manifest / `state.current` → “继续学习” → SKILL router。
