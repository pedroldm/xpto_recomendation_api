from fastapi import APIRouter, Depends

from src.dependencies import get_recommendations_service
from src.services.recommendation_service import RecommendationsService

recommendations_router = APIRouter()

@recommendations_router.get("/{user_id}")
async def get_user_recommendations(service: RecommendationsService = Depends(get_recommendations_service)):
    return {"message": "Hello, World!"}