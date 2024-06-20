import time
from locust import HttpUser, task, constant

class QuickstartUser(HttpUser):
    wait_time = constant(2)
  
    @task(1)
    def index(self):
        self.client.get("/")
    
    @task(2)
    def random_pet(self):
        self.client.get("/pets/random")
