import re
import allure

from playwright.sync_api import expect

from pages.checkout_login_page import CheckoutLoginPage
from pages.home_page import HomePage
from pages.order_completed_page import OrderCompletedPage
from utils.allure_labels import EPIC, Feature, Severity, Story
from utils.test_data import (DEFAULT_BILLING_ADDRESS, DEFAULT_CREDIT_CARD, PURCHASE_ORDER_NUMBER)

pytestmark = [
    allure.epic(EPIC),
    allure.feature(Feature.CHECKOUT),
]

ADDRESS = DEFAULT_BILLING_ADDRESS

# Option values used by the site's country / state drop-downs.
UKRAINE_OPTION_VALUE = "78"
OTHER_NON_US_STATE_OPTION_VALUE = "0"


def billing_text_fields(checkout_page, address):
    """(locator, expected value) pairs for the billing form's text inputs."""
    return [
        (checkout_page.first_name_input, address.first_name),
        (checkout_page.last_name_input, address.last_name),
        (checkout_page.email_input, address.email),
        (checkout_page.city_input, address.city),
        (checkout_page.address_1_input, address.address_1),
        (checkout_page.zip_code_input, address.zip_code),
        (checkout_page.phone_input, address.phone),
    ]


# Start checkout
@allure.story(Story.START_CHECKOUT)
@allure.title("User cannot start checkout without accepting the terms of service")
@allure.severity(Severity.CRITICAL)
def test_user_cannot_checkout_without_accepting_terms(computer_in_cart):
    cart_page = computer_in_cart

    cart_page.click_checkout()

    expect(cart_page.terms_warning).to_be_visible()
    expect(cart_page.terms_warning).to_contain_text(
        "Please accept the terms of service before the next step."
    )


@allure.story(Story.START_CHECKOUT)
@allure.title("Guest is redirected to the checkout login page")
@allure.severity(Severity.CRITICAL)
def test_unauthenticated_user_is_redirected_to_checkout_login(page, computer_in_cart):
    cart_page = computer_in_cart

    cart_page.accept_terms_of_service()
    cart_page.click_checkout()

    checkout_login_page = CheckoutLoginPage(page)

    expect(checkout_login_page.email_input).to_be_visible()
    expect(checkout_login_page.password_input).to_be_visible()
    checkout_login_page.expect_opened()


@allure.story(Story.START_CHECKOUT)
@allure.title("Logged-in user can proceed to checkout")
@allure.severity(Severity.BLOCKER)
def test_authenticated_user_can_proceed_to_checkout(checkout_page):
    checkout_page.expect_opened()


# Billing address
@allure.story(Story.BILLING_ADDRESS)
@allure.title("Billing address form contains all the fields")
@allure.severity(Severity.NORMAL)
def test_checkout_page_contains_billing_address_fields(checkout_page):
    expect(checkout_page.billing_address_section).to_be_visible()

    checkout_page.select_new_billing_address()

    for field in (
        checkout_page.first_name_input,
        checkout_page.last_name_input,
        checkout_page.email_input,
        checkout_page.country_select,
        checkout_page.state_select,
        checkout_page.city_input,
        checkout_page.address_1_input,
        checkout_page.zip_code_input,
        checkout_page.phone_input,
    ):
        expect(field).to_be_visible()


@allure.story(Story.BILLING_ADDRESS)
@allure.title("User can fill in the billing address")
@allure.severity(Severity.NORMAL)
def test_user_can_fill_billing_address(checkout_page):
    checkout_page.select_new_billing_address()
    checkout_page.fill_billing_address(ADDRESS)

    for field, value in billing_text_fields(checkout_page, ADDRESS):
        expect(field).to_have_value(value)


@allure.story(Story.BILLING_ADDRESS)
@allure.title("User can select the country and the state")
@allure.severity(Severity.NORMAL)
def test_user_can_select_country_and_state_in_billing_address(checkout_page):
    checkout_page.select_new_billing_address()

    checkout_page.select_country(ADDRESS.country)
    expect(checkout_page.country_select).to_have_value(UKRAINE_OPTION_VALUE)

    checkout_page.select_state(ADDRESS.state)
    expect(checkout_page.state_select).to_have_value(
        OTHER_NON_US_STATE_OPTION_VALUE
    )


@allure.story(Story.BILLING_ADDRESS)
@allure.title("User can continue from the billing address to the shipping method")
@allure.severity(Severity.CRITICAL)
def test_user_can_continue_from_billing_address(checkout_page):
    checkout_page.select_new_billing_address()
    checkout_page.fill_billing_address(ADDRESS)
    checkout_page.select_location(ADDRESS.country, ADDRESS.state)

    for field, value in billing_text_fields(checkout_page, ADDRESS):
        expect(field).to_have_value(value)
    expect(checkout_page.country_select).to_have_value(UKRAINE_OPTION_VALUE)

    checkout_page.proceed_from_billing_address()

    expect(checkout_page.shipping_address_section).to_be_visible()
    expect(checkout_page.pickup_in_store_checkbox).not_to_be_checked()

    checkout_page.proceed_from_shipping_address()

    expect(checkout_page.shipping_method_section).to_be_visible()
    expect(checkout_page.ground_shipping_radio).to_be_checked()


# Shipping method
@allure.story(Story.SHIPPING_METHOD)
@allure.title("User can select Next Day Air shipping")
@allure.severity(Severity.CRITICAL)
def test_user_can_select_next_day_air_shipping(checkout_at_shipping_method):
    checkout_page = checkout_at_shipping_method

    expect(checkout_page.shipping_method_section).to_be_visible()

    checkout_page.select_next_day_air_shipping()

    expect(checkout_page.next_day_air_shipping_radio).to_be_checked()
    expect(checkout_page.ground_shipping_radio).not_to_be_checked()

    checkout_page.proceed_from_shipping_method()
    expect(checkout_page.payment_method_section).to_be_visible()


# Payment method
@allure.story(Story.PAYMENT_METHOD)
@allure.title("User can pay by Cash On Delivery")
@allure.severity(Severity.CRITICAL)
def test_user_can_view_cod_payment_information(checkout_at_payment_method):
    checkout_page = checkout_at_payment_method

    expect(checkout_page.payment_method_section).to_be_visible()
    expect(checkout_page.cash_on_delivery_radio).to_be_checked()

    checkout_page.proceed_from_payment_method()

    expect(checkout_page.payment_info_section).to_be_visible()
    expect(checkout_page.cod_payment_info).to_be_visible()

    checkout_page.proceed_from_payment_info()
    expect(checkout_page.confirm_order_section).to_be_visible()


@allure.story(Story.PAYMENT_METHOD)
@allure.title("User can pay by Check / Money Order")
@allure.severity(Severity.NORMAL)
def test_user_can_view_cmo_payment_information(checkout_at_payment_method):
    checkout_page = checkout_at_payment_method

    expect(checkout_page.cash_on_delivery_radio).to_be_checked()

    checkout_page.select_check_money_order()

    expect(checkout_page.check_money_order_radio).to_be_checked()
    expect(checkout_page.cash_on_delivery_radio).not_to_be_checked()

    checkout_page.proceed_from_payment_method()

    expect(checkout_page.payment_info_section).to_be_visible()
    expect(checkout_page.cmo_payment_info).to_be_visible()

    checkout_page.proceed_from_payment_info()
    expect(checkout_page.confirm_order_section).to_be_visible()


@allure.story(Story.PAYMENT_METHOD)
@allure.title("Credit card payment shows the card form")
@allure.severity(Severity.NORMAL)
def test_user_can_view_credit_card_payment_information(checkout_at_payment_method):
    checkout_page = checkout_at_payment_method

    expect(checkout_page.cash_on_delivery_radio).to_be_checked()

    checkout_page.select_credit_card()

    expect(checkout_page.credit_card_radio).to_be_checked()
    expect(checkout_page.cash_on_delivery_radio).not_to_be_checked()

    checkout_page.proceed_from_payment_method()

    expect(checkout_page.payment_info_section).to_be_visible()

    for field in (
        checkout_page.credit_card_type_select,
        checkout_page.cardholder_name_input,
        checkout_page.card_number_input,
        checkout_page.expiration_month_select,
        checkout_page.expiration_year_select,
        checkout_page.card_code_input,
    ):
        expect(field).to_be_visible()


@allure.story(Story.PAYMENT_METHOD)
@allure.title("User can fill in the credit card details")
@allure.severity(Severity.NORMAL)
def test_user_can_fill_credit_card_payment_information(checkout_at_payment_method):
    checkout_page = checkout_at_payment_method
    card = DEFAULT_CREDIT_CARD

    checkout_page.select_credit_card()
    expect(checkout_page.credit_card_radio).to_be_checked()

    checkout_page.proceed_from_payment_method()

    expect(checkout_page.payment_info_section).to_be_visible()

    checkout_page.fill_credit_card(card)

    expect(checkout_page.credit_card_type_select).to_have_value(card.card_type)
    expect(checkout_page.cardholder_name_input).to_have_value(card.holder_name)
    expect(checkout_page.card_number_input).to_have_value(card.number)
    expect(checkout_page.card_code_input).to_have_value(card.code)

    checkout_page.proceed_from_payment_info()

    expect(checkout_page.confirm_order_section).to_be_visible()


@allure.story(Story.PAYMENT_METHOD)
@allure.title("User can pay by Purchase Order")
@allure.severity(Severity.NORMAL)
def test_user_can_complete_purchase_order_payment_information(checkout_at_payment_method):
    checkout_page = checkout_at_payment_method
    checkout_page.select_purchase_order()

    expect(checkout_page.purchase_order_radio).to_be_checked()
    expect(checkout_page.cash_on_delivery_radio).not_to_be_checked()

    checkout_page.proceed_from_payment_method()

    expect(checkout_page.payment_info_section).to_be_visible()
    expect(checkout_page.purchase_order_number_input).to_be_visible()

    checkout_page.fill_purchase_order_number(PURCHASE_ORDER_NUMBER)

    expect(checkout_page.purchase_order_number_input).to_have_value(
        PURCHASE_ORDER_NUMBER
    )

    checkout_page.proceed_from_payment_info()

    expect(checkout_page.confirm_order_section).to_be_visible()


@allure.story(Story.PAYMENT_METHOD)
@allure.title("User can continue with an empty Purchase Order number")
@allure.severity(Severity.MINOR)
def test_user_can_continue_with_empty_purchase_order_number(checkout_at_payment_method):
    checkout_page = checkout_at_payment_method
    checkout_page.select_purchase_order()
    checkout_page.proceed_from_payment_method()

    expect(checkout_page.payment_info_section).to_be_visible()
    expect(checkout_page.purchase_order_number_input).to_be_visible()

    checkout_page.proceed_from_payment_info()
    expect(checkout_page.confirm_order_section).to_be_visible()


# Confirm the order
@allure.story(Story.CONFIRM_ORDER)
@allure.title("User can view the order summary")
@allure.severity(Severity.CRITICAL)
def test_user_can_view_confirm_order_details(checkout_at_confirm_order):
    expect(checkout_at_confirm_order.confirm_order_section).to_be_visible()
    expect(checkout_at_confirm_order.confirm_order_button).to_be_visible()


@allure.story(Story.CONFIRM_ORDER)
@allure.title("Order summary shows the billing and order information")
@allure.severity(Severity.CRITICAL)
def test_confirm_order_displays_billing_and_order_information(checkout_at_confirm_order, computer_name):
    checkout_page = checkout_at_confirm_order

    expect(checkout_page.confirm_order_billing_name).to_have_text(
        ADDRESS.full_name
    )
    expect(checkout_page.confirm_order_billing_email).to_contain_text(
        ADDRESS.email
    )
    expect(checkout_page.confirm_order_billing_phone).to_contain_text(
        ADDRESS.phone
    )
    expect(checkout_page.confirm_order_billing_address_line).to_have_text(
        ADDRESS.address_1
    )
    expect(checkout_page.confirm_order_billing_city_state_zip).to_contain_text(
        ADDRESS.city
    )
    expect(checkout_page.confirm_order_billing_city_state_zip).to_contain_text(
        ADDRESS.zip_code
    )
    expect(checkout_page.confirm_order_billing_country).to_have_text(
        ADDRESS.country
    )
    expect(checkout_page.confirm_order_payment_method).to_have_text(
        "Cash On Delivery (COD)"
    )
    expect(checkout_page.confirm_order_shipping_method).to_have_text(
        "Next Day Air"
    )
    expect(checkout_page.confirm_order_product_name).to_have_text(
        computer_name
    )
    expect(checkout_page.confirm_order_product_quantity).to_contain_text(
        "Qty.:"
    )


@allure.story(Story.CONFIRM_ORDER)
@allure.title("Order total is calculated correctly")
@allure.severity(Severity.CRITICAL)
def test_confirm_order_total_is_calculated_correctly(checkout_at_confirm_order):
    checkout_page = checkout_at_confirm_order
    expect(checkout_page.confirm_order_total).to_be_visible()

    totals = checkout_page.get_order_totals()

    assert totals.total == (
        totals.subtotal
        + totals.shipping
        + totals.payment_fee
        + totals.tax
    )


@allure.story(Story.CONFIRM_ORDER)
@allure.title("User can confirm the order")
@allure.severity(Severity.BLOCKER)
def test_user_can_confirm_order(page, checkout_at_confirm_order):
    checkout_at_confirm_order.confirm_order()

    order_completed_page = OrderCompletedPage(page)
    order_completed_page.expect_opened()

    expect(order_completed_page.success_message).to_be_visible()
    expect(order_completed_page.order_number).to_have_text(
        re.compile(r"^\s*Order number:\s*\d+\s*$")
    )
    expect(order_completed_page.order_details_link).to_be_visible()
    expect(order_completed_page.continue_button).to_be_visible()


@allure.story(Story.CONFIRM_ORDER)
@allure.title("User can return to the home page after the order is completed")
@allure.severity(Severity.NORMAL)
def test_user_can_return_to_homepage_after_order_completion(page, checkout_at_confirm_order):
    checkout_at_confirm_order.confirm_order()

    OrderCompletedPage(page).click_continue()

    HomePage(page).expect_opened()
