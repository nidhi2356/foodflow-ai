from fastapi import FastAPI

from app.config.settings import settings
from app.logger.logger import logger
from app.api.chat import router as chat_router


logger.info("Starting FlowFood AI")

app = FastAPI(
    title = settings.app_name,
    version= settings.app_version
)

app.include_router(chat_router)

@app.get("/")
def home():
    logger.info("Home endpoint called")

    return {
        "message": "Welcome to FoodFlow AI ",
        "version": settings.app_version,
        "environment": settings.environment
    }