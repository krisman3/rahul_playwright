from playwright.sync_api import Playwright


class APIUtils:
    orders_payload = {"orders": [{"country": "India", "productOrderedId": "6960eac0c941646b7a8b3e68"}]}
    base_url = "https://rahulshettyacademy.com"
    api_order_url = "api/ecom/order/create-order"
    api_login_url = "api/ecom/auth/login"
    delete_endpoint = "api/ecom/order/delete-order/"

    def get_token(self, playwright: Playwright):
        api_request_context = playwright.request.new_context(base_url=self.base_url)
        response = api_request_context.post(self.api_login_url,
                                            data={"userEmail": "rahulshetty@gmail.com", "userPassword": "Iamking@000"})
        assert response.ok
        print(response.json())
        response_body = response.json()
        return response_body["token"]

    def create_order(self, playwright: Playwright):
        api_request_context = playwright.request.new_context(base_url=self.base_url)
        response = api_request_context.post(self.api_order_url,
                                            data=self.orders_payload,
                                            headers={"Authorization": self.get_token(playwright)})
        print(response.json())
        response_body = response.json()
        return response_body["orders"][0]

    def delete_order(self, playwright: Playwright):
        api_request_context = playwright.request.new_context(base_url=self.base_url)
        response = api_request_context.delete(self.delete_endpoint, data=None,
                                              headers={"Authorization": self.get_token(playwright)})
        print(f"DELETE RESPONSE:\n{response.json()}")
        response_body = response.json()
        return response_body["message"]
