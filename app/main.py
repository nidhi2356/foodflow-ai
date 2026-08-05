from fastapi import FastAPI
from app.config.settings import settings


app = FastAPI(
    title = settings.app_name,
    version= settings.app_version
)


@app.get("/")
def home():
    return {
        "message": "Welcome to FoodFlow AI 🚀",
        "version": settings.app_version,
        "environment": settings.environment
    }