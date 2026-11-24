import allure

from playwright.sync_api import expect
from utils.allure_labels import EPIC, Feature, Severity, Story

pytestmark = [
    allure.epic(EPIC),
    allure.feature(Feature.HOME),
]


@allure.story(Story.HOME_PAGE)
@allure.title("Home page has the shop's title")
@allure.severity(Severity.NORMAL)
def test_home_page_title(page, home_page):
    expect(page).to_have_title("Demo Web Shop")
