from fastapi import APIRouter

from .payments import router as payment_router
from .ai_model import router as ai_model_router
api_router = APIRouter()
api_router.include_router(payment_router, prefix="/payments", tags=["payments"])
api_router.include_router(ai_model_router, prefix="/ai_model", tags=["ai_model"])
