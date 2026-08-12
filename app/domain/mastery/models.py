from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class MasterySnapshot:
    """Read-only view of mastery used for routing/diagnostics."""
    concept_id: str
    mastery_estimate: float
    confidence: float
    evidence_count: int
    is_unknown: bool = False               # True if no stored record exists


@dataclass
class MasteryUpdate:
    """Proposed mastery change; deterministic code applies and persists it."""
    concept_id: str
    mastery_delta: float
    confidence_delta: float
    misconception_tags: Optional[list[str]] = None
