import pytest_asyncio

from src.services.recommendation_service import RecommendationsService


@pytest_asyncio.fixture
async def recommendation_service():
    """
    Fixture to initialize the RecommendationsService for use in tests.

    Returns:
    - RecommendationsService: An initialized instance of the service.
    """
    service = RecommendationsService()
    return service