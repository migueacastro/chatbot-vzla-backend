from abc import ABC, abstractmethod
import requests


class RagEmbbeder(ABC):
    @abstractmethod
    def generate_embedding(self, data: str) -> list[float]


class OpenRouter(RagEmbbeder):
    embedder_model: str
    api_key: str
    openrouter_url ="https://openrouter.ai/api/v1/chat/completions"
    def __init__(self, embedder_model: str, api_key: str) -> None:
        self.embedder_model = embedder_model
        self.api_key = api_key

    def generate_embedding(self, data: str) -> list[float]:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        request = {
            "model": self.embedder_model,
            "input": data
        }
        response = requests.post(self.openrouter_url, headers = headers, json=request)
        parsed_response = response.json()
        embedding = parsed_response["data"][0]["embedding"]
        return embedding
