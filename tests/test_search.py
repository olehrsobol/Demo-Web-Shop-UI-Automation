import allure
import pytest

from playwright.sync_api import expect

from utils.allure_labels import EPIC, Feature, Severity, Story
from utils.test_data import SMARTPHONE_QUERY

pytestmark = [
    allure.epic(EPIC),
    allure.feature(Feature.SEARCH),
]


# Find products
@allure.story(Story.FIND_PRODUCTS)
@allure.title("User can search for a product")
@allure.severity(Severity.CRITICAL)
@pytest.mark.parametrize(
    "query",
    [
        pytest.param(SMARTPHONE_QUERY, id="full_name"),
        pytest.param("smart", id="partial_name"),
    ],
)
def test_user_can_search_for_product(search_page, query):
    search_page.search(query)

    expect(search_page.search_results.first).to_be_visible()
    expect(search_page.search_results).not_to_have_count(0)


@allure.story(Story.FIND_PRODUCTS)
@allure.title("Search shows 'no results' for an unknown product")
@allure.severity(Severity.NORMAL)
def test_search_returns_no_results_for_unknown_product(search_page):
    search_page.search("xyznonexistentproduct123")

    expect(search_page.no_results_message).to_contain_text(
        "No products were found that matched your criteria."
    )


@allure.story(Story.FIND_PRODUCTS)
@allure.title("Search with an empty query keeps the user on the page")
@allure.severity(Severity.MINOR)
def test_search_with_empty_query(search_page):
    search_page.search("")

    expect(search_page.search_input).to_be_visible()


# Product details
@allure.story(Story.PRODUCT_DETAILS)
@allure.title("User can open product details from the search results")
@allure.severity(Severity.CRITICAL)
def test_user_can_open_product_details_from_search_results(smartphone_product_page):
    expect(smartphone_product_page.product_name).to_be_visible()
