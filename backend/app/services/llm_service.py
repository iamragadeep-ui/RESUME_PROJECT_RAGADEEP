from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

from app.config import get_settings

settings = get_settings()


class LLMService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def is_configured(self) -> bool:
        return self.client is not None

    def generate(self, prompt: str, system_prompt: str | None = None, model: str | None = None) -> str:
        if not self.is_configured():
            return "OpenAI API key is not configured. Running in demo mode with a safe fallback response."

        response = self.client.chat.completions.create(
            model=model or settings.openai_model,
            messages=[
                {"role": "system", "content": system_prompt or "You are a helpful support assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=512,
        )
        return response.choices[0].message.content or ""
