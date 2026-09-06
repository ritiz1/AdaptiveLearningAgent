"""
Database access for learner profiles and stored mastery.

This layer owns every SQLAlchemy query for learner data and returns
domain objects. Nodes, tools, and services must not query the ORM models
themselves.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.learner import LearningProfile
from app.domain.mastery import MasterySnapshot
from app.infrastructure.db.models import LearnerProfile, UserConceptState


class LearnerRepository:
    """Read learner rows from PostgreSQL as domain objects."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_profile(self, user_id: str) -> LearningProfile | None:
        """Return the stored profile, or None when the learner is unknown."""

        row = self._session.get(LearnerProfile, user_id)
        if row is None:
            return None

        return LearningProfile(
            top_down=row.top_down,
            example_first=row.example_first,
            causal_reasoning=row.causal_reasoning,
            visual_structure=row.visual_structure,
            code_preference=row.code_preference,
            preferred_depth=row.preferred_depth,
            pacing=row.pacing,
        )

    def get_mastery(self, user_id: str, concept_id: str) -> MasterySnapshot:
        """Return mastery for one concept.

        A missing row means we have never observed this learner on this
        concept, which is unknown rather than zero mastery.
        """

        row = self._session.get(UserConceptState, (user_id, concept_id))
        if row is None:
            return MasterySnapshot(
                concept_id=concept_id,
                mastery_estimate=0.0,
                confidence=0.0,
                evidence_count=0,
                is_unknown=True,
            )

        return MasterySnapshot(
            concept_id=row.concept_id,
            mastery_estimate=row.mastery_estimate,
            confidence=row.confidence,
            evidence_count=row.evidence_count,
            is_unknown=False,
        )
