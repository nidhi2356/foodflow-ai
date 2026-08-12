from pydantic import BaseModel, Field


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


class SearchResponse(BaseModel):

    results: list[dict]

    recommendation: str