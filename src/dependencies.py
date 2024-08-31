from src.config import get_database_path
from src.services.recommendation_service import Recommendations


class DependencyProvider:
    def __init__(self):
        self.file_path = get_database_path()
        self.recommendations_service = Recommendations(self.file_path)
    
    def get_recommendations(self) -> Recommendations:
        return self.recommendations_service

dependency_provider = DependencyProvider()

def get_recommendations_service() -> Recommendations:
    return dependency_provider.get_recommendations()