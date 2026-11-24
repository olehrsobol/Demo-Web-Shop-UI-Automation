import allure

from playwright.sync_api import expect

from utils.allure_labels import EPIC, Feature, Severity, Story

pytestmark = [
    allure.epic(EPIC),
    allure.feature(Feature.CART),
]


# Add to cart
@allure.story(Story.ADD_TO_CART)
@allure.title("User can add a product to the cart")
@allure.severity(Severity.BLOCKER)
def test_user_can_add_product_to_cart(empty_cart, smartphone_product_page, smartphone_name):
    smartphone_product_page.add_to_cart()

    empty_cart.open()
    empty_cart.expect_single_item(smartphone_name)


@allure.story(Story.ADD_TO_CART)
@allure.title("Product is added to the cart with correct data")
@allure.severity(Severity.CRITICAL)
def test_product_is_added_to_cart_with_correct_data(computer_in_cart, computer_name):
    cart_page = computer_in_cart
    cart_page.expect_single_item(computer_name)
    expect(cart_page.quantity_inputs.first).to_have_value("1")

    unit_price = cart_page.get_unit_price_value()

    assert unit_price > 0
    assert cart_page.get_total_price_value() == unit_price


# Edit the cart
@allure.story(Story.EDIT_CART)
@allure.title("User can remove a product from the cart")
@allure.severity(Severity.CRITICAL)
def test_user_can_remove_product_from_cart(computer_in_cart):
    cart_page = computer_in_cart
    cart_page.remove_item()
    cart_page.expect_empty()


@allure.story(Story.EDIT_CART)
@allure.title("User can change the product quantity and the total is recalculated")
@allure.severity(Severity.NORMAL)
def test_user_can_change_product_quantity_in_cart(computer_in_cart):
    cart_page = computer_in_cart

    original_unit_price = cart_page.get_unit_price_value()

    cart_page.set_quantity(2)

    expect(cart_page.quantity_inputs.first).to_have_value("2")
    assert cart_page.get_unit_price_value() == original_unit_price
    assert cart_page.get_total_price_value() == original_unit_price * 2
