from pages.base_page import BasePage
from utils.allure_helpers import step


class HomePage(BasePage):
    PATH = "/"

    def __init__(self, page):
        super().__init__(page)

        self.login_link = page.get_by_role("link", name="Log in")
        self.register_link = page.get_by_role("link", name="Register")
        self.logout_link = page.get_by_role("link", name="Log out")

    @step("Click 'Log in'")
    def click_login(self) -> None:
        self.login_link.click()

    @step("Click 'Register'")
    def click_register(self) -> None:
        self.register_link.click()

    @step("Click 'Log out'")
    def click_logout(self) -> None:
        self.logout_link.click()
