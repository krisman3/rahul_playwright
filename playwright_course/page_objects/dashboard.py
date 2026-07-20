from playwright_course.page_objects.order_history_page import OrderHistoryPage


class DashboardPage:

    def __init__(self, page):
        self.page = page

    def select_orders_nav_link(self):
        # Orders History page -> Order is present
        self.page.get_by_role("button", name="ORDERS").click()
        order_history_page = OrderHistoryPage(self.page)
        return order_history_page
