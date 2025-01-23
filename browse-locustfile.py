from locust import task, FastHttpUser, between
from locust import run_single_user

class Browse(FastHttpUser):
    host = "http://localhost:5000"
    
    # Class-level headers that can be reused for every request
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    # Optional: if there's a login or session management step (example shown below), you can include on_start() method
    # def on_start(self):
    #     # Handle login or session initialization here if needed
    #     self.token = get_token_from_login_or_cookie_method()
    #     self.default_headers["Cookies"] = f"token={self.token}"

    @task
    def browse_page(self):
        """Simulate browsing the product page."""
        with self.client.get(
            "/browse",
            headers=self.default_headers,
            catch_response=True
        ) as response:
            # Check if the request was successful
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error: {response.status_code}")

    # Optional: Introduce realistic wait time between requests
    wait_time = between(1, 3)

if __name__ == "__main__":
    run_single_user(Browse)