from app.models.query import FoodQuery
from app.ranking.metadata_scorer import MetadataScorer


scorer = MetadataScorer()

query = FoodQuery(
    semantic_query="vegetarian dinner",
    is_veg=True,
    dietary_tags=[
        "Healthy",
        "High Protein"
    ]
)

protein_bowl = {
    "dietary_tags": "Vegetarian, High Protein, Healthy",
    "cuisine": "Healthy, Continental",
    "spice_level": "Mild"
}

paneer_tikka = {
    "dietary_tags": "Vegetarian, High Protein",
    "cuisine": "North Indian, Punjabi",
    "spice_level": "Medium"
}

garlic_naan = {
    "dietary_tags": "Vegetarian",
    "cuisine": "North Indian, Punjabi",
    "spice_level": "Mild"
}


print(
    "Protein Bowl:",
    scorer.score(query, protein_bowl)
)

print(
    "Paneer Tikka:",
    scorer.score(query, paneer_tikka)
)

print(
    "Garlic Naan:",
    scorer.score(query, garlic_naan)
)