import re

from pages.base_page import BasePage


class CheckoutLoginPage(BasePage):
    PATH = "/login/checkoutasguest"
    TITLE = "Welcome, Please Sign In!"

    def __init__(self, page):
        super().__init__(page)

        self.email_input = page.get_by_label("Email:")
        self.password_input = page.get_by_label("Password:")
        self.login_button = page.get_by_role("button", name="Log in")

    def _url_pattern(self) -> re.Pattern:
        base = re.escape(self.absolute_url())

        return re.compile(rf"^{base}\?returnUrl=%2Fcart$")