import time

from playwright.sync_api import Page, expect, Playwright
from pytest_playwright.pytest_playwright import playwright

from playwright_course.utils.api_base import APIUtils


def test_placeholder(page: Page):
    # Hide/display and placeholder
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_visible()
    page.get_by_role("button", name="Hide").click()
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_hidden()

    # Alert Boxes
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Confirm").click()

    # iFrame Example
    page_frame = page.frame_locator("#courses-iframe")
    page_frame.get_by_role("link", name="All Access plan").click()
    expect(page_frame.locator("body")).to_contain_text("Happy Subscibers")


def test_email(page: Page):
    page.goto("https://rahulshettyacademy.com/client/#/auth/login")
    page.locator("#userEmail").fill("test123")
    page.locator("#userPassword").fill("pass123")
    time.sleep(3)


def test_check_price_in_table(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/seleniumpractice/#/offers")

    row = page.locator("table tbody tr").filter(
        has_text="Tomato")  # can be changed with "item_name" and can be passed as argument
    headers = page.locator("table thead th")
    header_texts = headers.all_inner_texts()
    price_col_index = header_texts.index("Price")

    price_cell = row.locator("td").nth(price_col_index)

    assert price_cell.inner_text() == "37"

    for index in range(page.locator("th").count()):
        if page.locator("th").nth(index).filter(has_text="Price").count() > 0:
            price_col_value = index
            break
    rice_row = page.locator("tr").filter(has_text="Rice")
    expect(rice_row.locator("td").nth(price_col_value)).to_have_text("37")


def test_mouse_hover(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    page.goto("https://rahulshettyacademy.com/AutomationPractice")
    page.locator("#mousehover").hover()
    page.get_by_role("link", name="Top").click()


def test_e2e_web_api(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    # Create order -> Order ID
    api_utils = APIUtils()
    api_utils.create_order(playwright)

    page.goto("https://rahulshettyacademy.com/client")
    page.get_by_placeholder("email@example.com").fill("rahulshetty@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("Iamking@000")
    page.get_by_role("button", name="Login").click()

    # Orders History page -> Order is present
