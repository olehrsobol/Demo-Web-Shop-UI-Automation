import os
import platform
import allure
import pytest

from collections.abc import Iterator
from playwright.sync_api import Page, expect

from config.settings import BASE_URL, TEST_USER_EMAIL, TEST_USER_PASSWORD
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.registration_page import RegistrationPage
from pages.search_page import SearchPage
from pages.wishlist_page import WishlistPage
from utils.test_data import (COMPUTER_QUERY, DEFAULT_BILLING_ADDRESS, SMARTPHONE_QUERY)


# Allure

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when not in ("setup", "call") or not report.failed:
        return

    page = getattr(item, "funcargs", {}).get("page")
    if page is None:
        return
    try:
        allure.attach(
            page.screenshot(full_page=True),
            name="Screenshot at failure",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            page.url,
            name="URL at failure",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            page.content(),
            name="Page HTML at failure",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as error:
        allure.attach(
            str(error),
            name="Could not collect failure artifacts",
            attachment_type=allure.attachment_type.TEXT,
        )


def pytest_sessionfinish(session, exitstatus):
    alluredir = session.config.getoption("allure_report_dir", default=None)
    if not alluredir:
        return

    browsers = session.config.getoption("browser", default=None) or ["chromium"]

    os.makedirs(alluredir, exist_ok=True)
    with open(
        os.path.join(alluredir, "environment.properties"),
        "w",
        encoding="utf-8",
    ) as file:
        file.write(f"Base.URL={BASE_URL}\n")
        file.write(f"Browser={', '.join(browsers)}\n")
        file.write(f"Python={platform.python_version()}\n")
        file.write(f"OS={platform.system()}\n")


# Session state
@pytest.fixture
def home_page(page: Page) -> HomePage:
    home_page = HomePage(page)
    home_page.open()

    return home_page


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login_page = LoginPage(page)
    login_page.open()

    return login_page


@pytest.fixture
def registration_page(page: Page) -> RegistrationPage:
    registration_page = RegistrationPage(page)
    registration_page.open()

    return registration_page


def _clear_user_data(page: Page) -> None:
    with allure.step("Clean up the user's cart and wishlist"):
        home_page = HomePage(page)
        home_page.open()

        if not home_page.logout_link.is_visible():
            return

        CartPage(page).clear()
        WishlistPage(page).clear()


@pytest.fixture
def logged_in_user(page: Page, login_page: LoginPage) -> Iterator[HomePage]:
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)

    home_page = HomePage(page)
    expect(home_page.logout_link).to_be_visible()

    yield home_page

    _clear_user_data(page)


# Clean-up of server-side state (before the test)
# The matching clean-up *after* the test lives in logged_in_user's teardown.
@pytest.fixture
def empty_cart(page: Page, logged_in_user: HomePage) -> CartPage:
    cart_page = CartPage(page)
    cart_page.clear()

    return cart_page


@pytest.fixture
def empty_wishlist(page: Page, logged_in_user: HomePage) -> WishlistPage:
    wishlist_page = WishlistPage(page)
    wishlist_page.clear()

    return wishlist_page


# Search and products

@pytest.fixture
def search_page(page: Page, home_page: HomePage) -> SearchPage:
    return SearchPage(page)


@pytest.fixture
def open_product(page: Page):
    def _open_product(query: str) -> ProductPage:
        HomePage(page).open()

        search_page = SearchPage(page)
        search_page.search(query)

        expect(search_page.search_results.first).to_be_visible()
        search_page.open_first_product()

        product_page = ProductPage(page)
        expect(product_page.product_name).to_be_visible()

        return product_page
    return _open_product


@pytest.fixture
def smartphone_product_page(open_product) -> ProductPage:
    return open_product(SMARTPHONE_QUERY)


@pytest.fixture
def computer_product_page(open_product) -> ProductPage:
    return open_product(COMPUTER_QUERY)


@pytest.fixture
def smartphone_name(smartphone_product_page: ProductPage) -> str:
    return smartphone_product_page.get_product_name()


@pytest.fixture
def computer_name(computer_product_page: ProductPage) -> str:
    return computer_product_page.get_product_name()


# Cart
@pytest.fixture
def computer_in_cart(page: Page, computer_product_page: ProductPage, computer_name: str) -> CartPage:
    computer_product_page.add_to_cart()

    cart_page = CartPage(page)
    cart_page.open()
    cart_page.expect_single_item(computer_name)

    return cart_page


# Wishlist
@pytest.fixture
def smartphone_in_wishlist(empty_wishlist: WishlistPage, smartphone_product_page: ProductPage, smartphone_name: str) -> WishlistPage:
    smartphone_product_page.add_to_wishlist()

    wishlist_page = empty_wishlist
    wishlist_page.open()
    wishlist_page.expect_single_item(smartphone_name)

    return wishlist_page


# Checkout (authenticated user)
@pytest.fixture
def checkout_page(page: Page, logged_in_user: HomePage, empty_cart: CartPage, computer_in_cart: CartPage) -> CheckoutPage:
    computer_in_cart.accept_terms_of_service()
    computer_in_cart.click_checkout()

    checkout_page = CheckoutPage(page)
    checkout_page.expect_opened()
    expect(checkout_page.billing_address_section).to_be_visible()

    return checkout_page


@pytest.fixture
def checkout_at_shipping_method(checkout_page: CheckoutPage) -> CheckoutPage:
    checkout_page.provide_billing_address(DEFAULT_BILLING_ADDRESS)
    checkout_page.proceed_from_billing_address()

    expect(checkout_page.pickup_in_store_checkbox).not_to_be_checked()
    checkout_page.proceed_from_shipping_address()

    return checkout_page


@pytest.fixture
def checkout_at_payment_method(checkout_at_shipping_method: CheckoutPage) -> CheckoutPage:
    checkout_page = checkout_at_shipping_method
    checkout_page.select_next_day_air_shipping()

    expect(checkout_page.next_day_air_shipping_radio).to_be_checked()
    checkout_page.proceed_from_shipping_method()

    return checkout_page


@pytest.fixture
def checkout_at_confirm_order(checkout_at_payment_method: CheckoutPage) -> CheckoutPage:
    checkout_page = checkout_at_payment_method
    checkout_page.select_cash_on_delivery()
    checkout_page.proceed_from_payment_method()

    expect(checkout_page.cod_payment_info).to_be_visible()
    checkout_page.proceed_from_payment_info()

    expect(checkout_page.confirm_order_section).to_be_visible()

    return checkout_page
