from app.recommendation.service import (
    RecommendationService
)


results = [
    {
        "text": (
            "Restaurant: Punjabi Rasoi\n"
            "Location: Connaught Place, Delhi\n"
            "Cuisine: North Indian, Punjabi\n"
            "Rating: 4.5\n"
            "Food: Paneer Tikka\n"
            "Description: Grilled Indian cottage cheese "
            "marinated with yogurt and aromatic spices.\n"
            "Category: Starter\n"
            "Price: ₹280\n"
            "Vegetarian: Yes\n"
            "Spice Level: Medium\n"
            "Dietary Tags: Vegetarian, High Protein"
        ),

        "metadata": {
            "restaurant_name": "Punjabi Rasoi",
            "location": "Connaught Place, Delhi",
            "cuisine": "North Indian, Punjabi",
            "rating": 4.5,
            "item_name": "Paneer Tikka",
            "price": 280,
            "is_veg": True,
            "spice_level": "Medium",
            "dietary_tags": "Vegetarian, High Protein"
        },

        "cross_encoder_score": 6.9433,
        "metadata_score": 0.0,
        "final_score": 0.7000
    },

    {
        "text": (
            "Restaurant: Green Bowl\n"
            "Location: Saket, Delhi\n"
            "Cuisine: Healthy, Continental\n"
            "Rating: 4.6\n"
            "Food: Grilled Paneer Protein Bowl\n"
            "Description: Grilled paneer served with quinoa, "
            "vegetables, lettuce and a yogurt dressing.\n"
            "Category: Healthy Bowl\n"
            "Price: ₹350\n"
            "Vegetarian: Yes\n"
            "Spice Level: Mild\n"
            "Dietary Tags: Vegetarian, High Protein, Healthy"
        ),

        "metadata": {
            "restaurant_name": "Green Bowl",
            "location": "Saket, Delhi",
            "cuisine": "Healthy, Continental",
            "rating": 4.6,
            "item_name": "Grilled Paneer Protein Bowl",
            "price": 350,
            "is_veg": True,
            "spice_level": "Mild",
            "dietary_tags": (
                "Vegetarian, High Protein, Healthy"
            )
        },

        "cross_encoder_score": -2.1840,
        "metadata_score": 0.0,
        "final_score": 0.3507
    }
]


service = RecommendationService()

query = (
    "healthy high protein vegetarian dinner under ₹400"
)

recommendation = (
    service.generate_recommendation(
        query,
        results
    )
)

print("\nRecommendation:\n")
print(recommendation)