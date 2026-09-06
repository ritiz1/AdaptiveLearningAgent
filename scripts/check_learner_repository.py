"""
Verify that seeded PostgreSQL data is readable through both layers:
the repository directly, and the configured learner service.

Run from the project root:

    python -m scripts.check_learner_repository
"""

from __future__ import annotations

from app.infrastructure.db.engine import get_session_factory
from app.infrastructure.db.repositories import LearnerRepository
from app.services.container import get_learner_service


def check_repository() -> None:
    print("--- repository ---")
    with get_session_factory()() as session:
        repo = LearnerRepository(session)

        print("user-a profile:", repo.get_profile("user-a"))
        print("user-b profile:", repo.get_profile("user-b"))
        print("unknown user   :", repo.get_profile("does-not-exist"))
        print("missing mastery:", repo.get_mastery("user-a", "recursion"))


def check_service() -> None:
    service = get_learner_service()

    print(f"--- service ({type(service).__name__}) ---")
    print("user-a state   :", service.get_learner_state("user-a"))
    print("user-b state   :", service.get_learner_state("user-b"))
    print("unknown user   :", service.get_learner_state("does-not-exist"))
    print("missing mastery:", service.get_mastery("user-a", "recursion"))


if __name__ == "__main__":
    check_repository()
    print()
    check_service()
