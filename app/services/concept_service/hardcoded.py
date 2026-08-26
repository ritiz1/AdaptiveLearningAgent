from __future__ import annotations

from typing import Optional

from app.domain.concepts import Concept, ConceptEdge, ConceptNeighborhood
from app.services.concept_service.interface import ConceptService


class HardcodedConceptService(ConceptService):
    """Temporary Phase 1B concept data stored in memory."""

    def __init__(self) -> None:
        self._concepts = {
            "python-functions": Concept(
                concept_id="python-functions",
                name="Python Functions",
            ),
            "call-stack": Concept(
                concept_id="call-stack",
                name="Call Stack",
            ),
            "python-recursion": Concept(
                concept_id="python-recursion",
                name="Python Recursion",
            ),
        }

        self._prerequisites = {
            "python-recursion": [
                "python-functions",
                "call-stack",
            ]
        }

    def resolve_concept(self, name_or_phrase: str) -> Concept:
        concept_id = "-".join(name_or_phrase.lower().strip().split())

        existing = self._concepts.get(concept_id)
        if existing is not None:
            return existing

        concept = Concept(
            concept_id=concept_id,
            name=name_or_phrase.strip(),
        )
        self._concepts[concept_id] = concept
        return concept

    def get_concept(self, concept_id: str) -> Optional[Concept]:
        return self._concepts.get(concept_id)

    def get_dependencies(
        self,
        concept_id: str,
        *,
        max_depth: int = 2,
    ) -> ConceptNeighborhood:
        target = self._concepts.get(concept_id)

        if target is None:
            target = Concept(
                concept_id=concept_id,
                name=concept_id,
            )

        prerequisite_ids = (
            self._prerequisites.get(concept_id, [])
            if max_depth >= 1
            else []
        )

        prerequisites = [
            self._concepts[item]
            for item in prerequisite_ids
            if item in self._concepts
        ]

        edges = [
            ConceptEdge(
                from_concept_id=item,
                to_concept_id=concept_id,
            )
            for item in prerequisite_ids
        ]

        return ConceptNeighborhood(
            target=target,
            prerequisites=prerequisites,
            edges=edges,
        )