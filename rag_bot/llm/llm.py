import os
import requests
from dotenv import load_dotenv

load_dotenv()  # загружает переменные из .env

class LLM:
    def __init__(self):
        self.api_url = os.environ["LLM_API_URL"]
        self.model = os.environ["LLM_MODEL"]
        self.temperature = float(os.environ["LLM_TEMPERATURE"])
        self.max_tokens = int(os.environ["LLM_MAX_TOKENS"])
        self.api_key = os.environ.get("OPENAI_API_KEY")

    def generate(self, user_message: str) -> str:
        # payload универсальный, совместим с LM Studio и ChatGPT API
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False
        }

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
