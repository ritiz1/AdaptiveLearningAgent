from __future__ import annotations
from app.ai.graph.state import WorkflowState
from langchain_core.messages import HumanMessage, SystemMessage 

from app.ai.graph.state import WorkflowState
from app.ai.llm_schemas.understand_request import RequestUnderstanding
from app.infrastructure.llm.client import get_llm


structured_llm = get_llm().with_structured_output(
    RequestUnderstanding,
    method="json_schema",
    strict=True,
)

def understand_request_node(state: WorkflowState) -> dict:
    result = structured_llm.invoke(
        [
            SystemMessage(
                content=(
                    "Analyze the learner's request. Classify the intent as "
                    "learn, review, or debug. Extract only the concise target "
                    "concept, not the full user message."
                )
            ),
            HumanMessage(content=state["user_message"]),
        ]
    )
    return result.model_dump()
