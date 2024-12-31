# app/api/endpoints/predict.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

