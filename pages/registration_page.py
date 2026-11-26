from pages.base_page import BasePage
from utils.test_data import UserData
from utils.allure_helpers import step


class RegistrationPage(BasePage):
    PATH = "/register"
    TITLE = "Register"

    def __init__(self, page):
        super().__init__(page)

        self.male_gender_radio = page.get_by_role(
            "radio",
            name="Male",
            exact=True
        )
        self.female_gender_radio = page.get_by_role(
            "radio",
            name="Female",
            exact=True
        )
        self.first_name_input = page.get_by_label("First name:")
        self.last_name_input = page.get_by_label("Last name:")
        self.email_input = page.get_by_label("Email:")
        self.password_input = page.get_by_role(
            "textbox",
            name="Password:",
            exact=True
        )
        self.confirm_password_input = page.get_by_role(
            "textbox",
            name="Confirm password:",
            exact=True
        )

        self.register_button = page.get_by_role("button", name="Register")
        self.registration_result = page.locator(".result")
        self.validation_summary = page.locator(".validation-summary-errors")
        self.field_validation_errors = page.locator(".field-validation-error")

    @step("Register user {user.email}")
    def register(self, user: UserData, gender: str = "male") -> None:
        if gender == "male":
            self.male_gender_radio.check()
        elif gender == "female":
            self.female_gender_radio.check()

        self.first_name_input.fill(user.first_name)
        self.last_name_input.fill(user.last_name)
        self.email_input.fill(user.email)
        self.password_input.fill(user.password)
        self.confirm_password_input.fill(user.confirm_password)
        self.register_button.click()