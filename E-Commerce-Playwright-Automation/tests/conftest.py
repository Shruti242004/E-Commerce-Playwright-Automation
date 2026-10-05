import datetime
import pytest
from pathlib import Path
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.config import Config, SCREENSHOTS_DIR

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configures browser viewport and options."""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720,
        },
        "ignore_https_errors": True,
    }

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Provides an instance of LoginPage."""
    return LoginPage(page)

@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    """Provides an instance of ProductsPage."""
    return ProductsPage(page)

@pytest.fixture
def cart_page(page: Page) -> CartPage:
    """Provides an instance of CartPage."""
    return CartPage(page)

@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    """Provides an instance of CheckoutPage."""
    return CheckoutPage(page)

@pytest.fixture
def authenticated_page(page: Page, login_page: LoginPage, products_page: ProductsPage) -> ProductsPage:
    """Logs into the application with standard user and yields products page."""
    login_page.navigate()
    login_page.login(Config.STANDARD_USER, Config.PASSWORD)
    assert "inventory.html" in page.url
    return products_page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Captures full-page screenshot on test failure and attaches it to pytest-html report.
    """
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = (
                item.nodeid.replace("::", "_")
                .replace(".py", "")
                .replace("/", "_")
                .replace("\\", "_")
                .replace("[", "_")
                .replace("]", "_")
            )
            screenshot_path = SCREENSHOTS_DIR / f"FAILURE_{test_name}_{timestamp}.png"
            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                # pytest-html attachment
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html is not None:
                    extras.append(pytest_html.extras.image(str(screenshot_path)))
            except Exception as e:
                print(f"\n[Warning] Failed to capture failure screenshot: {e}")

    report.extras = extras
