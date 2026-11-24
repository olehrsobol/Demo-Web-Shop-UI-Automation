import allure
import pytest

from playwright.sync_api import expect

from config.settings import TEST_USER_EMAIL, TEST_USER_PASSWORD
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.allure_labels import EPIC, Feature, Severity, Story
from utils.test_data import (INVALID_PASSWORD, UNKNOWN_USER_EMAIL)

pytestmark = [
    allure.epic(EPIC),
    allure.feature(Feature.LOGIN),
]


# Log in
@allure.story(Story.LOG_IN)
@allure.title("Login page is reachable from the home page")
@allure.severity(Severity.CRITICAL)
def test_login_page_is_reachable(page, home_page):
    home_page.click_login()

    login_page = LoginPage(page)

    expect(login_page.email_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.login_button).to_be_visible()


@allure.story(Story.LOG_IN)
@allure.title("User can log in with valid credentials")
@allure.severity(Severity.BLOCKER)
def test_user_can_login_with_valid_credentials(page, login_page):
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)

    expect(HomePage(page).logout_link).to_be_visible()


@allure.story(Story.LOG_IN)
@allure.title("User can log in with 'Remember me' checked")
@allure.severity(Severity.NORMAL)
def test_user_can_login_with_remember_me(page, login_page):
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD, remember_me=True)

    expect(HomePage(page).logout_link).to_be_visible()


@allure.story(Story.LOG_IN)
@allure.title("User cannot log in with invalid credentials")
@allure.severity(Severity.CRITICAL)
@pytest.mark.parametrize(
    "email, password",
    [
        pytest.param(TEST_USER_EMAIL, INVALID_PASSWORD, id="invalid_password"),
        pytest.param(UNKNOWN_USER_EMAIL, TEST_USER_PASSWORD, id="invalid_email"),
    ],
)
def test_user_cannot_login_with_invalid_credentials(page, login_page, email, password):
    login_page.login(email, password)

    expect(login_page.validation_summary).to_be_visible()
    expect(HomePage(page).login_link).to_be_visible()


@allure.story(Story.LOG_IN)
@allure.title("User cannot log in with empty fields")
@allure.severity(Severity.NORMAL)
@pytest.mark.parametrize(
    "email, password",
    [
        pytest.param("", TEST_USER_PASSWORD, id="empty_email"),
        pytest.param(TEST_USER_EMAIL, "", id="empty_password"),
        pytest.param("", "", id="empty_credentials"),
    ],
)
def test_user_cannot_login_with_empty_fields(page, login_page, email, password):
    login_page.login(email, password)

    expect(login_page.email_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(HomePage(page).logout_link).not_to_be_visible()


# Log out
@allure.story(Story.LOG_OUT)
@allure.title("User can log out")
@allure.severity(Severity.CRITICAL)
def test_user_can_logout(logged_in_user):
    logged_in_user.click_logout()

    expect(logged_in_user.login_link).to_be_visible()
