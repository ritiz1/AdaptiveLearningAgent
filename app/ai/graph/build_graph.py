from __future__ import annotations
from langgraph.graph import StateGraph, START, END


from app.ai.graph.state import WorkflowState
from app.ai.nodes import (
    understand_request_node,
    load_learner_state_node,
    tutor_node,
    detect_next_action_node,
    diagnose_node,
    practice_node,
)


def build_graph():
    workflow = StateGraph(WorkflowState)
    workflow.add_node("understand_request", understand_request_node)
    workflow.add_node("load_learner_state", load_learner_state_node)
    workflow.add_node("tutor", tutor_node)
    workflow.add_node("detect_next_action", detect_next_action_node)
    workflow.add_node("diagnose", diagnose_node)
    workflow.add_node("practice", practice_node)


    workflow.add_edge(START, "understand_request")
    workflow.add_edge("understand_request", "load_learner_state")
    # workflow.add_edge("load_learner_state", "tutor")
    workflow.add_edge("load_learner_state", "detect_next_action")
    # workflow.add_edge("detect_next_action", "tutor")
    workflow.add_conditional_edges (
        "detect_next_action", 
        lambda state: state["next_action"],
        {
            "teach" : "tutor",
            "practice" : "practice",
            "diagnose" : "diagnose",
        })

    workflow.add_edge("practice" , END) 
    workflow.add_edge("diagnose" , END)
    workflow.add_edge("tutor", END)
    # print(workflow.get_graph().draw_mermaid_png())

    return workflow.compile()
