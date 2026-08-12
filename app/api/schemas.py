from pydantic import BaseModel, Field, field_validator


class SearchRequest(BaseModel):

    query: str = Field(
        min_length=1,
        description="Natural language food search query"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of food results to return"
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Query cannot be empty or contain only whitespace"
            )

        return value


class FoodMetadata(BaseModel):

    item_name: str
    item_id: str
    restaurant_id: str
    restaurant_name: str
    location: str
    cuisine: str
    rating: float
    category: str
    price: float
    is_veg: bool
    spice_level: str
    dietary_tags: str


class SearchResult(BaseModel):

    text: str

    metadata: FoodMetadata

    cross_encoder_score: float
    normalized_cross_score: float

    metadata_score: float
    normalized_metadata_score: float

    final_score: float


class SearchResponse(BaseModel):

    results: list[SearchResult]

    recommendation: str