from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    def __init__(self, api_key: str, model_name: str = ""):
        self.api_key = api_key
        self.model_name = model_name

    @abstractmethod
    async def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        ...

    @abstractmethod
    async def chat_stream(self, prompt: str, system_prompt: Optional[str] = None):
        """Async generator yielding text chunks."""
        yield ""  # pragma: no cover

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...

    @staticmethod
    def get_provider(provider: str, api_key: str, model_name: str = "") -> "LLMProvider":
        from .claude import ClaudeProvider
        from .openai import OpenAIProvider
        from .gemini import GeminiProvider
        from .deepseek import DeepSeekProvider

        mapping = {
            "claude": ClaudeProvider,
            "openai": OpenAIProvider,
            "gemini": GeminiProvider,
            "deepseek": DeepSeekProvider,
        }
        cls = mapping.get(provider)
        if not cls:
            raise ValueError(f"Unknown provider: {provider}")
        return cls(api_key, model_name)
