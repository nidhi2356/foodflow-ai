from app.retrieval.hybrid_service import (
    HybridRetrievalService
)


vector_results = [

    {
        "text": "Paneer Tikka",
        "metadata": {
            "item_id": "m001",
            "item_name": "Paneer Tikka"
        }
    },

    {
        "text": "Grilled Paneer Protein Bowl",
        "metadata": {
            "item_id": "m004",
            "item_name": "Grilled Paneer Protein Bowl"
        }
    },

    {
        "text": "Garlic Naan",
        "metadata": {
            "item_id": "m003",
            "item_name": "Garlic Naan"
        }
    }
]


bm25_results = [

    {
        "text": "Paneer Tikka",
        "metadata": {
            "item_id": "m001",
            "item_name": "Paneer Tikka"
        }
    },

    {
        "text": "Grilled Paneer Protein Bowl",
        "metadata": {
            "item_id": "m004",
            "item_name": "Grilled Paneer Protein Bowl"
        }
    },

    {
        "text": "Loaded Cheese Pizza",
        "metadata": {
            "item_id": "m006",
            "item_name": "Loaded Cheese Pizza"
        }
    }
]


service = HybridRetrievalService()

results = service.fuse(
    vector_results,
    bm25_results
)


for rank, result in enumerate(
    results,
    start=1
):

    print(
        f"{rank}. "
        f"{result['metadata']['item_name']}"
    )

    print(
        f"Vector Rank: "
        f"{result['vector_rank']}"
    )

    print(
        f"BM25 Rank: "
        f"{result['bm25_rank']}"
    )

    print(
        f"RRF Score: "
        f"{result['rrf_score']:.6f}"
    )

    print()