from sentence_transformers import SentenceTransformer

from app.logger.logger import logger


class EmbeddingService:

    def __init__(self):

        self.model_name = "all-MiniLM-L6-v2"

        logger.info(
            f"Loading embedding model: {self.model_name}"
        )

        self.model = SentenceTransformer(
            self.model_name
        )

        logger.info(
            "Embedding model loaded successfully"
        )

    def generate_embedding(self, text: str) -> list[float]:

        embedding = self.model.encode(
            text,
            convert_to_numpy=True
        )

        return embedding.tolist()


    #batch processing
    def generate_embeddings(self, text: list[str]) -> list[list[float]]:
    
            embeddings = self.model.encode(
                text,
                convert_to_numpy=True
            )
    
            return embeddings.tolist()
    