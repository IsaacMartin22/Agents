from __future__ import annotations

import os
from typing import Any, Dict, Optional

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - surfaced in runtime if dependency is missing
    OpenAI = None


class OpenAIClient:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.model = self.config.get("model") or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.api_key = self.config.get("api_key") or os.getenv("OPENAI_API_KEY")
        self.base_url = self.config.get("base_url") or os.getenv("OPENAI_BASE_URL")
        self.client = None

        if self.api_key and OpenAI is not None:
            client_kwargs: Dict[str, Any] = {"api_key": self.api_key}
            if self.base_url:
                client_kwargs["base_url"] = self.base_url
            self.client = OpenAI(**client_kwargs)

    def is_configured(self) -> bool:
        return bool(self.api_key) and self.client is not None

    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 400) -> str:
        if not self.is_configured():
            return (
                "LLM API is not configured. Set OPENAI_API_KEY to enable OpenAI-backed agent behavior. "
                "The repository is ready for environment-based deployment."
            )

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=messages,
        )

        content = completion.choices[0].message.content
        if content is None:
            return "OpenAI response was empty."
        return content.strip()
