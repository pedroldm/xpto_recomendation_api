import random

from locust import HttpUser, TaskSet, between, task


class RecommendationTaskSet(TaskSet):
    @task
    def get_recommendations(self):
        user_id = random.randint(1, 25000)
        self.client.get(f"/recommendations/{user_id}")

class RecommendationUser(HttpUser):
    tasks = [RecommendationTaskSet]
    wait_time = between(1, 5)