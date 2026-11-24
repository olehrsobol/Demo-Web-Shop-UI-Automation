import re
import allure
import pytest

from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.wishlist_page import WishlistPage
from utils.allure_labels import EPIC, Feature, Severity, Story

pytestmark = [
    allure.epic(EPIC),
    allure.feature(Feature.WISHLIST),
]

FRIEND_EMAIL = "friend@example.com"
INVALID_EMAIL = "invalid-email"


# Manage the wishlist
@allure.story(Story.MANAGE_WISHLIST)
@allure.title("User can open the wishlist")
@allure.severity(Severity.NORMAL)
def test_user_can_open_wishlist(page, logged_in_user):
    wishlist_page = WishlistPage(page)
    wishlist_page.open()
    wishlist_page.expect_opened()


@allure.story(Story.MANAGE_WISHLIST)
@allure.title("User can add a smartphone to the wishlist")
@allure.severity(Severity.CRITICAL)
def test_user_can_add_smartphone_to_wishlist(empty_wishlist, smartphone_product_page):
    expect(smartphone_product_page.add_to_wishlist_button).to_be_visible()

    smartphone_product_page.add_to_wishlist()

    expect(
        smartphone_product_page.added_to_wishlist_notification
    ).to_be_visible()


@allure.story(Story.MANAGE_WISHLIST)
@allure.title("Added smartphone is displayed in the wishlist")
@allure.severity(Severity.CRITICAL)
def test_added_smartphone_is_displayed_in_wishlist(smartphone_in_wishlist, smartphone_name):
    smartphone_in_wishlist.expect_single_item(smartphone_name)


@allure.story(Story.MANAGE_WISHLIST)
@allure.title("User can change the quantity and the total is recalculated")
@allure.severity(Severity.NORMAL)
def test_user_can_change_wishlist_quantity_and_total_is_recalculated(smartphone_in_wishlist):
    wishlist_page = smartphone_in_wishlist

    unit_price = wishlist_page.get_unit_price_value()

    wishlist_page.set_quantity(2)

    expect(wishlist_page.quantity_inputs.first).to_have_value("2")
    assert wishlist_page.get_total_price_value() == unit_price * 2


@allure.story(Story.MANAGE_WISHLIST)
@allure.title("User can remove a product from the wishlist")
@allure.severity(Severity.NORMAL)
def test_user_can_remove_product_from_wishlist(smartphone_in_wishlist):
    wishlist_page = smartphone_in_wishlist
    wishlist_page.remove_item()
    wishlist_page.expect_empty()


@allure.story(Story.MANAGE_WISHLIST)
@allure.title("Wishlist share link is available")
@allure.severity(Severity.MINOR)
def test_wishlist_share_link_is_available(smartphone_in_wishlist):
    expect(smartphone_in_wishlist.share_link).to_have_attribute(
        "href",
        re.compile(r"^/wishlist/")
    )


# Move to cart
@allure.story(Story.MOVE_TO_CART)
@allure.title("User can add a product from the wishlist to the cart")
@allure.severity(Severity.CRITICAL)
def test_user_can_add_product_from_wishlist_to_cart(page, empty_cart, smartphone_in_wishlist, smartphone_name):
    wishlist_page = smartphone_in_wishlist
    wishlist_page.select_item_for_cart()
    wishlist_page.add_selected_items_to_cart()

    cart_page = CartPage(page)
    cart_page.expect_opened()
    cart_page.expect_single_item(smartphone_name)


@allure.story(Story.MOVE_TO_CART)
@allure.title("Wishlist quantity is preserved when the product is moved to the cart")
@allure.severity(Severity.NORMAL)
def test_wishlist_quantity_is_preserved_when_product_is_added_to_cart(page, empty_cart, smartphone_in_wishlist, smartphone_name):
    wishlist_page = smartphone_in_wishlist
    wishlist_page.set_quantity(2)
    expect(wishlist_page.quantity_inputs.first).to_have_value("2")

    wishlist_page.select_item_for_cart()
    wishlist_page.add_selected_items_to_cart()

    cart_page = CartPage(page)
    cart_page.expect_single_item(smartphone_name)
    expect(cart_page.quantity_inputs.first).to_have_value("2")


# Email the wishlist to a friend
@pytest.fixture
def email_form(smartphone_in_wishlist):
    return smartphone_in_wishlist.click_email_a_friend()


@allure.story(Story.EMAIL_WISHLIST)
@allure.title("User can open the 'Email a friend' page")
@allure.severity(Severity.MINOR)
def test_user_can_open_email_a_friend_page(email_form):
    email_form.expect_opened()

    expect(email_form.friend_email_input).to_be_visible()
    expect(email_form.your_email_input).to_be_visible()
    expect(email_form.personal_message_input).to_be_visible()
    expect(email_form.send_email_button).to_be_visible()


@allure.story(Story.EMAIL_WISHLIST)
@allure.title("User can fill in the 'Email a friend' form")
@allure.severity(Severity.MINOR)
def test_user_can_fill_email_a_friend_form(email_form):
    personal_message = "Check out my wishlist!"

    email_form.fill_form(
        friend_email=FRIEND_EMAIL,
        personal_message=personal_message
    )

    expect(email_form.friend_email_input).to_have_value(FRIEND_EMAIL)
    expect(email_form.your_email_input).not_to_have_value("")
    expect(email_form.personal_message_input).to_have_value(personal_message)


@allure.story(Story.EMAIL_WISHLIST)
@allure.title("Friend's email is validated")
@allure.severity(Severity.NORMAL)
@pytest.mark.parametrize(
    "friend_email, expected_message",
    [
        pytest.param("", "Enter friend's email", id="required"),
        pytest.param(INVALID_EMAIL, "Wrong email", id="invalid_format"),
    ],
)
def test_friend_email_is_validated(email_form, friend_email, expected_message):
    email_form.fill_form(friend_email=friend_email)
    email_form.send()

    expect(email_form.friend_email_validation_message).to_have_text(
        expected_message
    )


@allure.story(Story.EMAIL_WISHLIST)
@allure.title("User's own email is validated")
@allure.severity(Severity.NORMAL)
@pytest.mark.parametrize(
    "your_email, expected_message",
    [
        pytest.param("", "Enter your email", id="required"),
        pytest.param(INVALID_EMAIL, "Wrong email", id="invalid_format"),
    ],
)
def test_your_email_is_validated(email_form, your_email, expected_message):
    email_form.fill_form(friend_email=FRIEND_EMAIL, your_email=your_email)
    email_form.send()

    expect(email_form.your_email_validation_message).to_have_text(
        expected_message
    )


@allure.story(Story.EMAIL_WISHLIST)
@allure.title("Personal message is optional")
@allure.severity(Severity.NORMAL)
def test_personal_message_is_optional(email_form):
    email_form.fill_form(friend_email=FRIEND_EMAIL)
    expect(email_form.personal_message_input).to_have_value("")

    email_form.send()
    expect(email_form.sent_confirmation).to_be_visible()
