from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.evidence import LearningEvidence


class EvidenceService(ABC):
    """Store and read learning evidence. Writes stay deterministic (not LLM)."""

    @abstractmethod
    def save_evidence(self, evidence: LearningEvidence) -> LearningEvidence:
        """Persist one evidence record after validation."""
        raise NotImplementedError

    @abstractmethod
    def get_recent_evidence(
        self,
        user_id: str,
        concept_id: str,
        *,
        limit: int = 5,
    ) -> list[LearningEvidence]:
        """Return recent evidence for one user+concept (newest first)."""
        raise NotImplementedError
