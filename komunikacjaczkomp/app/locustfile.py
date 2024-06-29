from locust import HttpUser, task


class Check(HttpUser):
    @task
    def check_all(self):
        self.client.get("/users/id/33967047780")
        self.client.get("users/department/1")
        self.client.get("departments/name/ENEA")
        self.client.get("departments/id/1")

    @task
    def check_by_param(self):
        pass
