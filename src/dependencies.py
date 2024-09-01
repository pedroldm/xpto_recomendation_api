from src.services.recommendation_service import RecommendationsService


class DependencyProvider:
    def __init__(self):
        self.recommendations_service = RecommendationsService()
    
    def get_recommendations(self) -> RecommendationsService:
        return self.recommendations_service

dependency_provider = DependencyProvider()

def get_recommendations_service() -> RecommendationsService:
    return dependency_provider.get_recommendations()