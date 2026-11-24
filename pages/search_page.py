from pages.base_page import BasePage
from utils.allure_helpers import step


class SearchPage(BasePage):
    PATH = "/search"
    TITLE = "Search"

    def __init__(self, page):
        super().__init__(page)

        self.search_input = page.locator("#small-searchterms")
        self.search_button = page.get_by_role("button", name="Search")
        self.search_results = page.locator(".product-item")
        self.no_results_message = page.locator(".result")

    @step("Search for '{query}'")
    def search(self, query: str) -> None:
        self.search_input.fill(query)
        self.search_button.click()

    @step("Open the first search result")
    def open_first_product(self) -> None:
        self.search_results.first.get_by_role("link").first.click()
