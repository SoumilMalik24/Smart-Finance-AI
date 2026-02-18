from typing import Dict, List
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from system_prompts import get_system_message

session_store: Dict[str, List[BaseMessage]] = {}

MAX_MESSAGES = 20  # Prevent token explosion


def sanitize_history(history: List[BaseMessage]) -> List[BaseMessage]:
    """Ensure every AIMessage with tool_calls has ALL its ToolMessages, and
    every ToolMessage has a preceding AIMessage with tool_calls.

    OpenAI throws 400 errors in both directions:
    - AIMessage with tool_calls not followed by matching ToolMessages
    - ToolMessage not preceded by an AIMessage with tool_calls
    """
    # Pass 1: find all tool_call_ids that have a ToolMessage response
    responded_ids: set = set()
    for msg in history:
        if isinstance(msg, ToolMessage):
            responded_ids.add(msg.tool_call_id)

    # Pass 2: rebuild history, skipping broken groups
    clean = []
    last_tool_ai: AIMessage | None = None  # track last AIMessage with tool_calls

    for msg in history:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            # Only keep if ALL tool_calls have a matching ToolMessage response
            all_responded = all(tc["id"] in responded_ids for tc in msg.tool_calls)
            if all_responded:
                clean.append(msg)
                last_tool_ai = msg
            else:
                last_tool_ai = None  # drop this group
        elif isinstance(msg, ToolMessage):
            # Only keep if there's a valid preceding AIMessage with tool_calls
            if last_tool_ai is not None:
                clean.append(msg)
            # else: orphaned ToolMessage — drop it
        else:
            last_tool_ai = None  # reset on any non-tool message
            clean.append(msg)
    return clean


def get_session_history(session_id: str) -> List[BaseMessage]:
    if session_id not in session_store:
        session_store[session_id] = [get_system_message()]
    return sanitize_history(session_store[session_id])


def append_to_session(session_id: str, message: BaseMessage):
    if session_id not in session_store:
        session_store[session_id] = [get_system_message()]

    session_store[session_id].append(message)
    trim_history(session_id)


def trim_history(session_id: str):
    history = session_store[session_id]

    if len(history) > MAX_MESSAGES:
        system_msg = history[0]
        trimmed = [system_msg] + history[-(MAX_MESSAGES - 1):]
        # Sanitize after trimming to remove any newly orphaned ToolMessages
        session_store[session_id] = sanitize_history(trimmed)


def clear_session(session_id: str):
    if session_id in session_store:
        del session_store[session_id]
