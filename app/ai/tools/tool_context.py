"""
Create the services used by the Phase 1B read-only tools.

The hardcoded services are temporary. Later, database-backed services
can replace them without changing the LLM tool functions.
"""

from app.ai.tools.safe_reads import SafeReadTools
from app.services.concept_service import HardcodedConceptService
from app.services.evidence_service import HardcodedEvidenceService
from app.services.learner_service.hardcoded import HardcodedLearnerService


# Create one shared instance of each temporary service.
learner_service = HardcodedLearnerService()
concept_service = HardcodedConceptService()
evidence_service = HardcodedEvidenceService()


# SafeReadTools provides one controlled, read-only access layer.
# The LLM will not receive direct write access to these services.
safe_reads = SafeReadTools(
    learner_service=learner_service,
    concept_service=concept_service,
    evidence_service=evidence_service,
)