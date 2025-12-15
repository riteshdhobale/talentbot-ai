"""FastAPI backend for TalentScout - API endpoints for frontend integration."""

from core.logging_utils import logger
from core.config import config
from core.storage import save_session
from core.question_bank import generate_questions
from core.prompts import (
    get_system_prompt,
    get_greeting_message,
    get_exit_handler,
    get_fallback_prompt
)
from core.llm import get_llm_provider
from core.validators import (
    validate_full_name,
    validate_email,
    validate_phone,
    validate_years_experience,
    validate_tech_stack,
    validate_desired_position,
    validate_current_location
)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))


app = FastAPI(title="TalentScout API", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage (replace with database in production)
sessions: Dict[str, Dict[str, Any]] = {}


# Request/Response Models
class SessionCreate(BaseModel):
    """Create a new session."""
    pass


class MessageRequest(BaseModel):
    """Send a message to the chatbot."""
    session_id: str
    message: str


class FieldUpdate(BaseModel):
    """Update a specific field."""
    session_id: str
    field_name: str
    field_value: str


class SessionResponse(BaseModel):
    """Session information response."""
    session_id: str
    conversation_stage: str
    collected_fields: Dict[str, Any]
    missing_fields: List[str]
    chat_history: List[Dict[str, str]]


class MessageResponse(BaseModel):
    """Message response."""
    response: str
    conversation_stage: str
    fields_collected: Dict[str, Any]
    missing_fields: List[str]
    questions: Optional[List[Dict[str, str]]] = None


class QuestionGenerationRequest(BaseModel):
    """Request to generate questions."""
    session_id: str


# Helper functions
def get_or_create_session(session_id: str) -> Dict[str, Any]:
    """Get or create a session."""
    if session_id not in sessions:
        sessions[session_id] = {
            "session_id": session_id,
            "conversation_stage": "greeting",
            "collected_fields": {},
            "chat_history": [],
            "llm_messages": [],
            "questions_generated": False,
            "created_at": datetime.now().isoformat()
        }
    return sessions[session_id]


def check_exit_keyword(text: str) -> bool:
    """Check if text contains exit keyword."""
    text_lower = text.lower().strip()
    return any(keyword in text_lower for keyword in config.EXIT_KEYWORDS)


# API Endpoints
@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "TalentScout API", "version": "1.0.0"}


@app.post("/api/sessions", response_model=SessionResponse)
def create_session():
    """Create a new session."""
    session_id = str(uuid.uuid4())
    session = get_or_create_session(session_id)

    # Initialize greeting
    greeting = get_greeting_message()
    session["chat_history"].append({"role": "assistant", "content": greeting})
    session["llm_messages"].append(
        {"role": "system", "content": get_system_prompt()})
    session["llm_messages"].append({"role": "assistant", "content": greeting})
    session["conversation_stage"] = "collection"

    return SessionResponse(
        session_id=session_id,
        conversation_stage=session["conversation_stage"],
        collected_fields=session["collected_fields"],
        missing_fields=_get_missing_fields(session),
        chat_history=session["chat_history"]
    )


@app.get("/api/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: str):
    """Get session information."""
    session = get_or_create_session(session_id)
    return SessionResponse(
        session_id=session_id,
        conversation_stage=session["conversation_stage"],
        collected_fields=session["collected_fields"],
        missing_fields=_get_missing_fields(session),
        chat_history=session["chat_history"]
    )


@app.post("/api/message", response_model=MessageResponse)
def send_message(request: MessageRequest):
    """Send a message and get response."""
    session = get_or_create_session(request.session_id)

    # Check for exit keywords
    if check_exit_keyword(request.message):
        exit_msg = get_exit_handler()
        session["chat_history"].append(
            {"role": "user", "content": request.message})
        session["chat_history"].append(
            {"role": "assistant", "content": exit_msg})
        session["conversation_stage"] = "exit"

        return MessageResponse(
            response=exit_msg,
            conversation_stage="exit",
            fields_collected=session["collected_fields"],
            missing_fields=[]
        )

    # Add user message
    session["chat_history"].append(
        {"role": "user", "content": request.message})

    stage = session["conversation_stage"]
    llm_provider = get_llm_provider()

    if not llm_provider.is_available():
        raise HTTPException(
            status_code=500, detail="LLM provider not available")

    # Handle collection stage
    if stage == "collection":
        missing_fields = _get_missing_fields(session)

        if missing_fields:
            # Try to extract and validate field from message
            next_field = missing_fields[0]
            validation_result = _validate_and_store_field(
                session, next_field, request.message
            )

            if validation_result["valid"]:
                confirmation = validation_result.get(
                    "confirmation", f"Got it! {request.message}")
                session["chat_history"].append(
                    {"role": "assistant", "content": confirmation})

                # Check if all fields collected
                if not _get_missing_fields(session):
                    # Generate questions
                    tech_stack = session["collected_fields"].get(
                        "tech_stack", [])
                    if isinstance(tech_stack, str):
                        tech_stack = [tech_stack]

                    questions = generate_questions(tech_stack)
                    session["questions_generated"] = True
                    session["conversation_stage"] = "questions"

                    questions_text = "\n\n".join([
                        f"{i+1}. [{q.get('difficulty_stars', '★')}] {q.get('text', '')}"
                        for i, q in enumerate(questions)
                    ])

                    response = f"Great! I have all the information I need. Here are your tailored technical questions:\n\n{questions_text}\n\nPlease answer these questions to the best of your ability."
                    session["chat_history"].append(
                        {"role": "assistant", "content": response})

                    return MessageResponse(
                        response=response,
                        conversation_stage="questions",
                        fields_collected=session["collected_fields"],
                        missing_fields=[],
                        questions=questions
                    )
                else:
                    # Ask for next field
                    next_missing = _get_missing_fields(session)[0]
                    next_question = _get_field_prompt(next_missing)
                    session["chat_history"].append(
                        {"role": "assistant", "content": next_question})

                    return MessageResponse(
                        response=next_question,
                        conversation_stage="collection",
                        fields_collected=session["collected_fields"],
                        missing_fields=_get_missing_fields(session)
                    )
            else:
                # Validation failed
                error_msg = validation_result.get(
                    "error", "Invalid input. Please try again.")
                next_question = _get_field_prompt(next_field)
                response = f"{error_msg}\n\n{next_question}"
                session["chat_history"].append(
                    {"role": "assistant", "content": response})

                return MessageResponse(
                    response=response,
                    conversation_stage="collection",
                    fields_collected=session["collected_fields"],
                    missing_fields=_get_missing_fields(session)
                )

    # Handle questions stage or general conversation
    session["llm_messages"].append(
        {"role": "user", "content": request.message})

    # Ensure system prompt is first
    if not session["llm_messages"] or session["llm_messages"][0].get("role") != "system":
        session["llm_messages"] = [
            {"role": "system", "content": get_system_prompt()}] + session["llm_messages"]

    # Generate response
    response = llm_provider.generate_response(
        messages=session["llm_messages"],
        temperature=0.7,
        max_tokens=500
    )

    if response:
        session["chat_history"].append(
            {"role": "assistant", "content": response})
        session["llm_messages"].append(
            {"role": "assistant", "content": response})

        # Save session if storage is enabled
        if config.ENABLE_STORAGE and not _get_missing_fields(session):
            try:
                save_session(
                    session_id=request.session_id,
                    collected_fields=session["collected_fields"],
                    tech_stack=session["collected_fields"].get(
                        "tech_stack", []),
                    answers=[],
                    sentiment_log=[]
                )
            except Exception as e:
                logger.error(f"Error saving session: {e}")
    else:
        response = "I apologize, but I encountered an error processing your request. Please try again."
        session["chat_history"].append(
            {"role": "assistant", "content": response})

    return MessageResponse(
        response=response,
        conversation_stage=session["conversation_stage"],
        fields_collected=session["collected_fields"],
        missing_fields=_get_missing_fields(session)
    )


@app.post("/api/generate-questions")
def generate_questions_endpoint(request: QuestionGenerationRequest):
    """Generate questions for a session."""
    session = get_or_create_session(request.session_id)

    tech_stack = session["collected_fields"].get("tech_stack", [])
    if isinstance(tech_stack, str):
        tech_stack = [tech_stack]

    if not tech_stack:
        raise HTTPException(status_code=400, detail="Tech stack not provided")

    questions = generate_questions(tech_stack)
    session["questions_generated"] = True

    return {"questions": questions}


# Helper functions
REQUIRED_FIELDS = [
    "full_name", "email", "phone", "years_experience",
    "desired_position", "current_location", "tech_stack"
]


def _get_missing_fields(session: Dict[str, Any]) -> List[str]:
    """Get missing required fields."""
    collected = session["collected_fields"]
    return [field for field in REQUIRED_FIELDS
            if field not in collected or collected[field] is None]


def _validate_and_store_field(session: Dict[str, Any], field_name: str, value: str) -> Dict[str, Any]:
    """Validate and store a field."""
    if field_name == "full_name":
        is_valid, error = validate_full_name(value)
        if is_valid:
            session["collected_fields"]["full_name"] = value
            return {"valid": True, "confirmation": f"Thank you, {value}!"}
        return {"valid": False, "error": error}

    elif field_name == "email":
        is_valid, error = validate_email(value)
        if is_valid:
            session["collected_fields"]["email"] = value
            return {"valid": True, "confirmation": f"Email recorded: {value}"}
        return {"valid": False, "error": error}

    elif field_name == "phone":
        is_valid, error = validate_phone(value)
        if is_valid:
            session["collected_fields"]["phone"] = value
            return {"valid": True, "confirmation": f"Phone number recorded: {value}"}
        return {"valid": False, "error": error}

    elif field_name == "years_experience":
        is_valid, error, normalized = validate_years_experience(value)
        if is_valid:
            session["collected_fields"]["years_experience"] = normalized
            return {"valid": True, "confirmation": f"Experience recorded: {normalized} years"}
        return {"valid": False, "error": error}

    elif field_name == "desired_position":
        is_valid, error = validate_desired_position(value)
        if is_valid:
            session["collected_fields"]["desired_position"] = value
            return {"valid": True, "confirmation": f"Desired position recorded: {value}"}
        return {"valid": False, "error": error}

    elif field_name == "current_location":
        is_valid, error = validate_current_location(value)
        if is_valid:
            session["collected_fields"]["current_location"] = value
            return {"valid": True, "confirmation": f"Location recorded: {value}"}
        return {"valid": False, "error": error}

    elif field_name == "tech_stack":
        is_valid, error, normalized = validate_tech_stack(value)
        if is_valid:
            session["collected_fields"]["tech_stack"] = normalized
            stack_str = ", ".join(normalized)
            return {"valid": True, "confirmation": f"Tech stack recorded: {stack_str}"}
        return {"valid": False, "error": error}

    return {"valid": False, "error": "Unknown field"}


def _get_field_prompt(field_name: str) -> str:
    """Get prompt for a field."""
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


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
