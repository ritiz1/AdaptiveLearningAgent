from __future__ import annotations

from datetime import datetime, timezone

from app.domain.evidence import LearningEvidence
from app.services.evidence_service.interface import EvidenceService


class HardcodedEvidenceService(EvidenceService):
    """Temporary in-memory evidence storage for Phase 1B."""

    def __init__(self) -> None:
        self._evidence: list[LearningEvidence] = []

    def save_evidence(
        self,
        evidence: LearningEvidence,
    ) -> LearningEvidence:
        if evidence.created_at is None:
            evidence.created_at = datetime.now(timezone.utc)

        self._evidence.append(evidence)
        return evidence

    def get_recent_evidence(
        self,
        user_id: str,
        concept_id: str,
        *,
        limit: int = 5,
    ) -> list[LearningEvidence]:
        matches = [
            evidence
            for evidence in self._evidence
            if evidence.user_id == user_id
            and evidence.concept_id == concept_id
        ]

        return list(reversed(matches))[:limit]