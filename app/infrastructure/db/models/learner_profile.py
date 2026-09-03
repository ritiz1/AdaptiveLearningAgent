from sqlalchemy import Float, String 
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.db.base import Base

class LearnerProfile(Base):
    """ Database representation of a learner profile """ 
    __tablename__ = "learner_profiles"
    user_id: Mapped[str] = mapped_column(
        String(128), 
        primary_key=True,
    )
    top_down: Mapped[float] = mapped_column(Float, default=0.5)
    example_first: Mapped[float] = mapped_column(Float, default=0.5)
    causal_reasoning: Mapped[float] = mapped_column(Float, default=0.5)
    visual_structure: Mapped[float] = mapped_column(Float, default=0.5)
    code_preference: Mapped[float] = mapped_column(Float, default=0.5)

    preferred_depth: Mapped[str] = mapped_column(
        String(20),
        default="medium",
    )

    pacing: Mapped[str] = mapped_column(
        String(20),
        default="normal",
    )

    



