import asyncio
from typing import Optional
from google import genai
from .base import LLMProvider


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str = ""):
        super().__init__(api_key, model_name)
        self._client = genai.Client(api_key=api_key)

    @property
    def provider_name(self) -> str:
        return "gemini"

    async def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        model = self.model_name or "gemini-2.0-flash"
        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        kwargs = {"model": model, "contents": contents}
        if system_prompt:
            kwargs["config"] = {"system_instruction": {"parts": [{"text": system_prompt}]}}
        resp = await asyncio.to_thread(self._client.models.generate_content, **kwargs)
        return resp.text or ""

    async def chat_stream(self, prompt: str, system_prompt: Optional[str] = None):
        model = self.model_name or "gemini-2.0-flash"
        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        kwargs = {"model": model, "contents": contents}
        if system_prompt:
            kwargs["config"] = {"system_instruction": {"parts": [{"text": system_prompt}]}}
        loop = asyncio.get_running_loop()
        resp = await asyncio.to_thread(self._client.models.generate_content_stream, **kwargs)
        it = iter(resp)
        while True:
            try:
                chunk = await loop.run_in_executor(None, next, it)
                if chunk.text:
                    yield chunk.text
            except StopIteration:
                break
