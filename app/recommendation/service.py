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

STRICT GROUNDING RULES:

1. Recommend ONLY foods present in the retrieved results.

2. Use ONLY facts explicitly present in the retrieved results.

3. NEVER invent, estimate, calculate, or assume nutritional values.

4. NEVER invent protein grams, calories, carbohydrates, fat,
   ingredients, portion sizes, preparation methods, prices,
   ratings, or dietary properties.

5. If the retrieved data says "High Protein", you may say
   that the food is tagged as "High Protein".

6. Do NOT convert "High Protein" into a numerical protein amount.

7. Do NOT assume that an ingredient automatically means a
   particular nutritional value.

8. Do NOT assume user preferences that were not explicitly
   stated in the query.

9. If a property is present in the retrieved data, you may
   state that property as a fact.

10. Recommend only information that can be directly supported
    by the retrieved context.

11. Do not mention scores, embeddings, BM25, RRF, Cross-Encoder,
    metadata scoring, or internal system details.

12. Explain why the top result matches the user's query using only explicitly stated facts from the retrieved data.

13. You may mention one or two alternatives when useful.

14. Keep the response concise and natural.

15. Do not use subjective nutritional claims such as
    "balanced", "nutritious", "healthy meal", or "good source of protein"
    unless those exact properties are explicitly present in the retrieved data.

16. When the user specifies dietary tags or other explicit preferences,
    alternatives should satisfy those same requirements whenever possible.

17. Do not recommend an alternative merely because it is present in the
    retrieved results.

18. Do not claim that one food is "better", "more comprehensive",
    "more balanced", or "more nutritious" unless the retrieved data
    explicitly supports that comparison.

19. "High Protein" is a dietary tag, not a numerical nutritional value.
    Never infer or invent protein quantities from it.

20. Do not mention "nutritional information" unless nutritional
    information is explicitly provided in the retrieved data.

21. Do not use subjective descriptions such as "nutritious",
    "well-rounded", "balanced", "delicious", "excellent",
    "ideal", or "suitable" unless the retrieved data explicitly
    supports that statement.

22. Do not make judgments about whether a spice level is suitable
    or unsuitable for the user unless the user explicitly stated
    a spice preference.

23. When mentioning a food property such as spice level, state
    only the property itself as a fact.

24. Do not add conclusions or health claims based on ingredients.
    For example, do not infer that quinoa or vegetables make a
    dish "nutritious" unless that information is explicitly
    present in the retrieved data.

If the available information is insufficient to support a claim,
simply do not make that claim.

User query:
{query}

Retrieved food results:

{context}

Generate a concise, fully grounded recommendation.
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