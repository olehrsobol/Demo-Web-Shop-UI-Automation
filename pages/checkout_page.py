from dataclasses import dataclass
from decimal import Decimal

from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.price import parse_price
from utils.test_data import Address, CreditCard
from utils.allure_helpers import step


@dataclass(frozen=True)
class OrderTotals:
    subtotal: Decimal
    shipping: Decimal
    payment_fee: Decimal
    tax: Decimal
    total: Decimal


class CheckoutPage(BasePage):
    TITLE = "Checkout"

    def __init__(self, page):
        super().__init__(page)

        self._init_step_sections(page)
        self._init_billing_address(page)
        self._init_shipping(page)
        self._init_payment(page)
        self._init_confirm_order(page)
        self.continue_button = page.get_by_role("button", name="Continue")

    # Locators

    def _init_step_sections(self, page) -> None:
        self.billing_address_section = page.get_by_text(
            "Billing address",
            exact=True
        )
        self.shipping_address_section = page.get_by_text(
            "Shipping address",
            exact=True
        )
        self.shipping_method_section = page.get_by_text(
            "Shipping method",
            exact=True
        )
        self.payment_method_section = page.get_by_text(
            "Payment method",
            exact=True
        )
        self.payment_info_section = page.get_by_text(
            "Payment information",
            exact=True
        )
        self.confirm_order_section = page.locator(
            "#checkout-step-confirm-order"
        )

    def _init_billing_address(self, page) -> None:
        self.billing_address_select = page.locator("#billing-address-select")
        self.first_name_input = page.get_by_label("First name:")
        self.last_name_input = page.get_by_label("Last name:")
        self.email_input = page.get_by_label("Email:")
        self.company_input = page.get_by_label("Company:")
        self.country_select = page.get_by_label("Country:")
        self.state_select = page.get_by_label("State / province:")
        self.city_input = page.get_by_label("City:")
        self.address_1_input = page.get_by_label("Address 1:")
        self.address_2_input = page.get_by_label("Address 2:")
        self.zip_code_input = page.get_by_label("Zip / postal code:")
        self.phone_input = page.get_by_label("Phone number:")
        self.fax_input = page.get_by_label("Fax number:")

    def _init_shipping(self, page) -> None:
        self.pickup_in_store_checkbox = page.locator("#PickUpInStore")
        self.ground_shipping_radio = page.locator("#shippingoption_0")
        self.next_day_air_shipping_radio = page.locator("#shippingoption_1")
        self.second_day_air_shipping_radio = page.locator("#shippingoption_2")

    def _init_payment(self, page) -> None:
        self.cash_on_delivery_radio = page.locator("#paymentmethod_0")
        self.check_money_order_radio = page.locator("#paymentmethod_1")
        self.credit_card_radio = page.locator("#paymentmethod_2")
        self.purchase_order_radio = page.locator("#paymentmethod_3")
        self.cod_payment_info = page.get_by_text(
            "You will pay by COD",
            exact=True
        )
        self.cmo_payment_info = page.get_by_text(
            "Mail Personal or Business Check, Cashier's Check or money order to:"
        )
        self.credit_card_type_select = page.locator("#CreditCardType")
        self.cardholder_name_input = page.locator("#CardholderName")
        self.card_number_input = page.locator("#CardNumber")
        self.expiration_month_select = page.locator("#ExpireMonth")
        self.expiration_year_select = page.locator("#ExpireYear")
        self.card_code_input = page.locator("#CardCode")
        self.purchase_order_number_input = page.locator("#PurchaseOrderNumber")

    def _init_confirm_order(self, page) -> None:
        confirm_step = "#checkout-step-confirm-order"

        self.confirm_order_billing_name = page.locator(
            f"{confirm_step} .billing-info .name"
        )
        self.confirm_order_billing_email = page.locator(
            f"{confirm_step} .billing-info .email"
        )
        self.confirm_order_billing_phone = page.locator(
            f"{confirm_step} .billing-info .phone"
        )
        self.confirm_order_billing_address_line = page.locator(
            f"{confirm_step} .billing-info .address1"
        )
        self.confirm_order_billing_city_state_zip = page.locator(
            f"{confirm_step} .billing-info .city-state-zip"
        )
        self.confirm_order_billing_country = page.locator(
            f"{confirm_step} .billing-info .country"
        )
        self.confirm_order_payment_method = page.locator(
            f"{confirm_step} .payment-method"
        )
        self.confirm_order_shipping_method = page.locator(
            f"{confirm_step} .shipping-method"
        )
        self.confirm_order_product_name = page.locator(
            f"{confirm_step} .product-name"
        )
        self.confirm_order_product_price = page.locator(
            f"{confirm_step} .product-unit-price"
        )
        self.confirm_order_product_quantity = page.locator(
            f"{confirm_step} .qty"
        )
        self.confirm_order_product_total = page.locator(
            f"{confirm_step} .product-subtotal"
        )

        cart_total_prices = page.locator(
            f"{confirm_step} .cart-total .product-price"
        )
        self.confirm_order_subtotal = cart_total_prices.nth(0)
        self.confirm_order_payment_fee = cart_total_prices.nth(2)
        self.confirm_order_tax = cart_total_prices.nth(3)
        self.confirm_order_shipping_cost = page.locator(
            f"{confirm_step} .selected-shipping-method"
        ).locator("..").locator(
            "xpath=following-sibling::td"
        ).locator(".product-price")
        self.confirm_order_total = page.locator(f"{confirm_step} .order-total")

        self.confirm_order_button = page.locator(
            ".confirm-order-next-step-button"
        )

    # Billing address

    def has_saved_billing_address(self) -> bool:
        return self.billing_address_select.count() > 0

    def get_selected_billing_address(self) -> str:
        return self.billing_address_select.locator(
            "option:checked"
        ).inner_text()

    @step("Select 'New Address'")
    def select_new_billing_address(self) -> None:
        if self.has_saved_billing_address():
            self.billing_address_select.select_option(label="New Address")

    @step("Fill in the billing address")
    def fill_billing_address(self, address: Address) -> None:
        self.first_name_input.fill(address.first_name)
        self.last_name_input.fill(address.last_name)
        self.email_input.fill(address.email)
        self.city_input.fill(address.city)
        self.address_1_input.fill(address.address_1)
        self.zip_code_input.fill(address.zip_code)
        self.phone_input.fill(address.phone)

    @step("Select country {country}")
    def select_country(self, country: str) -> None:
        self.country_select.select_option(label=country)

    @step("Select state {state}")
    def select_state(self, state: str) -> None:
        self.state_select.select_option(label=state)

    def select_location(self, country: str, state: str) -> None:
        self.select_country(country)
        self.select_state(state)

    @step("Provide the billing address")
    def provide_billing_address(self, address: Address) -> None:
        if self.has_saved_billing_address():
            selected = self.get_selected_billing_address()
            expected_parts = (
                address.full_name,
                address.address_1,
                address.city,
                address.zip_code,
                address.country,
            )
            missing = [part for part in expected_parts if part not in selected]

            assert not missing, (
                f"Saved billing address {selected!r} does not match the "
                f"expected test address; missing: {missing}"
            )
        else:
            self.fill_billing_address(address)
            self.select_location(address.country, address.state)

    # Shipping
    @step("Select shipping: Ground")
    def select_ground_shipping(self) -> None:
        self.ground_shipping_radio.check()

    @step("Select shipping: Next Day Air")
    def select_next_day_air_shipping(self) -> None:
        self.next_day_air_shipping_radio.check()

    @step("Select shipping: 2nd Day Air")
    def select_second_day_air_shipping(self) -> None:
        self.second_day_air_shipping_radio.check()

    # Payment
    @step("Select payment: Cash On Delivery")
    def select_cash_on_delivery(self) -> None:
        self.cash_on_delivery_radio.check()

    @step("Select payment: Check / Money Order")
    def select_check_money_order(self) -> None:
        self.check_money_order_radio.check()

    @step("Select payment: Credit Card")
    def select_credit_card(self) -> None:
        self.credit_card_radio.check()

    @step("Select payment: Purchase Order")
    def select_purchase_order(self) -> None:
        self.purchase_order_radio.check()

    @step("Fill in the credit card details")
    def fill_credit_card(self, card: CreditCard) -> None:
        self.credit_card_type_select.select_option(label=card.card_type)
        self.cardholder_name_input.fill(card.holder_name)
        self.card_number_input.fill(card.number)
        self.card_code_input.fill(card.code)
        self.expiration_month_select.select_option(label=card.expiration_month)
        self.expiration_year_select.select_option(label=card.expiration_year)

    @step("Enter the purchase order number")
    def fill_purchase_order_number(self, po_number: str) -> None:
        self.purchase_order_number_input.fill(po_number)

    # Step transitions
    def click_continue(self) -> None:
        self.continue_button.click()

    @step("Continue: billing address -> shipping address")
    def proceed_from_billing_address(self) -> None:
        self.click_continue()
        expect(self.pickup_in_store_checkbox).to_be_visible()

    @step("Continue: shipping address -> shipping method")
    def proceed_from_shipping_address(self) -> None:
        self.click_continue()
        expect(self.ground_shipping_radio).to_be_visible()

    @step("Continue: shipping method -> payment method")
    def proceed_from_shipping_method(self) -> None:
        self.click_continue()
        expect(self.cash_on_delivery_radio).to_be_visible()

    @step("Continue: payment method -> payment information")
    def proceed_from_payment_method(self) -> None:
        self.click_continue()

    @step("Continue: payment information -> confirm order")
    def proceed_from_payment_info(self) -> None:
        self.click_continue()
        expect(self.confirm_order_button).to_be_visible()

    # Confirm order
    def get_order_totals(self) -> OrderTotals:
        return OrderTotals(
            subtotal=parse_price(self.confirm_order_subtotal.inner_text()),
            shipping=parse_price(self.confirm_order_shipping_cost.inner_text()),
            payment_fee=parse_price(
                self.confirm_order_payment_fee.inner_text()
            ),
            tax=parse_price(self.confirm_order_tax.inner_text()),
            total=parse_price(self.confirm_order_total.inner_text()),
        )

    @step("Confirm the order")
    def confirm_order(self) -> None:
        with self.page.expect_navigation(
            url="**/checkout/completed/",
            wait_until="domcontentloaded",
            timeout=15_000
        ):
            self.confirm_order_button.click()
