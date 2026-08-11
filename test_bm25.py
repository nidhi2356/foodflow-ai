from app.data.loader import load_restaurants
from app.retrieval.bm25_service import BM25Service
from app.data.document_builder import build_documents

documents = build_documents()

bm25_service = BM25Service(
    documents
)

def build_documents():

    restaurants = load_restaurants()

    documents = []

    for restaurant in restaurants:

        for item in restaurant["menu"]:

            text = (
                f"Restaurant: {restaurant['restaurant_name']} "
                f"Location: {restaurant['location']} "
                f"Cuisine: {' '.join(restaurant['cuisine'])} "
                f"Rating: {restaurant['rating']} "
                f"Food: {item['name']} "
                f"Description: {item['description']} "
                f"Category: {item['category']} "
                f"Price: {item['price']} "
                f"Vegetarian: {'Yes' if item['is_veg'] else 'No'} "
                f"Spice Level: {item['spice_level']} "
                f"Dietary Tags: {' '.join(item['dietary_tags'])}"
            )

            documents.append({
                "text": text,
                "metadata": {
                    "item_id": item["item_id"],
                    "item_name": item["name"],
                    "restaurant_name": restaurant["restaurant_name"],
                    "price": item["price"],
                    "is_veg": item["is_veg"],
                    "dietary_tags": ", ".join(
                        item["dietary_tags"]
                    )
                }
            })

    return documents


documents = build_documents()

bm25_service = BM25Service(documents)


queries = [
    "paneer tikka",
    "high protein",
    "cheesy pizza"
]


for query in queries:

    print("\n")
    print("=" * 60)
    print(f"QUERY: {query}")
    print("=" * 60)

    results = bm25_service.search(
        query,
        top_k=5
    )

    for i, result in enumerate(results):

        print(
            f"\n{i + 1}. "
            f"{result['metadata']['item_name']}"
        )

        print(
            f"BM25 Score: "
            f"{result['bm25_score']:.4f}"
        )