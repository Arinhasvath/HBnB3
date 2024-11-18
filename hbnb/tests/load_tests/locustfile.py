# tests/load_tests/locustfile.py
from locust import HttpUser, task, between
from collections.abc import Mapping


class HBNBUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Login au démarrage
        self.client.post(
            "/api/v1/auth/login",
            json={"email": "test@test.com", "password": "test123"},
        )

    @task(3)
    def view_places(self):
        self.client.get("/api/v1/places")

    @task(2)
    def search_places(self):
        self.client.get("/api/v1/places?location=Paris")

    @task(1)
    def create_review(self):
        self.client.post(
            "/api/v1/reviews",
            json={"place_id": "1", "rating": 5, "text": "Great place!"},
        )
