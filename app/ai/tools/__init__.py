# Original read-only service wrapper.
from .safe_reads import SAFE_READ_TOOL_NAMES, SafeReadTools

# LangChain tools that the Tutor LLM may call.
from .learner_tools import get_learner_state, get_mastery
from .concept_tools import get_dependencies
from .evidence_tools import get_recent_evidence


# This is the strict allow-list given to the Tutor LLM.
TUTOR_SAFE_TOOLS = [
    get_learner_state,
    get_mastery,
    get_dependencies,
    get_recent_evidence,
]


__all__ = [
    "SAFE_READ_TOOL_NAMES",
    "SafeReadTools",
    "get_learner_state",
    "get_mastery",
    "get_dependencies",
    "get_recent_evidence",
    "TUTOR_SAFE_TOOLS",
]