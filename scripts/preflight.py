"""Check the local runtime required by the Stage 01 LangChain example."""

from __future__ import annotations

import importlib.metadata
import platform
import sys
from pathlib import Path


EXPECTED_VERSION = "1.6.2"
DEPENDENCY = "langchain-core"
EXAMPLE_PATH = Path("examples/stage-01/ex1_message_prompt_langchain.py")
INSTALL_COMMAND = "python -m pip install -r environment/requirements-stage-01.txt"


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    print("preflight=FAIL", file=sys.stderr)
    return 1


def main() -> int:
    implementation = platform.python_implementation()
    if implementation != "CPython":
        return fail(f"python=FAIL expected=CPython actual={implementation}")

    actual_python = f"{sys.version_info.major}.{sys.version_info.minor}"
    if sys.version_info[:2] != (3, 11):
        return fail(f"python=FAIL expected=3.11 actual={actual_python}")
    print("python=PASS")

    try:
        actual_version = importlib.metadata.version(DEPENDENCY)
    except importlib.metadata.PackageNotFoundError:
        return fail(
            f"dependency=FAIL {DEPENDENCY} missing\n"
            f"install={INSTALL_COMMAND}"
        )

    if actual_version != EXPECTED_VERSION:
        return fail(
            f"dependency=FAIL {DEPENDENCY} "
            f"expected={EXPECTED_VERSION} actual={actual_version}\n"
            f"install={INSTALL_COMMAND}"
        )

    try:
        from langchain_core.language_models import FakeMessagesListChatModel
        from langchain_core.messages import AIMessage, HumanMessage
        from langchain_core.prompts import ChatPromptTemplate
    except ImportError as error:
        return fail(f"dependency=FAIL public_imports_unavailable error={error}")

    del ChatPromptTemplate, HumanMessage, AIMessage, FakeMessagesListChatModel
    print(f"dependency=PASS {DEPENDENCY}=={EXPECTED_VERSION}")

    repository_root = Path(__file__).resolve().parents[1]
    example = repository_root / EXAMPLE_PATH
    if not example.is_file():
        return fail(f"filesystem=FAIL missing {EXAMPLE_PATH.as_posix()}")
    try:
        with example.open("rb") as stream:
            stream.read(0)
    except OSError as error:
        return fail(
            f"filesystem=FAIL unreadable {EXAMPLE_PATH.as_posix()} error={error}"
        )
    print(f"filesystem=PASS {EXAMPLE_PATH.as_posix()}")

    print("external_api=NOT_REQUIRED")
    print("preflight=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
