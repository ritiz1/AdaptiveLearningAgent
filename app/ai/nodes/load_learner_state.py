from __future__ import annotations
from app.ai.graph.state import WorkflowState
from app.services.container import get_learner_service


def load_learner_state_node(state: WorkflowState) -> dict:
    """Load this user's learner slice via LearnerService (no LLM).

    The service comes from the composition root, so this node and the LLM
    tools always read from the same backend.
    """
    learner_service = get_learner_service()
    learner_state = learner_service.get_learner_state(state["user_id"])
    return {
        "learner_state": learner_state,
    }
