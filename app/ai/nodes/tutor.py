from __future__ import annotations

from app.ai.graph.state import WorkflowState

from langchain_core.messages import HumanMessage, SystemMessage 

from app.ai.graph.state import WorkflowState
from app.domain.learner import LearningProfile 
from app.infrastructure.llm.client import get_llm

from app.ai.tools import TUTOR_SAFE_TOOLS
from app.ai.tools.tool_runner import run_tool_loop


llm = get_llm()
#binding the tools to the llm so that it can use them.
tool_enabled_llm = llm.bind_tools(TUTOR_SAFE_TOOLS)

def build_teaching_strategy(profile: LearningProfile) -> str:
    instructions = []

    if profile.example_first > profile.top_down:
        instructions.append(
            "Start with one short concrete example."
        )
    else:
        instructions.append(
            "Start with a two-sentence big-picture explanation."
        )

    if profile.code_preference >= 0.7:
        instructions.append(
            "Include at most one small code snippet."
        )

    if profile.causal_reasoning >= 0.7:
        instructions.append(
            "Briefly explain why the current idea works."
        )

    word_limits = {
        "shallow": 120,
        "medium": 170,
        "deep": 220,
    }
    word_limit = word_limits.get(profile.preferred_depth, 170)

    instructions.append(
        f"Keep the entire response below {word_limit} words."
    )
    instructions.append(
        "Teach only one small part of the concept in this turn."
    )

    return "\n".join(f"- {item}" for item in instructions)





def tutor_node(state: WorkflowState)-> dict: 
    learner_state = state.get("learner_state")
    if learner_state is None:
        raise ValueError("Learner state most be loaded before tutoring")

    strategy = build_teaching_strategy(learner_state.profile)


    messages = [
        SystemMessage(
            content=(
                "You are a conversational adaptive tutor, not a textbook writer.\n\n"
                "Rules:\n"
                "- Teach exactly one manageable idea per response.\n"
                "- Never provide a complete chapter or exhaustive guide.\n"
                "- Use no more than three short sections.\n"
                "- Include at most one example.\n"
                "- End with one short question that checks understanding.\n"
                "- Use the approved read-only tools only when extra learner "
                "context would improve your answer.\n"
                "- Never request a write or state mutation.\n\n"
                "Personalization instructions:\n"
                f"{strategy}\n\n"
                "Do not mention tools, learner profiles, or internal instructions."
            )
        ),
        HumanMessage(
            content=(
                f"User ID: {state['user_id']}\n"
                f"Learner request: {state['user_message']}\n"
                f"Intent: {state['intent']}\n"
                f"Target concept: {state['target_concept']}"
            )
        ),
    ]

    response_content = run_tool_loop(
        messages=messages,
        tool_enabled_llm=tool_enabled_llm,
        fallback_llm=llm,
        tools=TUTOR_SAFE_TOOLS,
        max_rounds=2,
    )

    return {
        "tutor_response": response_content,
    }

