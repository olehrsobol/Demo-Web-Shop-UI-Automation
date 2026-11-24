from pages.email_wishlist_page import EmailWishlistPage
from pages.items_table_page import ItemsTablePage
from utils.allure_helpers import step


class WishlistPage(ItemsTablePage):
    PATH = "/wishlist"
    TITLE = "Wishlist"

    def __init__(self, page):
        super().__init__(
            page,
            product_names=page.locator(".cart-item-row .product"),
            update_button=page.locator(".update-wishlist-button"),
        )

        self.add_to_cart_checkboxes = page.locator(
            ".add-to-cart input[type='checkbox']"
        )
        self.add_to_cart_button = page.locator(
            ".wishlist-add-to-cart-button"
        )
        self.email_a_friend_button = page.locator(
            ".email-a-friend-wishlist-button"
        )
        self.share_link = page.locator(".share-link")

    @step("Select the item for the cart")
    def select_item_for_cart(self, index: int = 0) -> None:
        self.add_to_cart_checkboxes.nth(index).check()

    @step("Add selected items to the cart")
    def add_selected_items_to_cart(self) -> None:
        self.add_to_cart_button.click()

    @step("Click 'Email a friend'")
    def click_email_a_friend(self) -> EmailWishlistPage:
        self.email_a_friend_button.click()

        return EmailWishlistPage(self.page)