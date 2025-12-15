"""Main Streamlit application for TalentScout AI Hiring Assistant."""

import streamlit as st
from core.state import (
    initialize_session_state,
    check_exit_keyword,
    get_conversation_stage,
    set_conversation_stage,
    get_missing_fields,
    all_fields_collected,
    get_field,
    update_field,
    get_all_fields,
    are_questions_generated,
    set_questions_generated,
    add_llm_message,
    get_llm_messages,
    get_session_id
)
from core.validators import (
    validate_full_name,
    validate_email,
    validate_phone,
    validate_years_experience,
    validate_tech_stack,
    validate_desired_position,
    validate_current_location
)
from core.llm import get_llm_provider
from core.prompts import (
    get_system_prompt,
    get_info_collection_prompt,
    get_greeting_message,
    get_exit_handler,
    get_fallback_prompt
)
from core.question_bank import generate_questions, format_questions_for_display
from core.storage import save_session
from core.config import config
from core.logging_utils import logger
from ui.layout import render_chat_interface, display_message
from ui.widgets import render_sidebar

# Page configuration
st.set_page_config(
    page_title="TalentScout AI Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Render sidebar
render_sidebar()

# Main chat interface
user_input = render_chat_interface()

# Handle conversation flow
if user_input:
    # Check for exit keywords
    if check_exit_keyword(user_input):
        exit_message = get_exit_handler()
        display_message("assistant", exit_message)
        set_conversation_stage("exit")
        st.rerun()
    
    # Add user message to chat
    display_message("user", user_input)
    
    # Get conversation stage
    stage = get_conversation_stage()
    
    # Initialize LLM provider
    llm_provider = get_llm_provider()
    
    if not llm_provider.is_available():
        display_message(
            "assistant",
            "⚠️ Error: LLM provider is not available. Please check your API keys in the .env file."
        )
        st.stop()
    
    # Handle greeting stage
    if stage == "greeting":
        greeting = get_greeting_message()
        display_message("assistant", greeting)
        add_llm_message("system", get_system_prompt())
        add_llm_message("assistant", greeting)
        set_conversation_stage("collection")
        st.rerun()
    
    # Handle collection stage
    elif stage == "collection":
        missing_fields = get_missing_fields()
        
        if not missing_fields:
            # All fields collected, move to questions
            if not are_questions_generated():
                # Generate questions
                tech_stack = get_field("tech_stack")
                if tech_stack:
                    with st.spinner("Generating tailored technical questions..."):
                        questions = generate_questions(tech_stack)
                        
                        if questions:
                            questions_text = format_questions_for_display(questions)
                            response = f"Great! I have all the information I need. Here are your tailored technical questions:\n\n{questions_text}\n\nPlease answer these questions to the best of your ability."
                            display_message("assistant", response)
                            add_llm_message("assistant", response)
                            set_questions_generated(True)
                            set_conversation_stage("questions")
                        else:
                            display_message(
                                "assistant",
                                "I apologize, but I encountered an error generating questions. Please try again later."
                            )
                    st.rerun()
            else:
                # Questions already generated, continue conversation
                _handle_collection_or_questions(user_input, llm_provider)
        else:
            # Still collecting fields
            _handle_field_collection(user_input, missing_fields, llm_provider)
    
    # Handle questions stage
    elif stage == "questions":
        _handle_collection_or_questions(user_input, llm_provider)
    
    # Handle exit stage
    elif stage == "exit":
        display_message("assistant", "Thank you for using TalentScout. Have a great day!")
        st.rerun()


def _handle_field_collection(user_input: str, missing_fields: list[str], llm_provider) -> None:
    """
    Handle field collection from user input.
    
    Args:
        user_input: User's input text
        missing_fields: List of fields still needed
        llm_provider: LLM provider instance
    """
    next_field = missing_fields[0]
    
    # Validate and store field
    validation_result = _validate_and_store_field(next_field, user_input)
    
    if validation_result["valid"]:
        # Field validated and stored
        confirmation = validation_result.get("confirmation", f"Got it! {user_input}")
        display_message("assistant", confirmation)
        add_llm_message("assistant", confirmation)
        
        # Check if all fields collected
        if all_fields_collected():
            # Summarize collected information
            fields = get_all_fields()
            summary = _create_fields_summary(fields)
            display_message("assistant", summary)
            add_llm_message("assistant", summary)
            set_conversation_stage("collection")  # Will trigger question generation
        else:
            # Ask for next field
            next_missing = get_missing_fields()[0]
            next_question = _get_field_prompt(next_missing)
            display_message("assistant", next_question)
            add_llm_message("assistant", next_question)
    else:
        # Validation failed
        error_msg = validation_result.get("error", "Invalid input. Please try again.")
        next_question = _get_field_prompt(next_field)
        response = f"{error_msg}\n\n{next_question}"
        display_message("assistant", response)
        add_llm_message("assistant", response)
    
    st.rerun()


def _validate_and_store_field(field_name: str, value: str) -> dict:
    """
    Validate and store a field value.
    
    Args:
        field_name: Name of the field
        value: Field value to validate and store
    
    Returns:
        Dictionary with validation result
    """
    if field_name == "full_name":
        is_valid, error = validate_full_name(value)
        if is_valid:
            update_field("full_name", value)
            return {"valid": True, "confirmation": f"Thank you, {value}!"}
        return {"valid": False, "error": error}
    
    elif field_name == "email":
        is_valid, error = validate_email(value)
        if is_valid:
            update_field("email", value)
            return {"valid": True, "confirmation": f"Email recorded: {value}"}
        return {"valid": False, "error": error}
    
    elif field_name == "phone":
        is_valid, error = validate_phone(value)
        if is_valid:
            update_field("phone", value)
            return {"valid": True, "confirmation": f"Phone number recorded: {value}"}
        return {"valid": False, "error": error}
    
    elif field_name == "years_experience":
        is_valid, error, normalized = validate_years_experience(value)
        if is_valid:
            update_field("years_experience", normalized)
            return {"valid": True, "confirmation": f"Experience recorded: {normalized} years"}
        return {"valid": False, "error": error}
    
    elif field_name == "desired_position":
        is_valid, error = validate_desired_position(value)
        if is_valid:
            update_field("desired_position", value)
            return {"valid": True, "confirmation": f"Desired position recorded: {value}"}
        return {"valid": False, "error": error}
    
    elif field_name == "current_location":
        is_valid, error = validate_current_location(value)
        if is_valid:
            update_field("current_location", value)
            return {"valid": True, "confirmation": f"Location recorded: {value}"}
        return {"valid": False, "error": error}
    
    elif field_name == "tech_stack":
        is_valid, error, normalized = validate_tech_stack(value)
        if is_valid:
            update_field("tech_stack", normalized)
            stack_str = ", ".join(normalized)
            return {"valid": True, "confirmation": f"Tech stack recorded: {stack_str}"}
        return {"valid": False, "error": error}
    
    return {"valid": False, "error": "Unknown field"}


def _get_field_prompt(field_name: str) -> str:
    """
    Get the prompt for asking about a field.
    
    Args:
        field_name: Name of the field
    
    Returns:
        Prompt text
    """
    prompts = {
        "full_name": "What's your full name?",
        "email": "What's your email address?",
        "phone": "What's your phone number?",
        "years_experience": "How many years of professional experience do you have?",
        "desired_position": "What position(s) are you interested in?",
        "current_location": "What's your current location?",
        "tech_stack": "What's your tech stack? Please list languages, frameworks, databases, and tools (e.g., Python, Django, PostgreSQL, Docker)."
    }
    return prompts.get(field_name, f"Please provide your {field_name.replace('_', ' ')}.")


def _create_fields_summary(fields: dict) -> str:
    """
    Create a summary of collected fields.
    
    Args:
        fields: Dictionary of collected fields
    
    Returns:
        Summary text
    """
    summary_parts = ["Perfect! Here's a summary of the information I've collected:\n"]
    
    if fields.get("full_name"):
        summary_parts.append(f"• **Name:** {fields['full_name']}")
    if fields.get("email"):
        summary_parts.append(f"• **Email:** {fields['email']}")
    if fields.get("years_experience"):
        summary_parts.append(f"• **Experience:** {fields['years_experience']} years")
    if fields.get("desired_position"):
        summary_parts.append(f"• **Desired Position:** {fields['desired_position']}")
    if fields.get("current_location"):
        summary_parts.append(f"• **Location:** {fields['current_location']}")
    if fields.get("tech_stack"):
        stack_str = ", ".join(fields['tech_stack']) if isinstance(fields['tech_stack'], list) else fields['tech_stack']
        summary_parts.append(f"• **Tech Stack:** {stack_str}")
    
    summary_parts.append("\nNow I'll generate some tailored technical questions based on your tech stack...")
    
    return "\n".join(summary_parts)


def _handle_collection_or_questions(user_input: str, llm_provider) -> None:
    """
    Handle user input during collection or questions stage using LLM.
    
    Args:
        user_input: User's input text
        llm_provider: LLM provider instance
    """
    # Add user message to LLM history
    add_llm_message("user", user_input)
    
    # Get LLM messages
    messages = get_llm_messages()
    
    # Ensure system prompt is first
    if not messages or messages[0].get("role") != "system":
        messages = [{"role": "system", "content": get_system_prompt()}] + messages
    
    # Generate response
    with st.spinner("Thinking..."):
        response = llm_provider.generate_response(
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
    
    if response:
        display_message("assistant", response)
        add_llm_message("assistant", response)
        
        # Save session if storage is enabled
        if config.ENABLE_STORAGE and all_fields_collected():
            try:
                fields = get_all_fields()
                tech_stack = fields.get("tech_stack", [])
                if isinstance(tech_stack, str):
                    tech_stack = [tech_stack]
                
                save_session(
                    session_id=get_session_id(),
                    collected_fields=fields,
                    tech_stack=tech_stack,
                    answers=[],  # Could collect answers if needed
                    sentiment_log=[]
                )
            except Exception as e:
                logger.error(f"Error saving session: {e}")
    else:
        display_message(
            "assistant",
            "I apologize, but I encountered an error processing your request. Please try again."
        )
    
    st.rerun()


# Initialize greeting on first load
if get_conversation_stage() == "greeting":
    if not st.session_state.get("greeting_shown", False):
        st.session_state.greeting_shown = True
        greeting = get_greeting_message()
        display_message("assistant", greeting)
        add_llm_message("system", get_system_prompt())
        add_llm_message("assistant", greeting)
        set_conversation_stage("collection")
        st.rerun()

