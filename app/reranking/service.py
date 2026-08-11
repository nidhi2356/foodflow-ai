from sentence_transformers import CrossEncoder


class RerankerService:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query: str,
        documents: list[dict]
    ) -> list[dict]:

        pairs = [
            (query, document["text"])
            for document in documents
        ]

        scores = self.model.predict(pairs)

        results = []

        for document, score in zip(
            documents,
            scores
        ):

            results.append({
                "text": document["text"],
                "metadata": document["metadata"],
                "cross_encoder_score": float(score)
            })

        return results