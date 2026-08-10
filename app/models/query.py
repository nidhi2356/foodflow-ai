from pydantic import BaseModel, Field


class FoodQuery(BaseModel):

    semantic_query: str

    is_veg: bool | None = None

    max_price: float | None = None

    min_rating: float | None = None

    cuisine: str | None = None

    spice_level: str | None = None

    dietary_tags: list[str] = Field(
        default_factory=list
    )