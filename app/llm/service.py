from ollama import Client

from app.config.settings import settings
from app.logger.logger import logger


class LLMService:

    def __init__(self):

        self.client = Client(
            host=settings.ollama_base_url
        )

        self.model = settings.ollama_model

        logger.info(
            f"LLM Service initialized with model: {self.model}"
        )

    def generate_response(
        self,
        prompt: str
    ) -> str:

        logger.info(
            "Sending prompt to Ollama"
        )

        try:

            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            content = response[
                "message"
            ][
                "content"
            ]

            logger.info(
                "Response received from Ollama"
            )

            return content

        except Exception as e:

            logger.error(
                f"Ollama request failed: {e}"
            )

            raise RuntimeError(
                "LLM service is currently unavailable"
            ) from e