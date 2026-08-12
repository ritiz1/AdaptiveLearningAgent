from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.concepts import Concept, ConceptNeighborhood


class ConceptService(ABC):
    """Resolve/create concepts and fetch local prerequisite neighborhoods."""

    @abstractmethod
    def resolve_concept(self, name_or_phrase: str) -> Concept:
        """Map user text to a canonical concept; create lazily if missing."""
        raise NotImplementedError

    @abstractmethod
    def get_concept(self, concept_id: str) -> Optional[Concept]:
        """Fetch one concept by id, or None if it does not exist."""
        raise NotImplementedError

    @abstractmethod
    def get_dependencies(
        self,
        concept_id: str,
        *,
        max_depth: int = 2,
    ) -> ConceptNeighborhood:
        """Return a small local prerequisite neighborhood (depth-capped)."""
        raise NotImplementedError
