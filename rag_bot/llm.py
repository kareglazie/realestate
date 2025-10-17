import os
import requests
from dotenv import load_dotenv
from typing import Any, List, Optional, Mapping

from langchain_core.language_models.llms import LLM as BaseLLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun

load_dotenv()

class LLM(BaseLLM):
    api_url: str = ""
    model: str = ""
    temperature: float = 0.7
    max_tokens: int = 512
    api_key: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = os.environ.get("LLM_API_URL", "http://localhost:1234/v1/chat/completions")
        self.model = os.environ.get("LLM_MODEL", "qwen2.5-coder-7b-instruct")
        self.temperature = float(os.environ.get("LLM_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.environ.get("LLM_MAX_TOKENS", "512"))
        self.api_key = os.environ.get("OPENAI_API_KEY")

    @property
    def _llm_type(self) -> str:
        """Возвращает тип LLM."""
        return "custom_llm"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Основной метод для генерации ответа."""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False
        }
        
        if stop:
            payload["stop"] = stop

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при обращении к LLM API: {str(e)}")

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Возвращает параметры для идентификации модели."""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_url": self.api_url
        }