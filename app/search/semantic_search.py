from app.embeddings.service import EmbeddingService
from app.logger.logger import logger
from app.models.query import FoodQuery
from app.query.understanding import QueryUnderstandingService
from app.reranking.service import RerankerService
from app.ranking.service import RankingService
from app.retrieval.retrieval_service import RetrievalService
from app.recommendation.service import RecommendationService


class SemanticSearchService:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.retrieval_service = RetrievalService()

        self.reranker_service = RerankerService()

        self.ranking_service = RankingService()

        self.recommendation_service = (
            RecommendationService()
        )

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

        # 1. Query Understanding

        food_query: FoodQuery = (
            self.query_understanding_service.understand(
                query
            )
        )

        logger.info(
            f"Parsed query: {food_query.model_dump()}"
        )

        # 2. Generate Semantic Embedding
        

        query_embedding = (
            self.embedding_service.generate_embedding(
                food_query.semantic_query
            )
        )

        # =================================
        # 3. Build Hard Filters
        # =================================

        where = self._build_filters(
            food_query
        )

        # =================================
        # 4. Hybrid Retrieval
        # =================================

        # Retrieve more candidates than final result count
        candidate_k = max(
            top_k * 2,
            10
        )

        candidates = (
            self.retrieval_service.retrieve(
                query_embedding=query_embedding,
                query=query,
                food_query=food_query,
                top_k=candidate_k,
                where=where
            )
        )
        if not candidates:
            logger.info("No food results found")
            return {
                "results": [],
                "recommendation": ("Sorry, I couldn't find any food items matching your requirements.")
            }

        logger.info(
            f"Hybrid retrieval returned "
            f"{len(candidates)} candidates"
        )

        # =================================
        # 5. Cross-Encoder Reranking
        # =================================

        reranked_results = (
            self.reranker_service.rerank(
                query,
                candidates
            )
        )

        # 6. Metadata + Cross-Encoder Ranking

        ranked_results = (
            self.ranking_service.rank(
                food_query,
                reranked_results
            )
        )

        # 7. Return Final Results

        final_results =  ranked_results[:top_k]

        try:
            recommendation = (
                self.recommendation_service.generate_recommendation(
                    query,
                    final_results
                )
            )
        except RuntimeError as e:

            logger.error(
                f"Recommendation generation failed: {e}"
            )

            recommendation = (
                "I found some matching food options, but I'm unable to generate a recommendation right now."
            )

        return{
            "results" : final_results,
            "recommendation" : recommendation
        }

    def _build_filters(
        self,
        food_query: FoodQuery
    ) -> dict | None:

        filters = []

        # Vegetarian
        if food_query.is_veg is not None:

            filters.append({
                "is_veg": food_query.is_veg
            })

        # Maximum Price
        if food_query.max_price is not None:

            filters.append({
                "price": {
                    "$lte": food_query.max_price
                }
            })

        # Minimum Rating
        if food_query.min_rating is not None:

            filters.append({
                "rating": {
                    "$gte": food_query.min_rating
                }
            })

        # No Filters
        if len(filters) == 0:
            return None

        # Single Filter

        if len(filters) == 1:
            return filters[0]

        # Multiple Filters

        return {
            "$and": filters
        }


if __name__ == "__main__":

    service = SemanticSearchService()

    query = (
        "vegan sushi under ₹50"
    )

    response = service.search(
        query,
        top_k=5
    )

    print("\nFinal Ranked Results:\n")

    for i, result in enumerate(
        response["results"]
    ):

        print("\n" + "=" * 60)

        print(
            f"Rank: {i + 1}"
        )

        print(
            f"Food: "
            f"{result['metadata']['item_name']}"
        )

        print(
            f"Cross-Encoder Score: "
            f"{result['cross_encoder_score']:.4f}"
        )

        print(
            f"Metadata Score: "
            f"{result['metadata_score']:.4f}"
        )

        print(
            f"Final Score: "
            f"{result['final_score']:.4f}"
        )

        print(
            result["text"]
        )

    print("\n" + "=" * 60)

    print("\nAI Recommendation:\n")

    print(
        response["recommendation"]
    )