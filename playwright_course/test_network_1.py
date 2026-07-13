from playwright.sync_api import Page

fake_payload_no_orders = {"data": [], "message": "No Orders"}


def intercept_response(route):
    route.fulfill(
        json=fake_payload_no_orders
    )


# Verify page content when there's 0 orders available
def test_network(page: Page):
    # Login
    page.goto("https://rahulshettyacademy.com/client")

    page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-for-customer/*", intercept_response)
    page.get_by_placeholder("email@example.com").fill("rahulshetty@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("Iamking@000")
    page.get_by_role("button", name="Login").click()

    # Orders History page -> Order is present
    page.get_by_role("button", name="ORDERS").click()
    order_text = page.locator(".mt-4").text_content()
    print(order_text)
