from fastapi import APIRouter

from app.llm.service import LLMService
from app.models.chat import ChatRequest


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

llm_service = LLMService()


@router.post("/chat")
def chat(request: ChatRequest):

    response = llm_service.generate_response(
        request.message
    )

    return {
        "response": response
    }