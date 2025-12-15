"""Sentiment analysis utilities for TalentScout (bonus feature)."""

from typing import Optional, Dict, Any
from core.config import config
from core.logging_utils import logger

# Lazy loading of transformers
_sentiment_pipeline = None


def get_sentiment_pipeline():
    """Get or initialize the sentiment analysis pipeline."""
    global _sentiment_pipeline
    
    if _sentiment_pipeline is not None:
        return _sentiment_pipeline
    
    if not config.ENABLE_SENTIMENT:
        return None
    
    try:
        from transformers import pipeline
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            return_all_scores=True
        )
        logger.info("Sentiment analysis pipeline initialized")
        return _sentiment_pipeline
    except ImportError:
        logger.warning("transformers library not available. Install with: pip install transformers torch")
        return None
    except Exception as e:
        logger.error(f"Error initializing sentiment pipeline: {e}")
        return None


def analyze_sentiment(text: str) -> Optional[Dict[str, Any]]:
    """
    Analyze sentiment of text.
    
    Args:
        text: Text to analyze
    
    Returns:
        Dictionary with sentiment analysis results or None if unavailable
    """
    if not config.ENABLE_SENTIMENT:
        return None
    
    pipeline = get_sentiment_pipeline()
    if not pipeline:
        return None
    
    try:
        if not text or len(text.strip()) < 3:
            return None
        
        results = pipeline(text[:512])  # Limit to 512 characters
        
        if results and len(results) > 0:
            # Get the highest scoring sentiment
            scores = results[0] if isinstance(results[0], list) else results
            if scores:
                best = max(scores, key=lambda x: x.get('score', 0))
                return {
                    "label": best.get('label', 'unknown'),
                    "score": best.get('score', 0.0),
                    "all_scores": scores
                }
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
    
    return None


def get_sentiment_label(sentiment_result: Optional[Dict[str, Any]]) -> str:
    """
    Get a human-readable sentiment label.
    
    Args:
        sentiment_result: Sentiment analysis result
    
    Returns:
        Human-readable label
    """
    if not sentiment_result:
        return "neutral"
    
    label = sentiment_result.get("label", "neutral").lower()
    
    # Map common labels
    label_map = {
        "positive": "positive",
        "negative": "negative",
        "neutral": "neutral",
        "lab_0": "negative",
        "lab_1": "neutral",
        "lab_2": "positive"
    }
    
    return label_map.get(label, "neutral")


def format_sentiment_display(sentiment_result: Optional[Dict[str, Any]]) -> str:
    """
    Format sentiment result for display.
    
    Args:
        sentiment_result: Sentiment analysis result
    
    Returns:
        Formatted string for display
    """
    if not sentiment_result:
        return ""
    
    label = get_sentiment_label(sentiment_result)
    score = sentiment_result.get("score", 0.0)
    
    emoji_map = {
        "positive": "😊",
        "negative": "😟",
        "neutral": "😐"
    }
    
    emoji = emoji_map.get(label, "😐")
    return f"{emoji} Detected: {label} ({score:.2%})"

