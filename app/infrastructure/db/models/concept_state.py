from __future__ import annotations

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class UserConceptState(Base):
    """Stored mastery belief for one learner and one concept."""

    __tablename__ = "user_concept_states"

    # Together, these form the composite primary key.
    user_id: Mapped[str] = mapped_column(
        String(128),
        primary_key=True,
    )
    concept_id: Mapped[str] = mapped_column(
        String(128),
        primary_key=True,
    )

    mastery_estimate: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    evidence_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    last_evidence_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    misconception_tags: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "mastery_estimate >= 0 AND mastery_estimate <= 1",
            name="ck_user_concept_mastery_range",
        ),
        CheckConstraint(
            "confidence >= 0 AND confidence <= 1",
            name="ck_user_concept_confidence_range",
        ),
        CheckConstraint(
            "evidence_count >= 0",
            name="ck_user_concept_evidence_count",
        ),
    )
