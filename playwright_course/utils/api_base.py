from playwright.sync_api import Playwright
from playwright_course.utils.request_utils import auth_payload

orders_payload = {"orders": [{"country": "India", "productOrderedId": "6960eac0c941646b7a8b3e68"}]}
base_url = "https://rahulshettyacademy.com"
api_order_url = "api/ecom/order/create-order"
api_login_url = "api/ecom/auth/login"


class APIUtils:

    def get_token(self, playwright: Playwright):
        api_request_context = playwright.request.new_context(base_url=base_url)
        response = api_request_context.post(api_login_url,
                                            data={"userEmail": "rahulshetty@gmail.com", "userPassword": "Iamking@000"})
        assert response.ok
        print(response.json())
        response_body = response.json()
        return response_body["token"]

    def create_order(self, playwright: Playwright):
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com")
        response = api_request_context.post(api_order_url,
                                            data=orders_payload,
                                            headers=self.get_token(playwright))
        return response.json()
