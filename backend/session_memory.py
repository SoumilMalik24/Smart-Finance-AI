from typing import Dict, List
from langchain_core.messages import BaseMessage
from system_prompts import get_system_message

session_store: Dict[str, List[BaseMessage]] = {}

MAX_MESSAGES = 20  # Prevent token explosion


def get_session_history(session_id: str) -> List[BaseMessage]:
    if session_id not in session_store:
        session_store[session_id] = [get_system_message()]
    return session_store[session_id]


def append_to_session(session_id: str, message: BaseMessage):
    if session_id not in session_store:
        session_store[session_id] = [get_system_message()]

    session_store[session_id].append(message)
    trim_history(session_id)


def trim_history(session_id: str):
    history = session_store[session_id]

    if len(history) > MAX_MESSAGES:
        system_msg = history[0]
        session_store[session_id] = [system_msg] + history[-(MAX_MESSAGES - 1):]


def clear_session(session_id: str):
    if session_id in session_store:
        del session_store[session_id]
