from dataclasses import dataclass, replace
from datetime import datetime

from config.settings import TEST_USER_EMAIL

# Search queries
SMARTPHONE_QUERY = "smartphone"
COMPUTER_QUERY = "computer"

# Credentials
DEFAULT_PASSWORD = "Password123!"
INVALID_PASSWORD = "WrongPassword"
UNKNOWN_USER_EMAIL = "invalid-user@gmail.com"


def generate_unique_email() -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

    return f"JohnDoe_{timestamp}@gmail.com"


# Registration
@dataclass(frozen=True)
class UserData:
    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str


def build_user(**overrides) -> UserData:
    password = overrides.get("password", DEFAULT_PASSWORD)

    defaults = UserData(
        first_name="John",
        last_name="Doe",
        email=generate_unique_email(),
        password=password,
        confirm_password=password,
    )

    return replace(defaults, **overrides)


# Checkout
@dataclass(frozen=True)
class Address:
    first_name: str
    last_name: str
    email: str
    country: str
    state: str
    city: str
    address_1: str
    zip_code: str
    phone: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass(frozen=True)
class CreditCard:
    card_type: str
    holder_name: str
    number: str
    code: str
    expiration_month: str
    expiration_year: str


DEFAULT_BILLING_ADDRESS = Address(
    first_name="John",
    last_name="Doe",
    email=TEST_USER_EMAIL,
    country="Ukraine",
    state="Other (Non US)",
    city="Kharkiv",
    address_1="Test Street 123",
    zip_code="61000",
    phone="0123456789",
)

DEFAULT_CREDIT_CARD = CreditCard(
    card_type="Visa",
    holder_name="John Doe",
    number="4111111111111111",
    code="123",
    expiration_month="12",
    expiration_year="2030",
)

PURCHASE_ORDER_NUMBER = "PO-2026-001"
