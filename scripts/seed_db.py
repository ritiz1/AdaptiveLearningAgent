"""
Seed the learner_profiles table with the Phase 1 example learners.

Profile values come from HardcodedLearnerService so there is a single
source of truth while the hardcoded services are still in use.

Run from the project root:

    python -m scripts.seed_db
"""

from __future__ import annotations

from app.infrastructure.db.engine import get_session_factory
from app.infrastructure.db.models import LearnerProfile
from app.services.learner_service.hardcoded import HardcodedLearnerService


SEED_USER_IDS = ["user-a", "user-b"]


def seed_learner_profiles() -> None:
    """Insert the seed learners, skipping any that already exist."""

    learner_service = HardcodedLearnerService()

    with get_session_factory()() as session:
        for user_id in SEED_USER_IDS:
            if session.get(LearnerProfile, user_id) is not None:
                print(f"skip   {user_id} (already present)")
                continue

            profile = learner_service.get_learner_state(user_id).profile
            session.add(
                LearnerProfile(
                    user_id=user_id,
                    top_down=profile.top_down,
                    example_first=profile.example_first,
                    causal_reasoning=profile.causal_reasoning,
                    visual_structure=profile.visual_structure,
                    code_preference=profile.code_preference,
                    preferred_depth=profile.preferred_depth,
                    pacing=profile.pacing,
                )
            )
            print(f"insert {user_id}")

        session.commit()


if __name__ == "__main__":
    seed_learner_profiles()
    print("Seeding complete.")
