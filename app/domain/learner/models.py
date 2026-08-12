from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class KnowledgeState:
    """Belief about one concept for one learner (mastery + uncertainty)."""
    concept_id: str
    mastery_estimate: float = 0.0          # 0..1 estimated ability
    confidence: float = 0.0                # 0..1 trust in that estimate
    evidence_count: int = 0                # how many graded signals we have
    last_evidence_at: Optional[datetime] = None
    misconception_tags: list[str] = field(default_factory=list)


@dataclass
class LearningProfile:
    """Long-term preferences for how this learner likes explanations."""
    top_down: float = 0.5                  # prefers big-picture first
    example_first: float = 0.5             # prefers examples before theory
    causal_reasoning: float = 0.5          # prefers why/cause chains
    visual_structure: float = 0.5          # prefers structured/visual layout
    code_preference: float = 0.5           # prefers code-oriented teaching
    preferred_depth: str = "medium"        # shallow | medium | deep
    pacing: str = "normal"                 # slow | normal | fast


@dataclass
class BehaviorSignals:
    """Counts/patterns from past interactions used to update the profile."""
    asks_for_why: int = 0
    asks_for_examples: int = 0
    repeated_confusion_patterns: list[str] = field(default_factory=list)
    successful_explanation_strategies: list[str] = field(default_factory=list)


@dataclass
class LearnerState:
    """Per-turn learner snapshot loaded into GraphState for tutoring decisions."""
    user_id: str
    profile: LearningProfile = field(default_factory=LearningProfile)
    knowledge: list[KnowledgeState] = field(default_factory=list)
    behavior: BehaviorSignals = field(default_factory=BehaviorSignals)
