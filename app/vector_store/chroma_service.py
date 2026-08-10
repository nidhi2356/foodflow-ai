import chromadb
from langchain_core import documents, embeddings

from app.config.settings import settings
from app.logger.logger import logger


class ChromaService:

    def __init__(self):

        logger.info(
            f"Initializing ChromaDB at: {settings.chroma_db_path}"
        )

        self.client = chromadb.PersistentClient(
            path=settings.chroma_db_path
        )

        self.collection = self.client.get_or_create_collection(
            name="food_items",
            configuration={
                "hnsw": {
                    "space": "cosine"
                }
            }
        )

        logger.info(
            "ChromaDB collection initialized successfully"
        )

    
    def add_documents(
        self,
        documents: list[dict],
        embeddings: list[list[float]]
    ):

        ids = [
            document["metadata"]["item_id"]
            for document in documents
        ]

        texts = [
            document["text"]
            for document in documents
        ]

        metadatas = [
            document["metadata"]
            for document in documents
        ]

        self.collection.upsert(  # we are writing upsert  so that error like duplicates ids can be avoided as in upsert if the id already exists it will update the document instead of throwing an error
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

        logger.info(
            f"Added {len(documents)} documents to ChromaDB"
        )


    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        where: dict | None = None
    ):

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )

        logger.info(
            f"Retrieved {len(results['ids'][0])} documents from ChromaDB"
        )

        return results

if __name__ == "__main__":

    service = ChromaService()

    print(
        "Collection count:",
        service.collection.count()
    )