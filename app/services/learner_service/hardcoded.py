from app.domain.learner import LearnerState, LearningProfile
from app.domain.mastery import MasterySnapshot, MasteryUpdate
from app.services.learner_service.interface import LearnerService


class HardcodedLearnerService(LearnerService):
    """ Temporary hardcoded phase1 learner data stored in code """  
    
    def get_learner_state(self, user_id: str) -> LearnerState:
        if user_id == "user-a":
            profile = LearningProfile(
                top_down=0.2,
                example_first=0.9,
                causal_reasoning=0.4,
                visual_structure=0.7,
                code_preference=0.3,
                preferred_depth="shallow",
                pacing="slow",
            )
        elif user_id == "user-b":
            profile = LearningProfile(
                top_down=0.9,
                example_first=0.3,
                causal_reasoning=0.8,
                visual_structure=0.5,
                code_preference=0.9,
                preferred_depth="deep",
                pacing="fast",
            )
        else:
            profile = LearningProfile()
        return LearnerState(
            user_id=user_id,
            profile = profile
        )


    def get_mastery(
        self,
        user_id: str,
        concept_id: str,
    ) -> MasterySnapshot:
        return MasterySnapshot(
            concept_id=concept_id,
            mastery_estimate=0.0,
            confidence=0.0,
            evidence_count=0,
            is_unknown=True,
        )

    def update_mastery(
    self,
    user_id: str,
    update: MasteryUpdate,
) -> MasterySnapshot:
     raise NotImplementedError("Mastery updates are not part of Phase 1")



    def update_profile(
        self,
        user_id: str,
        profile: LearningProfile,
    ) -> LearningProfile:
        raise NotImplementedError("Profile updates are not part of Phase 1")

