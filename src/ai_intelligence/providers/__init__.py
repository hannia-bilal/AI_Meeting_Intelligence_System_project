"""
LLM Providers package.
Author: Muhammad Awais (AI Meeting Intelligence)
"""

import os
from typing import Optional
from .base import BaseLLMProvider
from .mock_provider import MockLLMProvider


def get_llm_provider(
    provider_type: Optional[str] = None,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> BaseLLMProvider:
    """
    Factory function to instantiate the chosen LLM provider based on config or environment.
    Falls back safely to MockLLMProvider if no valid API key is present.
    """
    prov = (provider_type or os.getenv("AI_PROVIDER", "mock")).lower().strip()

    if prov == "gemini":
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            # Informative fallback to mock
            return MockLLMProvider(model_name="mock-fallback-no-gemini-key")
        from .gemini_provider import GeminiLLMProvider
        model = model_name or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        return GeminiLLMProvider(api_key=key, model_name=model)

    elif prov == "openai":
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            return MockLLMProvider(model_name="mock-fallback-no-openai-key")
        from .openai_provider import OpenAILLMProvider
        model = model_name or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return OpenAILLMProvider(api_key=key, model_name=model)

    elif prov == "groq":
        key = api_key or os.getenv("GROQ_API_KEY")
        if not key:
            return MockLLMProvider(model_name="mock-fallback-no-groq-key")
        from .groq_provider import GroqLLMProvider
        model = model_name or os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
        return GroqLLMProvider(api_key=key, model_name=model)

    return MockLLMProvider(model_name=model_name or "mock-intelligence-v1")


__all__ = [
    "BaseLLMProvider",
    "MockLLMProvider",
    "get_llm_provider"
]
