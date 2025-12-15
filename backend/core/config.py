"""Configuration management for TalentScout AI Hiring Assistant."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # HuggingFace Configuration
    HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN", None)
    HF_MODEL: str = os.getenv("HF_MODEL", "microsoft/DialoGPT-medium")
    
    # Application Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENABLE_STORAGE: bool = os.getenv("ENABLE_STORAGE", "true").lower() == "true"
    STORAGE_PATH: Path = Path(os.getenv("STORAGE_PATH", "./data/sessions.json"))
    
    # Optional Features
    ENABLE_SENTIMENT: bool = os.getenv("ENABLE_SENTIMENT", "false").lower() == "true"
    ENABLE_MULTILINGUAL: bool = os.getenv("ENABLE_MULTILINGUAL", "false").lower() == "true"
    
    # Exit Keywords
    EXIT_KEYWORDS: list[str] = ["exit", "bye", "quit", "thank you", "stop"]
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            return False
        return True
    
    @classmethod
    def ensure_storage_dir(cls) -> None:
        """Ensure the storage directory exists."""
        if cls.ENABLE_STORAGE:
            cls.STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)


# Global config instance
config = Config()

