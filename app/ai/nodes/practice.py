from __future__ import annotations 

from langchain_core.messages import HumanMessage,SystemMessage

from app.ai.graph.state import WorkflowState
from app.infrastructure.llm.client import get_llm

llm = get_llm()

def practice_node(state: WorkflowState) -> dict:
    """Generate one practice question without revealing the solution ."""
    if state["learner_state"] is None:
        raise ValueError("Learner state is required to generate practice question.")

    response = llm.invoke([
        SystemMessage(content=(
                    "You are an adaptive tutor. "
                    "Give the learner exactly one short practice question. "
                    "Do not provide the answer yet. "
                    "Wait for the learner to respond."
                )
        ),
        HumanMessage (
            content = (
                f"Target concept : {state['target_concept']}\n"
                f"Learner request : {state['user_message']}\n"
            )

        )
    ] )
    return {
        "tutor_response" : response.content
    }