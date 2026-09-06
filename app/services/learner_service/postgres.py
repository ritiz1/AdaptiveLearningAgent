from __future__ import annotations

from sqlalchemy.orm import Session, sessionmaker

from app.domain.learner import LearnerState, LearningProfile
from app.domain.mastery import MasterySnapshot, MasteryUpdate
from app.infrastructure.db.repositories import LearnerRepository
from app.services.learner_service.interface import LearnerService


class PostgresLearnerService(LearnerService):
    """Learner belief state backed by PostgreSQL.

    Holds a session factory rather than a session, so a single instance is
    safe to share across concurrent graph runs. Each method opens a
    short-lived session and closes it before returning.
    """

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def get_learner_state(self, user_id: str) -> LearnerState:
        with self._session_factory() as session:
            profile = LearnerRepository(session).get_profile(user_id)

        # An unseeded learner gets neutral defaults rather than an error,
        # matching how the hardcoded service treats unknown users.
        return LearnerState(
            user_id=user_id,
            profile=profile or LearningProfile(),
        )

    def get_mastery(self, user_id: str, concept_id: str) -> MasterySnapshot:
        with self._session_factory() as session:
            return LearnerRepository(session).get_mastery(user_id, concept_id)

    def update_mastery(self, user_id: str, update: MasteryUpdate) -> MasterySnapshot:
        raise NotImplementedError("Mastery updates arrive with the Phase 5 engine")

    def update_profile(self, user_id: str, profile: LearningProfile) -> LearningProfile:
        raise NotImplementedError("Profile updates arrive with Phase 7 inference")
