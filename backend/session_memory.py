from typing import Dict, List
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from system_prompts import get_system_message

session_store: Dict[str, List[BaseMessage]] = {}

MAX_MESSAGES = 20  # Prevent token explosion


def sanitize_history(history: List[BaseMessage]) -> List[BaseMessage]:
    """Remove orphaned ToolMessages that have no preceding AIMessage with tool_calls.
    OpenAI rejects requests where a ToolMessage isn't preceded by a tool_calls AIMessage.
    """
    clean = []
    for msg in history:
        if isinstance(msg, ToolMessage):
            # Only keep if the previous message is an AIMessage with tool_calls
            if clean and isinstance(clean[-1], AIMessage) and clean[-1].tool_calls:
                clean.append(msg)
            # Otherwise drop the orphaned ToolMessage silently
        else:
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
