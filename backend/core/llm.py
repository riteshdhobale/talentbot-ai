"""LLM provider abstraction for TalentScout."""

from typing import Optional, List, Dict, Any
from openai import OpenAI
import requests
from core.config import config
from core.logging_utils import logger
from core.prompts import get_system_prompt


class LLMProvider:
    """Provider-agnostic LLM wrapper."""
    
    def __init__(self):
        """Initialize LLM provider."""
        self.openai_client: Optional[OpenAI] = None
        self.provider = "openai"  # Default provider
        
        # Try to initialize OpenAI
        if config.OPENAI_API_KEY:
            try:
                self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                self.openai_client = None
        
        # If OpenAI fails, try HuggingFace
        if not self.openai_client and config.HF_TOKEN:
            self.provider = "huggingface"
            logger.info("Using HuggingFace as LLM provider")
        elif not self.openai_client:
            logger.error("No LLM provider available. Please set OPENAI_API_KEY or HF_TOKEN")
    
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[str]:
        """
        Generate a response from the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens in response
        
        Returns:
            Generated response text or None if error
        """
        if self.provider == "openai" and self.openai_client:
            return self._generate_openai(messages, temperature, max_tokens)
        elif self.provider == "huggingface":
            return self._generate_huggingface(messages, temperature, max_tokens)
        else:
            logger.error("No LLM provider available")
            return None
    
    def _generate_openai(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> Optional[str]:
        """Generate response using OpenAI API."""
        try:
            # Ensure system prompt is included
            if not any(msg.get("role") == "system" for msg in messages):
                messages = [{"role": "system", "content": get_system_prompt()}] + messages
            
            response = self.openai_client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Try fallback to HuggingFace if available
            if config.HF_TOKEN and self.provider != "huggingface":
                logger.info("Falling back to HuggingFace")
                self.provider = "huggingface"
                return self._generate_huggingface(messages, temperature, max_tokens)
            return None
    
    def _generate_huggingface(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> Optional[str]:
        """Generate response using HuggingFace Inference API."""
        try:
            # Convert messages to prompt format
            prompt = self._messages_to_prompt(messages)
            
            api_url = f"https://api-inference.huggingface.co/models/{config.HF_MODEL}"
            headers = {
                "Authorization": f"Bearer {config.HF_TOKEN}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "temperature": temperature,
                    "max_new_tokens": max_tokens,
                    "return_full_text": False
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                if "generated_text" in result[0]:
                    return result[0]["generated_text"]
                elif "text" in result[0]:
                    return result[0]["text"]
            
            # Fallback: return string representation
            return str(result)
        
        except Exception as e:
            logger.error(f"HuggingFace API error: {e}")
            return None
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        Convert message list to a single prompt string.
        
        Args:
            messages: List of message dictionaries
        
        Returns:
            Formatted prompt string
        """
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}\n")
            elif role == "user":
                prompt_parts.append(f"User: {content}\n")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}\n")
        
        prompt_parts.append("Assistant: ")
        return "\n".join(prompt_parts)
    
    def is_available(self) -> bool:
        """Check if LLM provider is available."""
        return (self.openai_client is not None) or (config.HF_TOKEN is not None)


# Global LLM provider instance
_llm_provider: Optional[LLMProvider] = None


def get_llm_provider() -> LLMProvider:
    """Get or create the global LLM provider instance."""
    global _llm_provider
    if _llm_provider is None:
        _llm_provider = LLMProvider()
    return _llm_provider

