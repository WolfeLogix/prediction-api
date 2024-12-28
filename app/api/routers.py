# app/api/routers.py

from fastapi import APIRouter
from app.api.endpoints import predict, train  # Adapt if your folder structure differs

api_router = APIRouter()

api_router.include_router(
    predict.router, 
    prefix="/predict", 
    tags=["Predict"]
)
api_router.include_router(
    train.router, 
    prefix="/train", 
    tags=["Train"]
)
