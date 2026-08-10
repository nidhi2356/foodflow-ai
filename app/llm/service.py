from ollama import Client
from app.config.settings import settings
from app.logger.logger import logger

class LLMService:
    def __init__(self):
        self.client = Client(host=settings.ollama_base_url)
        self.model = settings.ollama_model

        logger.info(f"LLM Service initialized with model: {self.model}")


    def generate_response(self, prompt: str) -> str:

        logger.info("Sending prompt to Ollama")

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        logger.info("Response received from Ollama")

        return response["message"]["content"]

