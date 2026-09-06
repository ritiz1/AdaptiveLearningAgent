from __future__ import annotations

from typing import Any 

from langchain_core.tools import tool

from app.ai.tools.serialization import to_jsonable
from app.ai.tools.tool_context import get_safe_reads

@tool 
def get_recent_evidence(
    user_id: str, 
    concept_id: str,
    limit: int = 4,
) -> Any:
    """
    Fetch recent quiz or diagnostic evidence for a learner and concept.
    Use this tool when previous learner attempts may help determine
    the appropriate teaching response.
    """


    # Ask the evidence service for this learner's recent evidence.
    result = get_safe_reads().get_recent_evidence(
        user_id=user_id,
        concept_id=concept_id,
        limit=limit,
    )
    
    # convert the evidence list into llm-readable dictionary.
    return to_jsonable(result)


    