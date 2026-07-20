import time

from playwright.sync_api import Page, Route, Playwright, expect

from playwright_course.utils.api_base import APIUtils

fake_payload_no_orders = {"data": [], "message": "No Orders"}


def intercept_response(route: Route):
    route.continue_(
        url="https://rahulshettyacademy.com/client/dashboard/order-details/6711d910ae2afd4c0b9f67c6")


# Verify page content when there's 0 orders available
def test_network(page: Page):
    # Login
    page.goto("https://rahulshettyacademy.com/client")

    page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=*", intercept_response)
    page.get_by_placeholder("email@example.com").fill("email_kristiyan@email.com")
    page.get_by_placeholder("enter your passsword").fill("Pass1234")
    page.get_by_role("button", name="Login").click()

    # Orders History page -> Order is present
    page.get_by_role("button", name="ORDERS").click()
    page.get_by_role("button", name="View").first.click()
    message = page.locator(".blink_me").text_content()
    print(message)
    assert message == "You are not authorize to view this order"


# Bypassing login, through cookies injection.
def test_session_storage(playwright: Playwright):
    api_utils = APIUtils()
    get_token = api_utils.get_token(playwright)
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Script to inject token in session local storage
    page.add_init_script(f"""localStorage.setItem('token', '{get_token}')""")
    page.goto("https://rahulshettyacademy.com/client")
    page.get_by_role("button", name="ORDERS").click()
    expect(page.get_by_text("Your Orders")).to_be_visible()
