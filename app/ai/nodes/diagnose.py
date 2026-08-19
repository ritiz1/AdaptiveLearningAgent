from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from app.ai.graph.state import WorkflowState
from app.infrastructure.llm.client import get_llm

llm = get_llm()


def diagnose_node(state: WorkflowState) -> dict:
    """Ask one question to identify the learner's confusion."""

    if state["learner_state"] is None:
        raise ValueError("Learner state is required for diagnosis.")

    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are an adaptive tutor diagnosing confusion. "
                    "Ask exactly one short, focused diagnostic question. "
                    "Do not explain or solve the problem yet. "
                    "Wait for the learner's response."
                )
            ),
            HumanMessage(
                content=(
                    f"Target concept: {state['target_concept']}\n"
                    f"Learner request: {state['user_message']}"
                )
            ),
        ]
    )

    return {"tutor_response": response.content}