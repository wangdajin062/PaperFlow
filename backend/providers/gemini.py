import asyncio
from typing import Optional
from google import genai
from .base import LLMProvider


class GeminiProvider(LLMProvider):
    @property
    def provider_name(self) -> str:
        return "gemini"

    async def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        client = genai.Client(api_key=self.api_key)
        model = self.model_name or "gemini-2.0-flash"
        contents = []
        if system_prompt:
            contents.append({"role": "user", "parts": [{"text": system_prompt + "\n\n" + prompt}]})
        else:
            contents.append({"role": "user", "parts": [{"text": prompt}]})
        resp = await asyncio.to_thread(
            client.models.generate_content, model=model, contents=contents
        )
        return resp.text or ""

    async def chat_stream(self, prompt: str, system_prompt: Optional[str] = None):
        client = genai.Client(api_key=self.api_key)
        model = self.model_name or "gemini-2.0-flash"
        if system_prompt:
            full_prompt = system_prompt + "\n\n" + prompt
        else:
            full_prompt = prompt
        resp = await asyncio.to_thread(
            client.models.generate_content_stream, model=model,
            contents=[{"role": "user", "parts": [{"text": full_prompt}]}],
        )
        for chunk in resp:
            if chunk.text:
                yield chunk.text
