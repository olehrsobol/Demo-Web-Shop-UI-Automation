from pages.items_table_page import ItemsTablePage
from utils.allure_helpers import step


class CartPage(ItemsTablePage):
    PATH = "/cart"
    TITLE = "Shopping cart"

    def __init__(self, page):
        super().__init__(
            page,
            product_names=page.locator(".product-name"),
            update_button=page.get_by_role(
                "button",
                name="Update shopping cart"
            ),
        )

        self.shopping_cart_link = page.get_by_role(
            "link",
            name="Shopping cart"
        ).first

        self.continue_shopping_button = page.get_by_role(
            "button",
            name="Continue shopping"
        )
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.empty_cart_message = page.locator(".order-summary-content")

        self.terms_of_service_checkbox = page.locator("#termsofservice")
        self.terms_warning = page.locator(".ui-dialog")

    @step("Accept the terms of service")
    def accept_terms_of_service(self) -> None:
        self.terms_of_service_checkbox.check()

    @step("Click 'Checkout'")
    def click_checkout(self) -> None:
        self.checkout_button.click()
