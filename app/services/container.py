"""
Composition root for the service layer.

Nodes and tools resolve services here instead of constructing their own, so
every part of a turn reads from the same backend. Providers are lazy and
cached: importing this module touches neither the database nor the network.

The learner backend is selected by the LEARNER_BACKEND environment variable:

    postgres    read learner data from PostgreSQL (default)
    hardcoded   fall back to the in-code Phase 1 data
"""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv

from app.services.concept_service import ConceptService, HardcodedConceptService
from app.services.evidence_service import EvidenceService, HardcodedEvidenceService
from app.services.learner_service import LearnerService
from app.services.learner_service.hardcoded import HardcodedLearnerService

LEARNER_BACKEND_ENV = "LEARNER_BACKEND"
DEFAULT_LEARNER_BACKEND = "postgres"


def _learner_backend() -> str:
    load_dotenv("app/.env")
    return os.getenv(LEARNER_BACKEND_ENV, DEFAULT_LEARNER_BACKEND).strip().lower()


@lru_cache(maxsize=1)
def get_learner_service() -> LearnerService:
    """Return the configured learner service."""

    backend = _learner_backend()

    if backend == "hardcoded":
        return HardcodedLearnerService()

    if backend == "postgres":
        # Imported here so the hardcoded path never requires database config.
        from app.infrastructure.db.engine import get_session_factory
        from app.services.learner_service.postgres import PostgresLearnerService

        return PostgresLearnerService(get_session_factory())

    raise ValueError(
        f"Unknown {LEARNER_BACKEND_ENV}={backend!r}. Use 'postgres' or 'hardcoded'."
    )


@lru_cache(maxsize=1)
def get_concept_service() -> ConceptService:
    """Return the concept service.

    Still hardcoded: the concepts and concept_edges tables do not exist yet.
    """

    return HardcodedConceptService()


@lru_cache(maxsize=1)
def get_evidence_service() -> EvidenceService:
    """Return the evidence service.

    Still hardcoded: the learning_evidence table does not exist yet.
    """

    return HardcodedEvidenceService()


def reset_services() -> None:
    """Clear the cached services so tests can switch backends."""

    get_learner_service.cache_clear()
    get_concept_service.cache_clear()
    get_evidence_service.cache_clear()
