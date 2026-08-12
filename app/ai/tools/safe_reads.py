"""Allow-listed read-only LLM tools for the Tutor/Orchestrator node (Phase 1B).

These are thin wrappers around services. The LLM may call them to fetch
extra context. It must never write mastery or mutate authoritative DB state.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.concepts import ConceptNeighborhood
from app.domain.evidence import LearningEvidence
from app.domain.learner import LearnerState
from app.domain.mastery import MasterySnapshot
from app.services.concept_service import ConceptService
from app.services.evidence_service import EvidenceService
from app.services.learner_service import LearnerService

# Hard allow-list from the V1 architecture. Do not add write/web/SQL tools here.
SAFE_READ_TOOL_NAMES = (
    "get_learner_state",
    "get_mastery",
    "get_dependencies",
    "get_recent_evidence",
)


@dataclass
class SafeReadTools:
    """Read-only tool surface the tutor LLM can call (max 1–2 rounds later)."""

    learner_service: LearnerService
    concept_service: ConceptService
    evidence_service: EvidenceService

    def get_learner_state(self, user_id: str) -> LearnerState:
        """Fetch this learner's profile + known knowledge slice."""
        return self.learner_service.get_learner_state(user_id)

    def get_mastery(self, user_id: str, concept_id: str) -> MasterySnapshot:
        """Fetch mastery/confidence for one concept (unknown is allowed)."""
        return self.learner_service.get_mastery(user_id, concept_id)

    def get_dependencies(
        self,
        concept_id: str,
        max_depth: int = 2,
    ) -> ConceptNeighborhood:
        """Fetch a small prerequisite neighborhood for the target concept."""
        return self.concept_service.get_dependencies(
            concept_id,
            max_depth=max_depth,
        )

    def get_recent_evidence(
        self,
        user_id: str,
        concept_id: str,
        limit: int = 5,
    ) -> list[LearningEvidence]:
        """Fetch recent quiz/diagnostic signals for one user+concept."""
        return self.evidence_service.get_recent_evidence(
            user_id,
            concept_id,
            limit=limit,
        )
