from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class TeachingAction(str, Enum):
    """Allowed next teaching moves in the adaptive loop."""
    TEACH = "teach"
    DIAGNOSE = "diagnose"
    RETEACH = "reteach"
    PRACTICE = "practice"
    CONTINUE = "continue"
    END = "end"


@dataclass
class RoutingDecision:
    """Deterministic choice of what the graph should do next."""
    action: TeachingAction
    reason: Optional[str] = None
    target_concept_id: Optional[str] = None
