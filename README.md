# Demo-Web-Shop-Playwright-Automation

End-to-end UI automation project for the <a href="https://demowebshop.tricentis.com/">Demo Web Shop by Tricentis</a> built with Python, Playwright, and Pytest.

The project demonstrates a maintainable QA automation framework with Page Object Model (POM), reusable pytest fixtures, test isolation, and Allure reporting.

> <strong>Tech Stack:</strong>
<ul>
  <li>Python</li>
  <li>Playwright</li>
  <li>Pytest</li>
  <li>Allure Report</li>
  <li>Page Object Model (POM)</li>
  <li>Pytest Fixtures</li>
  <li>Git / GitHub</li>
  <li>.env configuration
</ul>

## Test Coverage

More than 50 automated test cases covering the key e-commerce user flows.

**Home page**
- Page title

**Login**
- Login with valid credentials and "Remember me"
- Login with invalid credentials
- Login with empty fields
- Logout

**Registration**
- Registration with valid data
- Validation of invalid data (mismatched passwords, short password, missing email, missing password)

**Search**
- Product search and partial product search
- Empty search
- Search with no results
- Opening product details

**Shopping Cart**
- Adding products to the cart
- Verifying product data
- Removing products
- Updating product quantity
- Price and total verification

**Wishlist**
- Adding and removing products
- Updating quantity and total recalculation
- Moving products from the wishlist to the cart
- Email a Friend form (validation, optional message)
- Wishlist sharing link

**Checkout**
- Terms of service validation
- Redirect of a guest user to the login page
- Billing address
- Shipping address and shipping method
- Payment methods (COD, Check / Money Order, Credit Card, Purchase Order)
- Order confirmation, order total calculation
- Order completion

## Framework Features

- Page Object Model: all UI interactions live in page objects, tests contain only scenarios and assertions
- Shared base for the cart and wishlist pages (`ItemsTablePage`)
- Layered fixtures: each test asks only for the state it needs (for example, `checkout_at_payment_method`)
- Automatic cleanup of the user's cart and wishlist before and after tests
- Dynamic test data (unique emails) and typed test data models (dataclasses)
- Parametrized tests for repeated scenarios
- Web-first assertions with Playwright `expect` (auto-waiting, no `sleep`)
- Exact price arithmetic with `Decimal`
- Allure report: Epic → Feature → Story hierarchy, test titles and severity, steps for meaningful user actions only
- Failure diagnostics: screenshot, page URL and page HTML in Allure, Playwright trace retained on failure
- Credentials and sensitive data are kept out of the report
- Configuration through environment variables
- CI: GitHub Actions workflow with Allure report as a build artifact (optional publishing to GitHub Pages)

## Project Structure

```
.
├── .github/workflows/tests.yml   # CI pipeline
├── config/
│   └── settings.py               # base URL and test account (from env variables)
├── pages/                        # page objects
├── tests/                        # test scenarios (one module per feature)
├── utils/
│   ├── allure_helpers.py         # @step decorator
│   ├── allure_labels.py          # Epic / Feature / Story / Severity constants
│   ├── price.py                  # price parsing
│   └── test_data.py              # test data models and constants
├── .env                          # configuration file (credentials)
├── conftest.py                   # fixtures, failure artifacts, Allure environment
├── pytest.ini
└── requirements.txt
```

## Running the Tests

```bash
# 1. Install
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium

# 2. Configure the test account (an existing account on the site)
export TEST_USER_EMAIL="your-email"
export TEST_USER_PASSWORD="your-password"
# PowerShell: $env:TEST_USER_EMAIL="your-email"; $env:TEST_USER_PASSWORD="your-password"

# 3. Run
pytest -v
pytest --headed                    # with a visible browser
pytest -k checkout                 # only a part of the suite

# 4. Open the Allure report (requires Allure CLI)
allure serve allure-results
```

The account used by the tests must exist on the site and either have no saved billing address or have one matching `utils/test_data.py`. All runs share one account, so tests must run sequentially (not in parallel).

> <strong>Purpose</strong>

This project is a QA automation portfolio piece. It shows how to structure a UI test framework that is readable, maintainable, and easy to extend, and how to make test results transparent with Allure reports and failure diagnostics.
The Demo Web Shop is a public training site provided by Tricentis; this project is not affiliated with it.
