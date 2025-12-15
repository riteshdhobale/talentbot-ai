"""Data storage utilities with PII anonymization for TalentScout."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from core.config import config
from core.logging_utils import logger, redact_pii


def anonymize_pii(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Anonymize PII in data dictionary for logging/storage.
    
    Args:
        data: Data dictionary that may contain PII
    
    Returns:
        Anonymized data dictionary
    """
    anonymized = data.copy()
    
    # Anonymize email
    if "email" in anonymized and anonymized["email"]:
        email = anonymized["email"]
        if "@" in email:
            parts = email.split("@")
            if len(parts) == 2:
                # Keep first letter and domain, mask the rest
                local_part = parts[0]
                domain = parts[1]
                if len(local_part) > 1:
                    masked_local = local_part[0] + "*" * (len(local_part) - 1)
                else:
                    masked_local = "*"
                anonymized["email"] = f"{masked_local}@{domain}"
    
    # Anonymize phone
    if "phone" in anonymized and anonymized["phone"]:
        phone = anonymized["phone"]
        if len(phone) > 4:
            anonymized["phone"] = "*" * (len(phone) - 4) + phone[-4:]
        else:
            anonymized["phone"] = "*" * len(phone)
    
    # Anonymize full name (keep first letter)
    if "full_name" in anonymized and anonymized["full_name"]:
        name = anonymized["full_name"]
        if len(name) > 1:
            anonymized["full_name"] = name[0] + "*" * (len(name) - 1)
        else:
            anonymized["full_name"] = "*"
    
    return anonymized


def save_session(
    session_id: str,
    collected_fields: Dict[str, Any],
    tech_stack: list[str],
    answers: list[str],
    sentiment_log: Optional[list[Dict[str, Any]]] = None
) -> bool:
    """
    Save session data to JSON file.
    
    Args:
        session_id: Unique session identifier
        collected_fields: Dictionary of collected candidate fields
        tech_stack: List of technologies in tech stack
        answers: List of candidate answers to questions
        sentiment_log: Optional list of sentiment analysis results
    
    Returns:
        True if saved successfully, False otherwise
    """
    if not config.ENABLE_STORAGE:
        logger.info("Storage is disabled, skipping save")
        return False
    
    try:
        config.ensure_storage_dir()
        
        # Load existing sessions
        sessions = load_all_sessions()
        
        # Create session data
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "pii": anonymize_pii(collected_fields.copy()),
            "tech_stack": tech_stack,
            "answers": answers,
            "sentiment_log": sentiment_log or []
        }
        
        # Add or update session
        sessions[session_id] = session_data
        
        # Save to file
        with open(config.STORAGE_PATH, 'w') as f:
            json.dump(sessions, f, indent=2)
        
        logger.info(f"Session {session_id} saved successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error saving session: {redact_pii(str(e))}")
        return False


def load_all_sessions() -> Dict[str, Dict[str, Any]]:
    """
    Load all sessions from storage file.
    
    Returns:
        Dictionary of session_id -> session_data
    """
    if not config.ENABLE_STORAGE or not config.STORAGE_PATH.exists():
        return {}
    
    try:
        with open(config.STORAGE_PATH, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.warning(f"Error loading sessions: {e}")
        return {}


def load_session(session_id: str) -> Optional[Dict[str, Any]]:
    """
    Load a specific session by ID.
    
    Args:
        session_id: Session identifier
    
    Returns:
        Session data or None if not found
    """
    sessions = load_all_sessions()
    return sessions.get(session_id)


def delete_session(session_id: str) -> bool:
    """
    Delete a session from storage.
    
    Args:
        session_id: Session identifier to delete
    
    Returns:
        True if deleted successfully, False otherwise
    """
    if not config.ENABLE_STORAGE:
        return False
    
    try:
        sessions = load_all_sessions()
        
        if session_id in sessions:
            del sessions[session_id]
            
            # Save updated sessions
            with open(config.STORAGE_PATH, 'w') as f:
                json.dump(sessions, f, indent=2)
            
            logger.info(f"Session {session_id} deleted successfully")
            return True
        
        return False
    
    except Exception as e:
        logger.error(f"Error deleting session: {redact_pii(str(e))}")
        return False


def delete_all_sessions() -> bool:
    """
    Delete all sessions from storage.
    
    Returns:
        True if deleted successfully, False otherwise
    """
    if not config.ENABLE_STORAGE:
        return False
    
    try:
        if config.STORAGE_PATH.exists():
            config.STORAGE_PATH.unlink()
        
        logger.info("All sessions deleted successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error deleting all sessions: {redact_pii(str(e))}")
        return False


def get_session_count() -> int:
    """
    Get the total number of stored sessions.
    
    Returns:
        Number of sessions
    """
    sessions = load_all_sessions()
    return len(sessions)

