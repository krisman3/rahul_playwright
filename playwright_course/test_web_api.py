import json

import pytest
from playwright.sync_api import Playwright, expect
from utils.api_base import APIUtils

# Json file -> util -> Access into test
with open('data/credentials.json', 'r') as f:
    test_data = json.load(f)
    print(test_data)
    user_credentials_list = test_data['user_credentials']


@pytest.mark.parametrize('user_credentials', user_credentials_list)
def test_e2e_web_api(playwright: Playwright, user_credentials):
    browser = playwright.chromium.launch()  # headless=True, args=["--start-maximized"]
    context = browser.new_context()  # no_viewport=True
    page = context.new_page()

    # Create order -> Order ID
    api_utils = APIUtils()
    order_id = api_utils.create_order(playwright)
    print(f"Order ID: {order_id}")

    # Login
    page.goto("https://rahulshettyacademy.com/client")
    page.get_by_placeholder("email@example.com").fill("email_kristiyan@email.com")
    page.get_by_placeholder("enter your passsword").fill("Pass1234")
    page.get_by_role("button", name="Login").click()

    # Orders History page -> Order is present
    page.get_by_role("button", name="ORDERS").click()
    expect(page.locator("body")).to_contain_text("Your Orders", use_inner_text=True)

    # Check that order id and name of item correspond
    name_col_index = None
    for index in range(page.locator("th").count()):
        if page.locator("th").nth(index).filter(has_text="Name").count() > 0:
            name_col_index = index
            break
    # Find the row that matches the current order_id
    order_id_row = page.locator("tr").filter(has_text=f"{order_id}")

    # TODO:  Hardcoded name for now, fix later
    expected_name = "ZARA COAT 3"

    expect(order_id_row.locator("th, td").nth(name_col_index)).to_have_text(expected_name)

    # Click View
    order_id_row.get_by_role("button", name="View").click()
    expect(page.locator(".tagline", has_text="Thank you"))

    # # Rahul's variant:
    # row = page.locator("tr").filter(has_text="order_id")
    # row.get_by_role("button", name="View").click()
    # expect(page.locator(".tagline", has_text="Thank you"))
