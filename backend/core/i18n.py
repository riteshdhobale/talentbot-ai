"""Multilingual support utilities for TalentScout (bonus feature)."""

from typing import Optional, Tuple
from core.config import config
from core.logging_utils import logger

# Lazy loading of googletrans
_translator = None


def get_translator():
    """Get or initialize the translator."""
    global _translator
    
    if _translator is not None:
        return _translator
    
    if not config.ENABLE_MULTILINGUAL:
        return None
    
    try:
        from googletrans import Translator
        _translator = Translator()
        logger.info("Translator initialized")
        return _translator
    except ImportError:
        logger.warning("googletrans library not available. Install with: pip install googletrans==4.0.0-rc1")
        return None
    except Exception as e:
        logger.error(f"Error initializing translator: {e}")
        return None


def detect_language(text: str) -> Optional[str]:
    """
    Detect the language of text.
    
    Args:
        text: Text to detect language for
    
    Returns:
        Language code (e.g., 'en', 'es', 'fr') or None if unavailable
    """
    if not config.ENABLE_MULTILINGUAL:
        return None
    
    translator = get_translator()
    if not translator:
        return None
    
    try:
        if not text or len(text.strip()) < 2:
            return None
        
        detection = translator.detect(text)
        return detection.lang if detection else None
    except Exception as e:
        logger.error(f"Error detecting language: {e}")
        return None


def translate_text(text: str, target_lang: str = "en", source_lang: Optional[str] = None) -> Optional[str]:
    """
    Translate text to target language.
    
    Args:
        text: Text to translate
        target_lang: Target language code (default: 'en')
        source_lang: Source language code (optional, auto-detect if not provided)
    
    Returns:
        Translated text or None if unavailable
    """
    if not config.ENABLE_MULTILINGUAL:
        return None
    
    translator = get_translator()
    if not translator:
        return None
    
    try:
        if not text or len(text.strip()) < 2:
            return None
        
        result = translator.translate(text, dest=target_lang, src=source_lang)
        return result.text if result else None
    except Exception as e:
        logger.error(f"Error translating text: {e}")
        return None


def is_english(text: str) -> bool:
    """
    Check if text is in English.
    
    Args:
        text: Text to check
    
    Returns:
        True if text appears to be in English
    """
    lang = detect_language(text)
    return lang == "en" if lang else True  # Default to English if detection fails


def get_language_name(lang_code: str) -> str:
    """
    Get human-readable language name from code.
    
    Args:
        lang_code: Language code (e.g., 'en', 'es')
    
    Returns:
        Language name
    """
    lang_names = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "ru": "Russian",
        "ar": "Arabic",
        "hi": "Hindi"
    }
    return lang_names.get(lang_code, lang_code.upper())

