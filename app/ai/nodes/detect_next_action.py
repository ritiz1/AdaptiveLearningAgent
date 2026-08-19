from __future__ import annotations 

from app.ai.graph.state import WorkflowState
from app.domain.routing.models import TeachingAction 


def detect_next_action_node(state: WorkflowState) -> dict:
    """Determine the next action based on the current state."""
    if state["learner_state"] is None:
        raise ValueError("Learner state is required to detect next action.")


    action_by_intent = {
        "learn" : TeachingAction.TEACH,
        "review" : TeachingAction.PRACTICE,
        "debug" : TeachingAction.DIAGNOSE
    }
    intent = state["intent"]
    action = action_by_intent.get(intent, TeachingAction.TEACH)

    return {
        "next_action" : action.value
    }



