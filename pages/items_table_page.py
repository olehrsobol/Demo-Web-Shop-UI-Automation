from decimal import Decimal

from playwright.sync_api import Locator, expect

from pages.base_page import BasePage
from utils.price import parse_price
from utils.allure_helpers import step


class ItemsTablePage(BasePage):

    def __init__(self, page, *, product_names: Locator, update_button: Locator):
        super().__init__(page)

        self.items = page.locator(".cart-item-row")
        self.product_names = product_names
        self.quantity_inputs = page.locator(".qty-input")
        self.unit_prices = page.locator(".product-unit-price")
        self.total_prices = page.locator(".product-subtotal")
        self.remove_checkboxes = page.locator(".remove-from-cart input[type='checkbox']")
        self.update_button = update_button

    # Reading
    def get_item_count(self) -> int:
        return self.items.count()

    def get_product_name(self, index: int = 0) -> str:
        return self.product_names.nth(index).inner_text()

    def get_quantity(self, index: int = 0) -> str:
        return self.quantity_inputs.nth(index).input_value()

    def get_unit_price_value(self, index: int = 0) -> Decimal:
        return parse_price(self.unit_prices.nth(index).inner_text())

    def get_total_price_value(self, index: int = 0) -> Decimal:
        return parse_price(self.total_prices.nth(index).inner_text())

    # Assertions
    def expect_single_item(self, product_name: str) -> None:
        expect(self.items).to_have_count(1)
        expect(self.product_names.first).to_have_text(product_name)

    def expect_empty(self) -> None:
        expect(self.items).to_have_count(0)

    # Actions
    @step("Set the item quantity to {quantity}")
    def set_quantity(self, quantity: int, index: int = 0) -> None:
        self.quantity_inputs.nth(index).fill(str(quantity))
        self._submit_update()

    @step("Remove the item")
    def remove_item(self, index: int = 0) -> None:
        self.remove_checkboxes.nth(index).check()
        self._submit_update()

    @step("Remove all items from {self.PATH}")
    def clear(self) -> None:
        self.open()

        if self.items.count() == 0:
            return

        for checkbox in self.remove_checkboxes.all():
            checkbox.check()

        self._submit_update()
        self.expect_empty()

    def _submit_update(self) -> None:
        with self.page.expect_navigation():
            self.update_button.click()
