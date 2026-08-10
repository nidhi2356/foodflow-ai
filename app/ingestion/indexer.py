from app.data.document_builder import build_documents
from app.embeddings.service import EmbeddingService
from app.logger.logger import logger
from app.vector_store.chroma_service import ChromaService


def index_food_data():

    logger.info("Starting food data indexing")

    documents = build_documents()

    logger.info(
        f"Generating embeddings for {len(documents)} documents"
    )

    embedding_service = EmbeddingService()

    texts = [
        document["text"]
        for document in documents
    ]

    embeddings = embedding_service.generate_embeddings(
        texts
    )

    chroma_service = ChromaService()

    chroma_service.add_documents(
        documents,
        embeddings
    )

    logger.info("Food data indexing completed successfully")


if __name__ == "__main__":

    index_food_data()