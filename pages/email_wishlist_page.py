from pages.base_page import BasePage
from utils.allure_helpers import step


class EmailWishlistPage(BasePage):
    TITLE = "Email your wishlist to a friend"

    def __init__(self, page):
        super().__init__(page)

        self.friend_email_input = page.locator("#FriendEmail")
        self.your_email_input = page.locator("#YourEmailAddress")
        self.personal_message_input = page.locator("#PersonalMessage")
        self.send_email_button = page.locator(".send-email-a-friend-button")
        self.friend_email_validation_message = page.locator("[data-valmsg-for='FriendEmail']")
        self.your_email_validation_message = page.locator("[data-valmsg-for='YourEmailAddress']")
        self.error_message = page.locator(".message-error")
        self.sent_confirmation = page.get_by_text("Your message has been sent.", exact=False)

    @step("Fill in the 'Email a friend' form")
    def fill_form(
        self,
        friend_email: str | None = None,
        your_email: str | None = None,
        personal_message: str | None = None
    ) -> None:
        if friend_email is not None:
            self.friend_email_input.fill(friend_email)

        if your_email is not None:
            self.your_email_input.fill(your_email)

        if personal_message is not None:
            self.personal_message_input.fill(personal_message)

    @step("Send the email")
    def send(self) -> None:
        self.send_email_button.click()
