
from openai import AsyncOpenAI

from .base import LLMProvider

DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"


class DeepSeekProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str = ""):
        super().__init__(api_key, model_name)
        self._client = AsyncOpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)

    @property
    def provider_name(self) -> str:
        return "deepseek"

    async def chat(self, prompt: str, system_prompt: str | None = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        resp = await self._client.chat.completions.create(
            model=self.model_name or "deepseek-chat",
            messages=messages,
        )
        return resp.choices[0].message.content or ""

    async def chat_stream(self, prompt: str, system_prompt: str | None = None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        stream = await self._client.chat.completions.create(
            model=self.model_name or "deepseek-chat",
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
