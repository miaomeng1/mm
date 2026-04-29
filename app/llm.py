from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Protocol
from urllib import request

from app.config import Settings


class LLMProvider(Protocol):
    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        ...


@dataclass(slots=True)
class MockLLMProvider:
    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        del system_prompt
        snippet = user_prompt.strip().replace("\n", " ")
        snippet = snippet[:220]
        return (
            "Mock long-context synthesis:\n"
            f"- inferred intent: {snippet}\n"
            "- emphasis: repository-wide impact analysis, quality gates, GitOps delivery\n"
            "- risk note: validate deployment constraints and service naming before release"
        )


@dataclass(slots=True)
class OpenAICompatLLMProvider:
    base_url: str
    api_key: str
    model: str

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        return await asyncio.to_thread(self._complete_sync, system_prompt, user_prompt)

    def _complete_sync(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }
        req = request.Request(
            url=f"{self.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with request.urlopen(req, timeout=30) as response:
            parsed = json.loads(response.read().decode("utf-8"))
        return parsed["choices"][0]["message"]["content"]


def load_llm_provider(settings: Settings) -> LLMProvider:
    if settings.enable_llm and settings.llm_base_url and settings.llm_api_key:
        return OpenAICompatLLMProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )
    return MockLLMProvider()
