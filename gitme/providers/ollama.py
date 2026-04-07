import requests
from .base import BaseProvider


class OllamaProvider(BaseProvider):

    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.url = "http://127.0.0.1:11434/api/chat"

    def _fix_subject_line(self, message: str) -> str:
        lines = message.split("\n")
        if lines and ": " in lines[0]:
            prefix, desc = lines[0].split(": ", 1)
            lines[0] = f"{prefix}: {desc[0].lower() + desc[1:]}"
        return "\n".join(lines)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ]
        }

        try:
            response = requests.post(self.url, json=payload, timeout=60)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "Could not connect to Ollama. Is it running? Try: ollama serve"
            )
        except requests.exceptions.Timeout:
            raise RuntimeError(
                "Ollama took too long to respond. Try a smaller model."
            )

        result = response.json()["message"]["content"].strip()
        return self._fix_subject_line(result)