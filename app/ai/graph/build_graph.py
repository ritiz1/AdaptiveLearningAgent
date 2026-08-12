from __future__ import annotations
from langgraph.graph import StateGraph, START, END


from app.ai.graph.state import WorkflowState
from app.ai.nodes import (
    understand_request_node,
    load_learner_state_node,
    tutor_node,
)

def build_graph():
    workflow = StateGraph(WorkflowState)
    workflow.add_node("understand_request", understand_request_node)
    workflow.add_node("load_learner_state", load_learner_state_node)
    workflow.add_node("tutor", tutor_node)


    workflow.add_edge(START, "understand_request")
    workflow.add_edge("understand_request", "load_learner_state")
    workflow.add_edge("load_learner_state", "tutor")
    workflow.add_edge("tutor", END)


    return workflow.compile()

    