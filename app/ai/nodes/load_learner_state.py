from __future__ import annotations
from app.ai.graph.state import WorkflowState
from app.services.learner_service.hardcoded import HardcodedLearnerService
def load_learner_state_node(state: WorkflowState) -> dict:
    """Load this user's learner slice via LearnerService (no LLM).
    Phase 0: stub only. Phase 1 will call a hardcoded LearnerService
    implementation; Phase 2 swaps it for PostgreSQL behind the same interface.
    """
    # TODO Phase 1: learner_service.get_learner_state(state["user_id"])
    learner_service = HardcodedLearnerService()
    learner_state = learner_service.get_learner_state(state["user_id"])
    return {
        "learner_state": learner_state,
    }

    