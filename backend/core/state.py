"""Session state management for TalentScout Streamlit application."""

from typing import Optional, Literal, Any
import streamlit as st
from core.config import config

# Conversation stages
ConversationStage = Literal["greeting", "collection", "questions", "exit"]

# Required fields for candidate information
REQUIRED_FIELDS = [
    "full_name",
    "email",
    "phone",
    "years_experience",
    "desired_position",
    "current_location",
    "tech_stack"
]


def initialize_session_state() -> None:
    """Initialize all session state variables if they don't exist."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "collected_fields" not in st.session_state:
        st.session_state.collected_fields = {}
    
    if "conversation_stage" not in st.session_state:
        st.session_state.conversation_stage: ConversationStage = "greeting"
    
    if "session_id" not in st.session_state:
        import uuid
        st.session_state.session_id = str(uuid.uuid4())
    
    if "questions_generated" not in st.session_state:
        st.session_state.questions_generated = False
    
    if "llm_messages" not in st.session_state:
        st.session_state.llm_messages = []


def add_message(role: str, content: str) -> None:
    """
    Add a message to chat history.
    
    Args:
        role: Message role ('user' or 'assistant')
        content: Message content
    """
    st.session_state.chat_history.append({"role": role, "content": content})


def get_chat_history() -> list[dict]:
    """Get the current chat history."""
    return st.session_state.chat_history


def update_field(field_name: str, value: Any) -> None:
    """
    Update a collected field.
    
    Args:
        field_name: Name of the field
        value: Field value
    """
    st.session_state.collected_fields[field_name] = value


def get_field(field_name: str) -> Optional[Any]:
    """
    Get a collected field value.
    
    Args:
        field_name: Name of the field
    
    Returns:
        Field value or None if not set
    """
    return st.session_state.collected_fields.get(field_name)


def get_all_fields() -> dict:
    """Get all collected fields."""
    return st.session_state.collected_fields.copy()


def is_field_collected(field_name: str) -> bool:
    """
    Check if a field has been collected.
    
    Args:
        field_name: Name of the field
    
    Returns:
        True if field is collected, False otherwise
    """
    return field_name in st.session_state.collected_fields and \
           st.session_state.collected_fields[field_name] is not None


def get_missing_fields() -> list[str]:
    """Get list of required fields that haven't been collected yet."""
    return [field for field in REQUIRED_FIELDS if not is_field_collected(field)]


def all_fields_collected() -> bool:
    """Check if all required fields have been collected."""
    return len(get_missing_fields()) == 0


def set_conversation_stage(stage: ConversationStage) -> None:
    """
    Set the current conversation stage.
    
    Args:
        stage: New conversation stage
    """
    st.session_state.conversation_stage = stage


def get_conversation_stage() -> ConversationStage:
    """Get the current conversation stage."""
    return st.session_state.conversation_stage


def check_exit_keyword(text: str) -> bool:
    """
    Check if the input text contains an exit keyword.
    
    Args:
        text: Input text to check
    
    Returns:
        True if exit keyword found, False otherwise
    """
    text_lower = text.lower().strip()
    return any(keyword in text_lower for keyword in config.EXIT_KEYWORDS)


def reset_session() -> None:
    """Reset the session state (clear all data)."""
    st.session_state.chat_history = []
    st.session_state.collected_fields = {}
    st.session_state.conversation_stage = "greeting"
    st.session_state.questions_generated = False
    st.session_state.llm_messages = []
    import uuid
    st.session_state.session_id = str(uuid.uuid4())


def add_llm_message(role: str, content: str) -> None:
    """
    Add a message to LLM conversation history.
    
    Args:
        role: Message role ('system', 'user', or 'assistant')
        content: Message content
    """
    st.session_state.llm_messages.append({"role": role, "content": content})


def get_llm_messages() -> list[dict]:
    """Get the LLM conversation history."""
    return st.session_state.llm_messages.copy()


def set_questions_generated(value: bool) -> None:
    """Set whether questions have been generated."""
    st.session_state.questions_generated = value


def are_questions_generated() -> bool:
    """Check if questions have been generated."""
    return st.session_state.questions_generated


def get_session_id() -> str:
    """Get the current session ID."""
    if "session_id" not in st.session_state:
        import uuid
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

