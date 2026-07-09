import time

from playwright.sync_api import Page, expect


def test_placeholder(page: Page):
    # Hide/display and placeholder
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_visible()
    page.get_by_role("button", name="Hide").click()
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_hidden()

    #Alert Boxes
    page.on("dialog", lambda dialog:dialog.accept())
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