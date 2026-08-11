from app.data.document_builder import build_documents
from app.models.query import FoodQuery
from app.retrieval.bm25_service import BM25Service
from app.retrieval.hybrid_service import HybridRetrievalService
from app.vector_store.chroma_service import ChromaService


class RetrievalService:

    def __init__(self):

        # Shared searchable documents
        self.documents = build_documents()

        self.bm25_service = BM25Service(
            self.documents
        )

        self.chroma_service = ChromaService()

        self.hybrid_service = (
            HybridRetrievalService()
        )

    def retrieve(
        self,
        query_embedding: list[float],
        query: str,
        food_query: FoodQuery,
        top_k: int = 10,
        where: dict | None = None
    ):

        # 1. Vector Search

        vector_results = (
            self.chroma_service.search(
                query_embedding=query_embedding,
                top_k=top_k,
                where=where
            )
        )

        vector_candidates = []

        documents = vector_results["documents"][0]
        metadatas = vector_results["metadatas"][0]

        for document, metadata in zip(
            documents,
            metadatas
        ):

            vector_candidates.append({
                "text": document,
                "metadata": metadata
            })

        # 2. BM25 Search

        bm25_candidates = (
            self.bm25_service.search(
                query,
                top_k=top_k
            )
        )

        # 3. Apply Hard Filters to BM25

        bm25_candidates = [
            result
            for result in bm25_candidates
            if self._matches_filters(
                result["metadata"],
                food_query
            )
        ]

        # 4. RRF Fusion

        hybrid_results = (
            self.hybrid_service.fuse(
                vector_candidates,
                bm25_candidates
            )
        )

        # 5. Return Top Candidates

        return hybrid_results[:top_k]

    def _matches_filters(
        self,
        metadata: dict,
        food_query: FoodQuery
    ) -> bool:

        # Vegetarian filter

        if (
            food_query.is_veg is not None
            and metadata["is_veg"]
            != food_query.is_veg
        ):
            return False

        # Maximum price filter

        if (
            food_query.max_price is not None
            and metadata["price"]
            > food_query.max_price
        ):
            return False

        # Minimum rating filter

        if (
            food_query.min_rating is not None
            and metadata["rating"]
            < food_query.min_rating
        ):
            return False

        return True