"""Main chat layout components for TalentScout."""

import streamlit as st
from typing import Optional
from core.state import get_chat_history, add_message


def render_chat_interface() -> Optional[str]:
    """
    Render the main chat interface and return user input.
    
    Returns:
        User input text or None if no input
    """
    st.title("🤖 TalentScout AI Hiring Assistant")
    st.markdown("---")
    
    # Display chat history
    chat_history = get_chat_history()
    
    for message in chat_history:
        role = message.get("role", "user")
        content = message.get("content", "")
        
        with st.chat_message(role):
            st.markdown(content)
    
    # User input
    user_input = st.chat_input("Type your message here...")
    
    return user_input


def display_message(role: str, content: str) -> None:
    """
    Display a message in the chat interface.
    
    Args:
        role: Message role ('user' or 'assistant')
        content: Message content
    """
    with st.chat_message(role):
        st.markdown(content)
    
    # Add to chat history
    add_message(role, content)

