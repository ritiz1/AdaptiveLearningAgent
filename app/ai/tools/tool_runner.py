from __future__ import annotations

import json
from collections.abc import Sequence
from typing import Any

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
from langchain_core.tools import BaseTool

import logging 
logger = logging.getLogger(__name__)


def run_tool_loop(
    *,
    messages: list[BaseMessage],
    tool_enabled_llm: Any,
    fallback_llm: Any,
    tools: Sequence[BaseTool],
    max_rounds: int = 2,
) -> str:
    """
    Run an LLM with a bounded read-only tool loop.

    The LLM may answer immediately or request approved tools.
    No more than `max_rounds` tool rounds are allowed.
    """

    # Copy the messages so we do not modify the caller's list.
    conversation = list(messages)

    # Create a lookup such as:
    # {"get_mastery": <tool>, "get_dependencies": <tool>}
    tools_by_name = {
        tool.name: tool
        for tool in tools
    }

    # The first LLM call may answer directly or request tools.
    response = tool_enabled_llm.invoke(conversation)

    for _ in range(max_rounds):
        # No tool requests means the response is final.
        if not response.tool_calls:
            return str(response.content)

        # Preserve the AI message containing its tool requests.
        conversation.append(response)

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]

            selected_tool = tools_by_name.get(tool_name)

            # The model should only request bound tools, but we still
            # validate the name as a safety guard.
            if selected_tool is None:
                result = {
                    "error": f"Tool '{tool_name}' is not allowed."
                }
            else:
                try:
                    logger.info(f"Running tool: {tool_name} with args: {tool_args}")
                    # Run the approved Python tool.
                    result = selected_tool.invoke(tool_args)
                except Exception:
                    # Return a controlled error instead of crashing
                    # the entire tutoring workflow.
                    result = {
                        "error": f"Tool '{tool_name}' failed."
                    }

            # Send the result back to the exact tool request.
            conversation.append(
                ToolMessage(
                    content=json.dumps(result, default=str),
                    tool_call_id=tool_call_id,
                )
            )

        # Let the LLM interpret the returned tool results.
        response = tool_enabled_llm.invoke(conversation)

    # The two-round limit was reached and another tool was requested.
    # Do not execute it. Ask the non-tool LLM to answer using data
    # collected during the approved rounds.
    if response.tool_calls:
        conversation.append(
            HumanMessage(
                content=(
                    "The tool-call limit has been reached. "
                    "Answer using the information already available."
                )
            )
        )
        response = fallback_llm.invoke(conversation)

    return str(response.content)