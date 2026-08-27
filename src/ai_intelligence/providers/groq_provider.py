"""
Groq Free LLM Provider implementation using OpenAI-compatible API.
Author: Muhammad Awais (AI Meeting Intelligence)
"""

import json
import os
import re
from typing import Dict, Any, Optional
from .base import BaseLLMProvider


class GroqLLMProvider(BaseLLMProvider):
    """
    Adapter for free, high-speed Groq models (e.g. openai/gpt-oss-20b, openai/gpt-oss-120b, qwen/qwen3.8-27b)
    via OpenAI-compatible API client.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "openai/gpt-oss-20b"
    ):
        self._model_name = model_name
        self._api_key = api_key or os.getenv("GROQ_API_KEY")

        if not self._api_key:
            raise ValueError(
                "Groq API key is required. Set GROQ_API_KEY environment variable "
                "or pass it directly to GroqLLMProvider."
            )

        from openai import OpenAI
        self._client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=self._api_key
        )

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
        Calls Groq API with JSON mode and returns parsed dictionary.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self._client.chat.completions.create(
            model=self._model_name,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.2,
        )

        content = response.choices[0].message.content or "{}"
        clean_text = content.strip()
        clean_text = re.sub(r"^```json\s*", "", clean_text)
        clean_text = re.sub(r"^```\s*", "", clean_text)
        clean_text = re.sub(r"\s*```$", "", clean_text)

        try:
            return json.loads(clean_text)
        except json.JSONDecodeError as err:
            raise ValueError(f"Failed to decode Groq JSON response: {err}\nResponse was:\n{clean_text[:500]}")
