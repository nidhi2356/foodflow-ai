import json
import re

from app.llm.service import LLMService
from app.logger.logger import logger
from app.models.query import FoodQuery


class QueryUnderstandingService:

    def __init__(self):

        self.llm_service = LLMService()

        logger.info(
            "Query Understanding Service initialized"
        )

    def understand(self, query: str) -> FoodQuery:

        prompt = f"""
You are the query understanding component of a food search system.

Your job is to convert a user's natural-language food search query
into a structured JSON object.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations.
Do not include ```json or ```.

The JSON must contain exactly these fields:

{{
    "semantic_query": string,
    "is_veg": boolean or null,
    "max_price": number or null,
    "min_rating": number or null,
    "cuisine": string or null,
    "spice_level": string or null,
    "dietary_tags": list of strings
}}

Data type rules:

1. semantic_query must be a string.

2. is_veg must be:
   - true when the user explicitly requests vegetarian/veg food.
   - false when the user explicitly requests non-vegetarian/non-veg food.
   - null when vegetarian status is not specified.

3. max_price must be a number or null.
   - Do NOT include ₹ or any other currency symbol.
   - Do NOT return the price as a string.
   - Example: "food under ₹400" -> 400.

4. min_rating must be a number or null.
   - Do NOT return the rating as a string.
   - Example: "rating above 4.5" -> 4.5.

5. cuisine must be a string or null.

6. spice_level must be a string or null.

7. dietary_tags must be a list of strings.

8. Use null whenever a value is not specified.

Extraction rules:

1. semantic_query:

   - Keep the main food intent.
   - Remove hard constraints such as price, rating and vegetarian status.
   - Keep meaningful food concepts such as meal type, ingredients and food preferences.

2. is_veg:

   - Set true when the user explicitly requests vegetarian/veg food.
   - Set false when the user explicitly requests non-vegetarian/non-veg food.
   - Otherwise set null.

3. max_price:

   - Extract the maximum price when the user says:
     "under", "below", "less than", "within", "up to", or similar.
   - Return ONLY the numeric value.
   - Example: "food under ₹400" -> 400.
   - Otherwise set null.

4. min_rating:

   - Extract the minimum rating when the user requests a rating threshold.
   - Return ONLY the numeric value.
   - Example: "rating above 4.5" -> 4.5.
   - Otherwise set null.

5. cuisine:

   - Extract the requested cuisine.
   - Examples: Indian, Italian, Punjabi, Chinese, South Indian.
   - Otherwise set null.

6. spice_level:
   Extract ONLY when explicitly mentioned.

   Normalize:
   - "mild" -> "Mild"
   - "medium" -> "Medium"
   - "spicy" -> "Hot"
   - "hot" -> "Hot"

   Do not infer spice level from cuisine or food type.

7. dietary_tags:
   Extract ONLY dietary or food-property preferences that are
   explicitly present in the user's query.

   Allowed tags:
   - Healthy
   - High Protein
   - Low Carb
   - Low Calorie
   - Vegan
   - Gluten Free
   - Keto
   - Cheesy
   - Dairy Free

   IMPORTANT:
   - NEVER infer a dietary tag from other words.
   - NEVER add a tag because it seems appropriate.
   - If the user does not explicitly mention a tag, do not include it.
   - Return [] when no dietary tag is explicitly mentioned.

   Examples:
   "healthy high protein dinner"
   -> ["Healthy", "High Protein"]

   "spicy North Indian food"
   -> []

   "cheesy pizza"
   -> ["Cheesy"]

   "healthy vegetarian food"
   -> ["Healthy"]

8. Multiple dietary preferences must all be included.

   Example:
   "healthy high protein vegetarian dinner"
   -> ["Healthy", "High Protein"]

9. Do not put vegetarian into dietary_tags.
   Vegetarian must only be represented by is_veg.

10. Do not invent preferences that are not present in the query.

11. Return ONLY the JSON object.
    Do not include any text before or after the JSON.

User query:
{query}
"""

        logger.info(
            f"Understanding query: {query}"
        )

        response = self.llm_service.generate_response(
            prompt
        )

        try:

            parsed_response = json.loads(response)
            food_query = FoodQuery(**parsed_response)

        except (ValueError,TypeError) as e:

            logger.error(f"Invalid LLM query response: {e}")
            logger.error(f"Raw response: {response}")
            raise ValueError("Unable to understand the food query") from e

        food_query = self._validate_query(query,food_query)
        return food_query

    def _validate_query(
        self,
        original_query: str,
        food_query: FoodQuery
    ) -> FoodQuery:

        query_lower = original_query.lower()

        allowed_tags = {
            "healthy": "Healthy",
            "high protein": "High Protein",
            "low carb": "Low Carb",
            "low calorie": "Low Calorie",
            "vegan": "Vegan",
            "gluten free": "Gluten Free",
            "keto": "Keto",
            "cheesy": "Cheesy",
            "dairy free": "Dairy Free"
        }

        validated_tags = []

        for keyword, normalized_tag in allowed_tags.items():

            if keyword in query_lower:
                validated_tags.append(normalized_tag)

        food_query.dietary_tags = validated_tags

        if (
            "vegetarian" in query_lower
            or re.search(r"\bveg\b", query_lower)
        ):
            food_query.is_veg = True

        if (
            "non-vegetarian" in query_lower
            or "non vegetarian" in query_lower
            or "non-veg" in query_lower
            or "non veg" in query_lower
        ):
            food_query.is_veg = False

        if "spicy" in query_lower or "hot" in query_lower:
            food_query.spice_level = "Hot"

        elif "medium" in query_lower:
            food_query.spice_level = "Medium"

        elif "mild" in query_lower:
            food_query.spice_level = "Mild"

        return food_query

if __name__ == "__main__":

    service = QueryUnderstandingService()

    query = (
        "healthy high protein vegetarian dinner under ₹400"
    )

    result = service.understand(query)

    print("\nParsed Query:")
    print(result.model_dump())