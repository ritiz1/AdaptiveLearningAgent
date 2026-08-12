from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Concept:
    """One teachable idea in the sparse concept registry."""
    concept_id: str
    name: str
    description: Optional[str] = None


@dataclass
class ConceptEdge:
    """Link between two concepts (usually prerequisite)."""
    from_concept_id: str
    to_concept_id: str
    relation: str = "prerequisite"         # prerequisite | related


@dataclass
class ConceptNeighborhood:
    """Small local prerequisite slice for the current target concept."""
    target: Concept
    prerequisites: list[Concept] = field(default_factory=list)
    edges: list[ConceptEdge] = field(default_factory=list)
