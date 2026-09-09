"""
Base LLM Provider Interface for AI Meeting Intelligence.
Author: Muhammad Awais (AI Meeting Intelligence)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseLLMProvider(ABC):
    """
    Abstract interface for LLM integrations (Gemini, OpenAI, Mock).
    """

    @abstractmethod
    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes a prompt against the model and returns parsed JSON.
        """
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Returns the identifier of the active model.
        """
        pass
