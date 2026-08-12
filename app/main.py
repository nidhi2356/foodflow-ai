from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="FoodFlow AI",
    description=(
        "AI-powered food search and recommendation service"
    ),
    version="1.0.0"
)


app.include_router(router)


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "foodflow-ai"
    }