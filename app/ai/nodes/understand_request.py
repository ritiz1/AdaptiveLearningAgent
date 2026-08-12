from __future__ import annotations
from app.ai.graph.state import WorkflowState

def understand_request_node(state : WorkflowState) -> WorkflowState:
    """LLM Call #1 (later): classify intent + target concept from user_message.
    Phase 0: stub only. Returns placeholder values so the graph can run
    end-to-end without an LLM.
    """
    # TODO Phase 1: call LLM with structured output (intent, target_concept),
    return {
        "intent" : "learn",
        "target_concept" : state["user_message"],  #naive approach for now , we will improve this later 
    }


