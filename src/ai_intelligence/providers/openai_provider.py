"""
OpenAI LLM Provider implementation.
Author: Muhammad Awais (AI Meeting Intelligence)
"""

import json
import os
import re
from typing import Dict, Any, Optional
from .base import BaseLLMProvider


class OpenAILLMProvider(BaseLLMProvider):
    """
    Adapter for OpenAI models (GPT-4o, GPT-4o-mini, GPT-4-turbo) via official OpenAI SDK.
    Uses json_object response format.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gpt-4o-mini"
    ):
        self._model_name = model_name
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self._api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass it directly to OpenAILLMProvider."
            )

        from openai import OpenAI
        self._client = OpenAI(api_key=self._api_key)

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
        Calls OpenAI API with JSON mode enabled.
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
            raise ValueError(f"Failed to decode OpenAI JSON response: {err}\nResponse was:\n{clean_text[:500]}")
