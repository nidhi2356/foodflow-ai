class HybridRetrievalService:

    def __init__(self, k: int = 60):

        self.k = k

    def fuse(
        self,
        vector_results: list[dict],
        bm25_results: list[dict]
    ) -> list[dict]:

        documents = {}

        # Vector Search Rankings

        for rank, result in enumerate(
            vector_results,
            start=1
        ):

            item_id = result["metadata"]["item_id"]

            if item_id not in documents:

                documents[item_id] = {
                    "text": result["text"],
                    "metadata": result["metadata"],
                    "vector_rank": rank,
                    "bm25_rank": None,
                    "rrf_score": 0.0
                }

            documents[item_id]["rrf_score"] += (
                1 / (self.k + rank)
            )

        # BM25 Rankings

        for rank, result in enumerate(
            bm25_results,
            start=1
        ):

            item_id = result["metadata"]["item_id"]

            if item_id not in documents:

                documents[item_id] = {
                    "text": result["text"],
                    "metadata": result["metadata"],
                    "vector_rank": None,
                    "bm25_rank": rank,
                    "rrf_score": 0.0
                }

            else:

                documents[item_id]["bm25_rank"] = rank

            documents[item_id]["rrf_score"] += (
                1 / (self.k + rank)
            )

        # Sort by RRF score

        results = sorted(
            documents.values(),
            key=lambda result: result["rrf_score"],
            reverse=True
        )

        return results