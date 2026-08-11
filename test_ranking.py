from app.models.query import FoodQuery
from app.ranking.service import RankingService


query = FoodQuery(
    semantic_query="vegetarian dinner",
    is_veg=True,
    dietary_tags=[
        "Healthy",
        "High Protein"
    ]
)


results = [

    {
        "text": "Grilled Paneer Protein Bowl",
        "metadata": {
            "dietary_tags": "Vegetarian, High Protein, Healthy",
            "cuisine": "Healthy, Continental",
            "spice_level": "Mild"
        },
        "cross_encoder_score": 2.8663
    },

    {
        "text": "Paneer Tikka",
        "metadata": {
            "dietary_tags": "Vegetarian, High Protein",
            "cuisine": "North Indian, Punjabi",
            "spice_level": "Medium"
        },
        "cross_encoder_score": 0.5051
    },

    {
        "text": "Garlic Naan",
        "metadata": {
            "dietary_tags": "Vegetarian",
            "cuisine": "North Indian, Punjabi",
            "spice_level": "Mild"
        },
        "cross_encoder_score": -8.8228
    }
]


ranking_service = RankingService()

ranked_results = ranking_service.rank(
    query,
    results
)


for result in ranked_results:

    print("\n" + "=" * 50)

    print(
        f"Food: {result['text']}"
    )

    print(
        f"Cross Encoder: "
        f"{result['cross_encoder_score']:.4f}"
    )

    print(
        f"Normalized Cross: "
        f"{result['normalized_cross_score']:.4f}"
    )

    print(
        f"Metadata: "
        f"{result['metadata_score']:.4f}"
    )

    print(
        f"Normalized Metadata: "
        f"{result['normalized_metadata_score']:.4f}"
    )

    print(
        f"Final Score: "
        f"{result['final_score']:.4f}"
    )