import json
from pathlib import Path

from app.logger.logger import logger


DATA_FILE = Path("data/restaurants.json")


def load_restaurants() -> list[dict]:

    logger.info(f"Loading restaurant data from {DATA_FILE}")

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        restaurants = json.load(file)

    logger.info(
        f"Loaded {len(restaurants)} restaurants"
    )

    return restaurants


