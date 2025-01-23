from locust import task, FastHttpUser, between
from insert_product import login

class AddToCart(FastHttpUser):
    # Initialize class-level variables
    username = "test123"
    password = "test123"
    host = "http://localhost:5000"
    
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    # Initialize login and set cookies
    def on_start(self):
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")
        self.default_headers["Cookies"] = f"token={self.token}"

    @task
    def get_cart(self):
        """Make a GET request to the /cart endpoint"""
        with self.client.get(
            "/cart", 
            headers=self.default_headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error: {response.status_code}")

    # Optional: Add a wait time between tasks to simulate realistic user behavior
    wait_time = between(1, 3)

if __name__ == "__main__":
    from locust import run_single_user
    run_single_user(AddToCart)