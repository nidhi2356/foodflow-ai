from app.llm.service import LLMService
from app.logger.logger import logger


class RecommendationService:

    def __init__(self):

        self.llm_service = LLMService()

        logger.info(
            "Recommendation Service initialized"
        )

    def generate_recommendation(
        self,
        query: str,
        ranked_results: list[dict]
    ) -> str:

        logger.info(
            f"Generating recommendation for: {query}"
        )

        context = self._build_context(
            ranked_results
        )

        prompt = f"""
You are the recommendation component of a food search system.

Your job is to recommend food from the retrieved search results
based on the user's original query.

IMPORTANT RULES:

1. Recommend ONLY foods present in the retrieved results.
2. Do NOT invent foods.
3. Do NOT invent ingredients.
4. Do NOT invent nutritional information.
5. Do NOT invent prices or ratings.
6. Use only information provided in the retrieved results.
7. Explain why the top recommendation matches the user's query.
8. You may mention one or two alternatives when useful.
9. Keep the response concise and natural.
10. Do not mention scores, embeddings, BM25, RRF, Cross-Encoder,
   metadata scoring, or internal system details.
11. Do not make assumptions about the user's preferences.
12. Do not describe a food property as a preference match unless
    the user explicitly requested that property.
13. If a food property is provided in the retrieved data, you may
    state that property as a fact.

User query:
{query}

Retrieved food results:

{context}

Generate a concise recommendation for the user.
"""

        response = (
            self.llm_service.generate_response(
                prompt
            )
        )

        return response.strip()

    def _build_context(
        self,
        ranked_results: list[dict]
    ) -> str:

        context_parts = []

        for rank, result in enumerate(
            ranked_results,
            start=1
        ):

            metadata = result["metadata"]

            context_parts.append(
                f"""
Result {rank}:

Food: {metadata["item_name"]}
Restaurant: {metadata["restaurant_name"]}
Location: {metadata["location"]}
Cuisine: {metadata["cuisine"]}
Rating: {metadata["rating"]}
Price: ₹{metadata["price"]}
Vegetarian: {
    "Yes" if metadata["is_veg"] else "No"
}
Spice Level: {metadata["spice_level"]}
Dietary Tags: {metadata["dietary_tags"]}

Description:
{result["text"]}
"""
            )

        return "\n".join(context_parts)