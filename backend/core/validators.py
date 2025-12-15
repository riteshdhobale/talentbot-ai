"""Input validation utilities for TalentScout."""

import re
from typing import Optional, Tuple


# Email validation regex
EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

# Phone validation regex (supports various formats)
PHONE_PATTERN = re.compile(
    r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$'
)


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate an email address.
    
    Args:
        email: Email address to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "Email is required and must be a string"
    
    email = email.strip()
    
    if not email:
        return False, "Email cannot be empty"
    
    if not EMAIL_PATTERN.match(email):
        return False, "Invalid email format. Please provide a valid email address."
    
    return True, None


def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a phone number.
    
    Args:
        phone: Phone number to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not phone or not isinstance(phone, str):
        return False, "Phone number is required and must be a string"
    
    phone = phone.strip()
    
    # Remove common separators for validation
    phone_clean = re.sub(r'[-\s\(\)]', '', phone)
    
    if not phone_clean:
        return False, "Phone number cannot be empty"
    
    # Check if it's all digits (with optional + prefix)
    if phone_clean.startswith('+'):
        phone_clean = phone_clean[1:]
    
    if not phone_clean.isdigit():
        return False, "Phone number must contain only digits and optional separators"
    
    if len(phone_clean) < 10 or len(phone_clean) > 15:
        return False, "Phone number must be between 10 and 15 digits"
    
    # Also check with pattern for format validation
    if not PHONE_PATTERN.match(phone):
        return False, "Invalid phone number format"
    
    return True, None


def validate_years_experience(years: str | float | int) -> Tuple[bool, Optional[str], Optional[float]]:
    """
    Validate years of experience.
    
    Args:
        years: Years of experience (can be string, float, or int)
    
    Returns:
        Tuple of (is_valid, error_message, normalized_value)
    """
    if years is None:
        return False, "Years of experience is required", None
    
    # Try to convert to float
    try:
        if isinstance(years, str):
            years_float = float(years.strip())
        else:
            years_float = float(years)
    except (ValueError, AttributeError):
        return False, "Years of experience must be a number", None
    
    # Check if non-negative
    if years_float < 0:
        return False, "Years of experience cannot be negative", None
    
    # Reasonable upper bound (e.g., 50 years)
    if years_float > 50:
        return False, "Years of experience seems unusually high. Please verify.", None
    
    return True, None, years_float


def normalize_tech_stack(tech_stack: str) -> list[str]:
    """
    Normalize and parse tech stack string into a list.
    
    Args:
        tech_stack: Comma-separated or space-separated tech stack string
    
    Returns:
        List of normalized tech stack items
    """
    if not tech_stack or not isinstance(tech_stack, str):
        return []
    
    # Split by comma or newline, then by space
    items = []
    for part in re.split(r'[,;\n]', tech_stack):
        part = part.strip()
        if part:
            # Further split by spaces if needed
            sub_items = [item.strip() for item in part.split() if item.strip()]
            items.extend(sub_items)
    
    # Remove duplicates while preserving order
    seen = set()
    normalized = []
    for item in items:
        item_lower = item.lower()
        if item_lower not in seen:
            seen.add(item_lower)
            normalized.append(item)
    
    return normalized


def validate_tech_stack(tech_stack: str) -> Tuple[bool, Optional[str], list[str]]:
    """
    Validate and normalize tech stack.
    
    Args:
        tech_stack: Tech stack string to validate
    
    Returns:
        Tuple of (is_valid, error_message, normalized_stack)
    """
    if not tech_stack or not isinstance(tech_stack, str):
        return False, "Tech stack is required and must be a string", []
    
    tech_stack = tech_stack.strip()
    
    if not tech_stack:
        return False, "Tech stack cannot be empty", []
    
    normalized = normalize_tech_stack(tech_stack)
    
    if not normalized:
        return False, "Tech stack must contain at least one technology", []
    
    return True, None, normalized


def validate_full_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate full name.
    
    Args:
        name: Full name to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not isinstance(name, str):
        return False, "Full name is required and must be a string"
    
    name = name.strip()
    
    if not name:
        return False, "Full name cannot be empty"
    
    if len(name) < 2:
        return False, "Full name must be at least 2 characters long"
    
    if len(name) > 100:
        return False, "Full name is too long (maximum 100 characters)"
    
    # Check for valid characters (letters, spaces, hyphens, apostrophes)
    if not re.match(r'^[a-zA-Z\s\-\']+$', name):
        return False, "Full name can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, None


def validate_desired_position(position: str) -> Tuple[bool, Optional[str]]:
    """
    Validate desired position.
    
    Args:
        position: Desired position to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not position or not isinstance(position, str):
        return False, "Desired position is required and must be a string"
    
    position = position.strip()
    
    if not position:
        return False, "Desired position cannot be empty"
    
    if len(position) < 2:
        return False, "Desired position must be at least 2 characters long"
    
    return True, None


def validate_current_location(location: str) -> Tuple[bool, Optional[str]]:
    """
    Validate current location.
    
    Args:
        location: Current location to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not location or not isinstance(location, str):
        return False, "Current location is required and must be a string"
    
    location = location.strip()
    
    if not location:
        return False, "Current location cannot be empty"
    
    if len(location) < 2:
        return False, "Current location must be at least 2 characters long"
    
    return True, None

