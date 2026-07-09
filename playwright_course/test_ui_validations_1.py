import time

from playwright.sync_api import Page, Playwright, expect


def test_filtering_items(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.get_by_label("Password:").fill("Learning@830$3mK2")
    page.get_by_role("combobox").select_option("teach")
    page.locator("#terms").check()
    page.get_by_role("button", name="Sign In").click()
    iphone_product = page.locator("app-card").filter(has_text="iphone X")
    iphone_product.get_by_role("button").click()
    nokia_product = page.locator("app-card").filter(has_text="Nokia Edge")
    nokia_product.get_by_role("button").click()
    page.get_by_text("Checkout").click()
    expect(page.locator(".media-body")).to_have_count(2)


def test_child_window_handle(page: Page):
    email = "mentor@rahulshettyacademy.com"

    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    with page.expect_popup() as new_page_info:
        # page.locator(".blinkingText:first-child").click()
        # page.locator(".blinkingText").first.click()
        page.get_by_role("link", name="Free Access").click()
        child_page = new_page_info.value
        text = child_page.locator(".red").text_content()
        assert text is not None
        assert email in text