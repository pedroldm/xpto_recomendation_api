from dataclasses import asdict

from cachetools import TTLCache
from fastapi import APIRouter, Depends

from src.dependencies import get_recommendations_service
from src.services.recommendation_service import RecommendationsService

cache = TTLCache(maxsize=1000, ttl=300)
recommendations_router = APIRouter()

@recommendations_router.get("/{user_id}")
async def get_user_recommendations(user_id: str, service: RecommendationsService = Depends(get_recommendations_service)):
    if user_id in cache:
        return cache[user_id]
    recommendations = await service.get_new_user_recommendations(amount=5)
    return [r.to_dict() for r in recommendations]