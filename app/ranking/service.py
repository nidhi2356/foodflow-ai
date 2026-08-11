from app.models.query import FoodQuery
from app.ranking.metadata_scorer import MetadataScorer


class RankingService:

    def __init__(self):

        self.metadata_scorer = MetadataScorer()

    def rank(
        self,
        query: FoodQuery,
        results: list[dict]
    ) -> list[dict]:

        if not results:
            return []

        # 1 Collect Cross-Encoder scores

        cross_scores = [
            result["cross_encoder_score"]
            for result in results
        ]

        min_cross = min(cross_scores)
        max_cross = max(cross_scores)

        # 2 Normalize Cross-Encoder scores

        if max_cross == min_cross:

            for result in results:
                result["normalized_cross_score"] = 1.0

        else:

            for result in results:

                score = result["cross_encoder_score"]

                normalized = (
                    (score - min_cross)
                    / (max_cross - min_cross)
                )

                result["normalized_cross_score"] = normalized

        # 3 Calculate metadata scores

        metadata_scores = []

        for result in results:

            metadata_score = self.metadata_scorer.score(
                query,
                result["metadata"]
            )

            result["metadata_score"] = metadata_score

            metadata_scores.append(metadata_score)

        # 4 Normalize metadata scores
        

        min_metadata = min(metadata_scores)
        max_metadata = max(metadata_scores)

        if max_metadata == min_metadata:

            for result in results:
                result["normalized_metadata_score"] = 0.0

        else:

            for result in results:

                score = result["metadata_score"]

                normalized = (
                    (score - min_metadata)
                    / (max_metadata - min_metadata)
                )

                result["normalized_metadata_score"] = normalized

        # 5 Calculate final score

        for result in results:

            result["final_score"] = (
                0.7 * result["normalized_cross_score"]
                +
                0.3 * result["normalized_metadata_score"]
            )

        # 6 Sort by final score

        results.sort(
            key=lambda result: result["final_score"],
            reverse=True
        )

        return results