"""
Google Gemini LLM Provider implementation.
Author: Muhammad Awais (AI Meeting Intelligence)
"""

import json
import os
import re
from typing import Dict, Any, Optional
from .base import BaseLLMProvider


class GeminiLLMProvider(BaseLLMProvider):
    """
    Adapter for Google Gemini models via google.generativeai.
    Uses native JSON mode for reliable structured extraction.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-1.5-flash"
    ):
        self._model_name = model_name
        self._api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self._api_key:
            raise ValueError(
                "Gemini API key is required. Set GEMINI_API_KEY environment variable "
                "or pass it directly to GeminiLLMProvider."
            )

        import google.generativeai as genai
        genai.configure(api_key=self._api_key)
        self._genai = genai

    @property
    def model_name(self) -> str:
        return self._model_name

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calls Gemini API with structured JSON output enforcement.
        """
        model = self._genai.GenerativeModel(
            model_name=self._model_name,
            system_instruction=system_prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.2,
            }
        )

        response = model.generate_content(user_prompt)
        text = response.text.strip()

        # Sanitize any accidental markdown fences
        text = re.sub(r"^```json\s*", "", text)
        text = re.sub(r"^```\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

        try:
            return json.loads(text)
        except json.JSONDecodeError as err:
            raise ValueError(f"Failed to decode Gemini JSON response: {err}\nResponse text was:\n{text[:500]}")
