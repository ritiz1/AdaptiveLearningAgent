from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class LearningEvidence:
    """One quiz/diagnostic/interaction signal used to update mastery later."""
    user_id: str
    concept_id: str
    evidence_type: str                     # quiz | diagnostic | interaction
    payload: dict[str, Any] = field(default_factory=dict)
    score: Optional[float] = None          # optional 0..1
    created_at: Optional[datetime] = None
