from typing import Optional
from anthropic import AsyncAnthropic
from .base import LLMProvider


class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str = ""):
        super().__init__(api_key, model_name)
        self._client = AsyncAnthropic(api_key=api_key)

    @property
    def provider_name(self) -> str:
        return "claude"

    async def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        kwargs = {
            "model": self.model_name or "claude-sonnet-4-20250514",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        resp = await self._client.messages.create(**kwargs)
        return resp.content[0].text

    async def chat_stream(self, prompt: str, system_prompt: Optional[str] = None):
        kwargs = {
            "model": self.model_name or "claude-sonnet-4-20250514",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        async with self._client.messages.stream(**kwargs) as stream:
            async for text in stream.text_stream:
                yield text
