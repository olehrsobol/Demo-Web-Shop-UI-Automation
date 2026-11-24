from pages.base_page import BasePage
from utils.allure_helpers import step


class LoginPage(BasePage):
    PATH = "/login"
    TITLE = "Welcome, Please Sign In!"

    def __init__(self, page):
        super().__init__(page)

        self.email_input = page.get_by_label("Email:")
        self.password_input = page.get_by_label("Password:")
        self.login_button = page.get_by_role("button", name="Log in")
        self.remember_me_checkbox = page.get_by_label("Remember me?")
        self.forgot_password_link = page.get_by_role(
            "link",
            name="Forgot password?"
        )
        self.validation_summary = page.locator(".validation-summary-errors")

    @step("Log in as {email} (remember me: {remember_me})")
    def login(
        self,
        email: str,
        password: str,
        remember_me: bool = False
    ) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)

        if remember_me:
            self.remember_me_checkbox.check()

        self.login_button.click()
