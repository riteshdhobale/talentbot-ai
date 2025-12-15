"""Structured logging utilities with PII redaction for TalentScout."""

import logging
import re
from pathlib import Path
from typing import Any
from core.config import config

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
LOG_FILE = LOG_DIR / "talentscout.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Email and phone regex patterns for redaction
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\b\+?\d{10,15}\b')


class PIIRedactingFormatter(logging.Formatter):
    """Custom formatter that redacts PII from log messages."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with PII redaction."""
        # Get the original message
        original_msg = super().format(record)
        
        # Redact email addresses
        redacted_msg = EMAIL_PATTERN.sub("[EMAIL_REDACTED]", original_msg)
        
        # Redact phone numbers
        redacted_msg = PHONE_PATTERN.sub("[PHONE_REDACTED]", redacted_msg)
        
        return redacted_msg


def setup_logger(name: str = "talentscout", level: str = None) -> logging.Logger:
    """
    Set up a logger with file and console handlers, including PII redaction.
    
    Args:
        name: Logger name
        level: Logging level (defaults to config.LOG_LEVEL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set log level
    log_level = getattr(logging, level or config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    file_formatter = PIIRedactingFormatter(LOG_FORMAT, DATE_FORMAT)
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def redact_pii(text: str) -> str:
    """
    Redact PII from a text string.
    
    Args:
        text: Input text that may contain PII
    
    Returns:
        Text with PII redacted
    """
    # Redact emails
    text = EMAIL_PATTERN.sub("[EMAIL_REDACTED]", text)
    
    # Redact phone numbers
    text = PHONE_PATTERN.sub("[PHONE_REDACTED]", text)
    
    return text


# Create default logger
logger = setup_logger()

