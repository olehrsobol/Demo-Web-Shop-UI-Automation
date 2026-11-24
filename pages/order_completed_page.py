from pages.base_page import BasePage
from utils.allure_helpers import step


class OrderCompletedPage(BasePage):
    PATH = "/checkout/completed"
    TITLE = "Thank you"

    def __init__(self, page):
        super().__init__(page)

        self.success_message = page.get_by_text(
            "Your order has been successfully processed!",
            exact=True
        )
        self.order_number = page.locator(".order-completed .details li").first
        self.order_details_link = page.get_by_role(
            "link",
            name="Click here for order details."
        )
        self.continue_button = page.locator(".order-completed-continue-button")

    def get_order_number_text(self) -> str:
        return self.order_number.inner_text()

    @step("Click 'Continue'")
    def click_continue(self) -> None:
        self.continue_button.click()
