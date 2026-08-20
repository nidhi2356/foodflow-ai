"""
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
"""

from huggingface_hub import InferenceClient

from app.config.settings import settings
from app.logger.logger import logger


class LLMService:

    def __init__(self):

        self.client = InferenceClient(
            api_key=settings.hf_token
        )

        self.model = settings.hf_model

        logger.info(
            f"LLM Service initialized with model: {self.model}"
        )

    def generate_response(
        self,
        prompt: str
    ) -> str:

        logger.info(
            "Sending prompt to Hugging Face"
        )

        try:

            response = self.client.chat_completion(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=512,
                temperature=0.7
            )

            content = response.choices[0].message.content

            logger.info(
                "Response received from Hugging Face"
            )

            return content

        except Exception as e:

            logger.error(
                f"Hugging Face request failed: {e}"
            )

            raise RuntimeError(
                "LLM service is currently unavailable"
            ) from e