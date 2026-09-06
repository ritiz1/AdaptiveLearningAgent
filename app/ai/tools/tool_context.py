"""
Build the read-only tool surface used by the Phase 1B tools.

Services come from the composition root, so the tools and the
load_learner_state node always read from the same backend within a turn.
The surface is built on first use rather than at import time, which keeps
importing a tool module free of database configuration.
"""

from __future__ import annotations

from functools import lru_cache

from app.ai.tools.safe_reads import SafeReadTools
from app.services.container import (
    get_concept_service,
    get_evidence_service,
    get_learner_service,
)


@lru_cache(maxsize=1)
def get_safe_reads() -> SafeReadTools:
    """Return the shared read-only access layer for the LLM tools.

    SafeReadTools is the single controlled entry point: the LLM never
    receives write access to these services.
    """

    return SafeReadTools(
        learner_service=get_learner_service(),
        concept_service=get_concept_service(),
        evidence_service=get_evidence_service(),
    )
