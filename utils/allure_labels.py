import allure

EPIC = "Demo Web Shop"

Severity = allure.severity_level


class Feature:
    HOME = "Home page"
    LOGIN = "Login"
    REGISTRATION = "Registration"
    SEARCH = "Search"
    CART = "Cart"
    WISHLIST = "Wishlist"
    CHECKOUT = "Checkout"


class Story:
    # Home
    HOME_PAGE = "Home page"
    # Login
    LOG_IN = "Log in"
    LOG_OUT = "Log out"
    # Registration
    REGISTER = "Register an account"
    # Search
    FIND_PRODUCTS = "Find products"
    PRODUCT_DETAILS = "Product details"
    # Cart
    ADD_TO_CART = "Add to cart"
    EDIT_CART = "Edit the cart"
    # Wishlist
    MANAGE_WISHLIST = "Manage the wishlist"
    MOVE_TO_CART = "Move to cart"
    EMAIL_WISHLIST = "Email the wishlist to a friend"
    # Checkout
    START_CHECKOUT = "Start checkout"
    BILLING_ADDRESS = "Billing address"
    SHIPPING_METHOD = "Shipping method"
    PAYMENT_METHOD = "Payment method"
    CONFIRM_ORDER = "Confirm the order"
