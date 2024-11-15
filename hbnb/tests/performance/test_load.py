import unittest
from locust import HttpUser, task, between

class HBNBLoadTest(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        self.client.post("/api/v1/login", json={
            "email": "test@test.com",
            "password": "test123"
        })

    @task(3)
    def view_places(self):
        self.client.get("/api/v1/places")
    
    @task(2)
    def search_places(self):
        self.client.get("/api/v1/places/search?location=beach")

    @task(1)
    def create_review(self):
        self.client.post("/api/v1/reviews", json={
            "place_id": "test-place-id",
            "rating": 5,
            "text": "Great place!"
        })