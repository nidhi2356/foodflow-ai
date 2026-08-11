from app.models.query import FoodQuery


class MetadataScorer:

    def score(
        self,
        query: FoodQuery,
        metadata: dict
    ) -> float:

        score = 0.0

        # Dietary tag matching
        query_tags = set(query.dietary_tags)

        food_tags = set(
            tag.strip()
            for tag in metadata.get("dietary_tags", "").split(",")
        )

        if query_tags:
            matched_tags = query_tags.intersection(food_tags)

            score += len(matched_tags) * 1.0

        # Cuisine matching
        if query.cuisine:

            food_cuisines = set(
                cuisine.strip().lower()
                for cuisine in metadata.get(
                    "cuisine", ""
                ).split(",")
            )

            if query.cuisine.lower() in food_cuisines:
                score += 1.0

        # Spice level matching
        if query.spice_level:

            food_spice = metadata.get(
                "spice_level"
            )

            if (
                food_spice
                and food_spice.lower()
                == query.spice_level.lower()
            ):
                score += 2.0

        return score