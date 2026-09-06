"""Stage 01 EX1: compare native and LangChain message flows offline."""

from __future__ import annotations

import sys

from langchain_core.language_models.fake_chat_models import (
    FakeMessagesListChatModel,
)
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate


RESPONSE_CONTENT = "Deterministic assistant response."
USER_INPUTS = (
    "What is a message?",
    "What is a prompt?",
    "How do they work together?",
)
EXPECTED_HISTORY_LENGTHS = [2, 4, 6]


def run_principle_flow() -> tuple[list[dict[str, str]], list[int], list[str]]:
    history: list[dict[str, str]] = []
    history_lengths: list[int] = []
    responses: list[str] = []

    for user_content in USER_INPUTS:
        history.append({"role": "user", "content": user_content})
        assistant_content = RESPONSE_CONTENT
        history.append({"role": "assistant", "content": assistant_content})
        responses.append(assistant_content)
        history_lengths.append(len(history))

    return history, history_lengths, responses


def run_framework_flow() -> tuple[list[HumanMessage | AIMessage], list[int], list[str]]:
    prompt = ChatPromptTemplate.from_messages([("placeholder", "{history}")])
    model = FakeMessagesListChatModel(
        responses=[AIMessage(content=RESPONSE_CONTENT) for _ in USER_INPUTS]
    )
    chain = prompt | model

    history: list[HumanMessage | AIMessage] = []
    history_lengths: list[int] = []
    responses: list[str] = []

    for user_content in USER_INPUTS:
        history.append(HumanMessage(content=user_content))
        response = chain.invoke({"history": history})
        history.append(response)
        responses.append(response.content)
        history_lengths.append(len(history))

    return history, history_lengths, responses


def main() -> int:
    principle_history, principle_lengths, principle_responses = run_principle_flow()
    framework_history, framework_lengths, framework_responses = run_framework_flow()

    principle_roles = [message["role"] for message in principle_history]
    expected_principle_roles = ["user", "assistant"] * len(USER_INPUTS)
    expected_framework_types = [HumanMessage, AIMessage] * len(USER_INPUTS)
    framework_types = [type(message) for message in framework_history]

    checks = (
        (principle_roles == expected_principle_roles, "principle roles differ"),
        (principle_lengths == EXPECTED_HISTORY_LENGTHS, "principle history lengths differ"),
        (framework_lengths == EXPECTED_HISTORY_LENGTHS, "framework history lengths differ"),
        (framework_types == expected_framework_types, "framework message types differ"),
        (principle_responses == framework_responses, "response contents differ"),
    )
    for passed, error in checks:
        if not passed:
            print(f"EX1=FAIL: {error}", file=sys.stderr)
            return 1

    role_names = ",".join(principle_roles[:2])
    length_values = ",".join(str(length) for length in principle_lengths)
    framework_type_names = ",".join(
        message_type.__name__ for message_type in framework_types[:2]
    )

    print(f"principle_roles={role_names}")
    print(f"history_lengths={length_values}")
    print(f"framework_roles={framework_type_names}")
    print("responses_equal=true")
    print("external_api=not_used")
    print("EX1=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
