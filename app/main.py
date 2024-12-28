from fastapi import FastAPI
from app.api.routers import api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="prediction-api",
        description="API for prediction of price data",
    )
    app.include_router(api_router)
    return app

app = create_app()