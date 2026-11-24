import allure
import pytest

from playwright.sync_api import expect

from utils.allure_labels import EPIC, Feature, Severity, Story
from utils.test_data import build_user

pytestmark = [
    allure.epic(EPIC),
    allure.feature(Feature.REGISTRATION),
]


@allure.story(Story.REGISTER)
@allure.title("User can register with valid data")
@allure.severity(Severity.CRITICAL)
def test_user_can_register(registration_page):
    registration_page.register(build_user())

    expect(registration_page.registration_result).to_have_text(
        "Your registration completed"
    )


@allure.story(Story.REGISTER)
@allure.title("User cannot register with invalid data")
@allure.severity(Severity.NORMAL)
@pytest.mark.parametrize(
    "invalid_fields",
    [
        pytest.param(
            {"confirm_password": "DifferentPassword123!"},
            id="mismatched_passwords",
        ),
        pytest.param({"password": "12345"}, id="short_password"),
        pytest.param({"email": ""}, id="missing_email"),
        pytest.param({"password": ""}, id="missing_password"),
    ],
)
def test_user_cannot_register_with_invalid_data(registration_page, invalid_fields):
    registration_page.register(build_user(**invalid_fields))

    expect(registration_page.field_validation_errors).not_to_have_count(0)
