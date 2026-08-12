from fastapi import APIRouter, HTTPException

from app.api.schemas import (
    SearchRequest,
    SearchResponse
)

from app.search.semantic_search import (
    SemanticSearchService
)

from app.logger.logger import logger


router = APIRouter(
    prefix="/api",
    tags=["Food Search"]
)


search_service = SemanticSearchService()


@router.post(
    "/search",
    response_model=SearchResponse
)
def search_food(
    request: SearchRequest
):

    logger.info(
        f"API search request: {request.query}"
    )

    try:

        response = search_service.search(
            query=request.query,
            top_k=request.top_k
        )

        return response

    except ValueError as e:

        logger.error(
            f"Query processing failed: {e}"
        )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:

        logger.error(
            f"AI service failed: {e}"
        )

        raise HTTPException(
            status_code=503,
            detail=str(e)
        )

    except Exception as e:

        logger.exception(
            "Unexpected error during food search"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )