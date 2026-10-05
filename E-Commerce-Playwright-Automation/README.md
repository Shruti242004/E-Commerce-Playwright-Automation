# E-Commerce Playwright Automation Framework

![Playwright](https://img.shields.io/badge/Playwright-1.59+-green.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Pytest](https://img.shields.io/badge/Pytest-8.0%2B-orange.svg)
![Design Pattern](https://img.shields.io/badge/Architecture-Page%20Object%20Model%20(POM)-purple.svg)

An enterprise-grade, clean, and maintainable test automation suite using **Python**, **Playwright**, and **Pytest** implementing the **Page Object Model (POM)** design pattern against a live e-commerce application ([SauceDemo](https://www.saucedemo.com)).

---

## 📁 Project Structure

```text
E-Commerce-Playwright-Automation/
│
├── tests/
│   ├── conftest.py          # Pytest fixtures, browser setup & screenshot hooks
│   ├── test_login.py        # Authentication, invalid credentials, and logout
│   ├── test_products.py     # Product catalog listing, search/filter & sorting
│   ├── test_cart.py         # Add/remove items, badge count & cart view
│   └── test_checkout.py     # Multi-step checkout, price math & validations
│
├── pages/
│   ├── base_page.py         # Base Page Object with reusable helper methods
│   ├── login_page.py        # Login Page locators & interactions
│   ├── products_page.py     # Inventory catalog, search & sorting locators
│   ├── cart_page.py         # Shopping cart locators & removal actions
│   └── checkout_page.py     # Multi-step checkout forms & overview assertions
│
├── utils/
│   └── config.py            # Central configuration, URLs, credentials, timeouts
│
├── screenshots/             # Auto-generated screenshots on test failures
├── reports/                 # Auto-generated HTML execution reports
│
├── requirements.txt         # Project dependencies
├── pytest.ini               # Pytest configuration and execution flags
├── README.md                # Comprehensive documentation
└── .gitignore               # Ignored files (reports, screenshots, venv, cache)
```

---

## 🚀 Covered Test Scenarios

| Category | Test Case | Description |
|---|---|---|
| **Authentication** | `test_valid_login` | Verify standard user can successfully log in and redirect to catalog |
| | `test_invalid_login_wrong_credentials` | Verify error message on invalid username/password |
| | `test_invalid_login_locked_out_user` | Verify error notification for locked-out user account |
| | `test_invalid_login_empty_fields` | Verify validation warning when submitting blank credentials |
| | `test_invalid_login_missing_password` | Verify validation warning when password is omitted |
| | `test_logout` | Verify logout redirects back to login and clears session |
| **Products & Search** | `test_products_catalog_loaded` | Verify all product titles and prices render properly |
| | `test_product_search_and_filter_matching` | Verify keyword search returns correct matching items |
| | `test_product_search_no_results` | Verify searching non-existent items returns empty results |
| | `test_sort_products_name_a_to_z` | Verify catalog sorting from A to Z |
| | `test_sort_products_name_z_to_a` | Verify catalog sorting from Z to A |
| | `test_sort_products_price_low_to_high` | Verify catalog sorting from Lowest to Highest Price |
| | `test_sort_products_price_high_to_low` | Verify catalog sorting from Highest to Lowest Price |
| **Shopping Cart** | `test_add_single_product_to_cart` | Verify adding an item updates badge and cart list |
| | `test_add_multiple_products_to_cart` | Verify multi-item addition and cart badge synchronization |
| | `test_remove_product_from_catalog_page` | Verify removing items directly from the catalog page |
| | `test_remove_product_from_cart_page` | Verify removing items from the cart overview page |
| | `test_continue_shopping_navigation` | Verify returning to catalog via "Continue Shopping" |
| **Checkout Flow** | `test_complete_checkout_end_to_end` | Complete full multi-step checkout workflow with order confirmation |
| | `test_checkout_validation_missing_first_name` | Verify Step 1 validation for missing First Name |
| | `test_checkout_validation_missing_last_name` | Verify Step 1 validation for missing Last Name |
| | `test_checkout_validation_missing_postal_code` | Verify Step 1 validation for missing Postal Code |
| | `test_checkout_price_calculation_multi_items` | Verify mathematical calculation of Subtotal + Tax = Total |

---

## 🛠️ Setup & Installation

### 1. Clone & Navigate
```bash
git clone <repository_url>
cd E-Commerce-Playwright-Automation
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies & Playwright Browsers
```bash
pip install -r requirements.txt
playwright install chromium
```

---

## 🧪 Running Tests

### Run all tests (Headless mode with HTML Report)
```bash
pytest
```

### Run tests in Headed mode (Visible Browser)
```bash
pytest --headed
```

### Run a specific test file
```bash
pytest tests/test_login.py
pytest tests/test_checkout.py
```

### Run by Pytest Marker
```bash
pytest -m login
pytest -m products
pytest -m cart
pytest -m checkout
```

### Run tests in Parallel (Multi-threaded)
```bash
pytest -n auto
```

---

## 📊 Test Reports & Screenshots

1. **HTML Test Report**: Automatically saved to `reports/report.html`. Open it in any browser:
   ```bash
   # Windows
   start reports/report.html
   ```
2. **Failure Screenshots**: If any test fails, `pytest_runtest_makereport` automatically captures a full-page screenshot into `screenshots/` and attaches it directly to the HTML report.

---

## 🏗️ Architecture & Best Practices

- **Page Object Model (POM)**: Complete separation between test logic and web elements.
- **Robust Locators**: Prioritizes test IDs, semantic CSS, and role-based locators.
- **Auto-Wait & Dynamic Assertions**: Uses Playwright's built-in auto-waiting to eliminate flaky sleeps.
- **Config Driven**: Centralized URLs, credentials, and timeouts in `utils/config.py`.
