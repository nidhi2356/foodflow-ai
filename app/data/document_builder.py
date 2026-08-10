from app.data.loader import load_restaurants
from app.logger.logger import logger


def build_documents() -> list[dict]:

    restaurants = load_restaurants()

    documents = []

    for restaurant in restaurants:

        for item in restaurant["menu"]:

            text = (
                f"Restaurant: {restaurant['restaurant_name']}\n"
                f"Location: {restaurant['location']}\n"
                f"Cuisine: {', '.join(restaurant['cuisine'])}\n"
                f"Rating: {restaurant['rating']}\n"
                f"Food: {item['name']}\n"
                f"Description: {item['description']}\n"
                f"Category: {item['category']}\n"
                f"Price: ₹{item['price']}\n"
                f"Vegetarian: {'Yes' if item['is_veg'] else 'No'}\n"
                f"Spice Level: {item['spice_level']}\n"
                f"Dietary Tags: {', '.join(item['dietary_tags'])}"
            )

            metadata = {
                "restaurant_id": restaurant["restaurant_id"],
                "restaurant_name": restaurant["restaurant_name"],
                "location": restaurant["location"],
                "cuisine": ", ".join(restaurant["cuisine"]),
                "rating": restaurant["rating"],
                "item_id": item["item_id"],
                "item_name": item["name"],
                "category": item["category"],
                "price": item["price"],
                "is_veg": item["is_veg"],
                "spice_level": item["spice_level"],
                "dietary_tags": ", ".join(item["dietary_tags"])
            }

            documents.append({
                "text": text,
                "metadata": metadata
            })

    logger.info(
        f"Built {len(documents)} searchable food documents"
    )

    return documents


if __name__ == "__main__":

    documents = build_documents()

    for document in documents:
        print("\n" + "=" * 60)
        print(document["text"])
        print(document["metadata"])