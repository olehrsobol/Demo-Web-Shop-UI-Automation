from playwright.sync_api import expect

from pages.base_page import BasePage, FEEDBACK_TIMEOUT_MS
from utils.allure_helpers import step


class ProductPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.product_name = page.locator(".product-name")
        self.product_price = page.locator(".product-price")
        self.product_description = page.locator(".full-description")

        self.add_to_cart_button = page.locator(".add-to-cart-button")
        self.add_to_wishlist_button = page.locator(".add-to-wishlist-button")

        self.added_to_cart_notification = page.get_by_text(
            "The product has been added to your"
        )
        self.added_to_wishlist_notification = page.get_by_text(
            "The product has been added to your wishlist"
        )

    def get_product_name(self) -> str:
        return self.product_name.inner_text()

    def get_product_price(self) -> str:
        return self.product_price.inner_text()

    def get_product_description(self) -> str:
        return self.product_description.inner_text()

    @step("Add the product to the cart")
    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()

        expect(self.added_to_cart_notification).to_be_visible(
            timeout=FEEDBACK_TIMEOUT_MS
        )

    @step("Add the product to the wishlist")
    def add_to_wishlist(self) -> None:
        self.add_to_wishlist_button.click()

        expect(self.added_to_wishlist_notification).to_be_visible(
            timeout=FEEDBACK_TIMEOUT_MS
        )
