from app.embeddings.service import EmbeddingService
from app.logger.logger import logger
from app.models.query import FoodQuery
from app.query.understanding import QueryUnderstandingService
from app.vector_store.chroma_service import ChromaService

class SemanticSearchService:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.chroma_service = ChromaService()

        self.query_understanding_service = (
            QueryUnderstandingService()
        )

        logger.info(
            "Semantic Search Service initialized"
        )

    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        logger.info(
            f"Performing semantic search for: {query}"
        )

        food_query: FoodQuery = (
            self.query_understanding_service.understand(
                query
            )
        )

        logger.info(
            f"Parsed query: {food_query.model_dump()}"
        )

        query_embedding = (
            self.embedding_service.generate_embedding(
                food_query.semantic_query
            )
        )

        where = self._build_filters(food_query)

        results = self.chroma_service.search(
            query_embedding=query_embedding,
            top_k=top_k,
            where=where
        )

        return results

    def _build_filters(
        self,
        food_query: FoodQuery
    ) -> dict | None:

        filters = []

        if food_query.is_veg is not None:

            filters.append({
                "is_veg": food_query.is_veg
            })

        if food_query.max_price is not None:

            filters.append({
                "price": {
                    "$lte": food_query.max_price
                }
            })

        if food_query.min_rating is not None:

            filters.append({
                "rating": {
                    "$gte": food_query.min_rating
                }
            })

        if len(filters) == 0:

            return None

        if len(filters) == 1:

            return filters[0]

        return {
            "$and": filters
        }

if __name__ == "__main__":

    service = SemanticSearchService()

    query = (
        "healthy high protein vegetarian "
        "dinner under ₹400"
    )

    results = service.search(
        query,
        top_k=5
    )

    print("\nSearch Results:\n")

    for i, document in enumerate(
        results["documents"][0]
    ):

        print(
            f"{i + 1}. {document}"
        )