from __future__ import annotations

from typing import Any

from langchain_core.tools import tool

from app.ai.tools.serialization import to_jsonable
from app.ai.tools.tool_context import safe_reads


@tool
def get_dependencies(
    concept_id: str,
    max_depth: int = 2,
) -> Any:
    """
    Fetch a small prerequisite neighborhood for one concept.

    Use this tool when missing prerequisite knowledge may be
    blocking the learner's understanding.
    """

    # Ask the concept service for this concept's prerequisites.
    result = safe_reads.get_dependencies(
        concept_id=concept_id,
        max_depth=max_depth,
    )

    # Convert ConceptNeighborhood into an LLM-readable dictionary.
    return to_jsonable(result)