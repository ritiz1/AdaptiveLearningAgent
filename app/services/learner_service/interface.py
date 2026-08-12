from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.learner import LearnerState, LearningProfile
from app.domain.mastery import MasterySnapshot, MasteryUpdate


class LearnerService(ABC):
    """Load/update learner belief state. Nodes call this, not the DB directly."""

    @abstractmethod
    def get_learner_state(self, user_id: str) -> LearnerState:
        """Return profile + known knowledge slice for this user."""
        raise NotImplementedError

    @abstractmethod
    def get_mastery(self, user_id: str, concept_id: str) -> MasterySnapshot:
        """Return mastery for one concept. Unknown => is_unknown=True."""
        raise NotImplementedError

    @abstractmethod
    def update_mastery(self, user_id: str, update: MasteryUpdate) -> MasterySnapshot:
        """Apply a validated mastery update and return the new snapshot."""
        raise NotImplementedError

    @abstractmethod
    def update_profile(self, user_id: str, profile: LearningProfile) -> LearningProfile:
        """Persist long-term learning-preference updates."""
        raise NotImplementedError
