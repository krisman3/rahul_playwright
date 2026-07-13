import time

from playwright.sync_api import Page, Route

fake_payload_no_orders = {"data": [], "message": "No Orders"}


def intercept_response(route: Route):
    route.continue_(
        url="https://rahulshettyacademy.com/client/dashboard/order-details/6711d910ae2afd4c0b9f67c6")


# Verify page content when there's 0 orders available
def test_network(page: Page):
    # Login
    page.goto("https://rahulshettyacademy.com/client")

    page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=*", intercept_response)
    page.get_by_placeholder("email@example.com").fill("rahulshetty@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("Iamking@000")
    page.get_by_role("button", name="Login").click()

    # Orders History page -> Order is present
    page.get_by_role("button", name="ORDERS").click()
    page.get_by_role("button", name="View").first.click()
    message = page.locator(".blink_me").text_content()
    print(message)