from __future__ import annotations

from app.ai.graph.state import WorkflowState


def tutor_node(state: WorkflowState) -> dict:
    """LLM Call #2 (later): generate personalized teaching response.

    Phase 0: stub only. Phase 1B will make this node tool-enabled with
    SafeReadTools (max 1-2 rounds).
    """
    # TODO Phase 1: build prompt from intent + target_concept + learner_state
    return {
        "tutor_response": f"[stub] would teach: {state.get('target_concept')}",
    }


    