# Stage 01 Framework Baseline

This document is the authority for Stage 01 runtime assumptions.
`environment/requirements-stage-01.txt` is the authority for direct dependencies.

## Runtime assumptions

- CPython 3.11.x
- UTF-8 text encoding
- A standard Python virtual environment
- `langchain-core==1.6.2`
- No provider SDK
- No API key
- Access to a Python package index for the first dependency installation
- After dependency installation, EX1 requires no external API or network access
