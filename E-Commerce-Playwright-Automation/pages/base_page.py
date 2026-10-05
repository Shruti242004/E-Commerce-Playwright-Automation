from pathlib import Path
from playwright.sync_api import Page, Locator, expect
from utils.config import Config, SCREENSHOTS_DIR

class BasePage:
    """Base Page Object containing shared methods and locators across all pages."""

    def __init__(self, page: Page):
        self.page = page
        self.burger_menu_button = page.locator("#react-burger-menu-btn")
        self.logout_sidebar_link = page.locator("#logout_sidebar_link")
        self.shopping_cart_link = page.locator(".shopping_cart_link")
        self.shopping_cart_badge = page.locator(".shopping_cart_badge")

    def navigate_to(self, path: str = ""):
        """Navigates to relative or absolute path."""
        url = f"{Config.BASE_URL}{path}" if not path.startswith("http") else path
        self.page.goto(url, wait_until="domcontentloaded", timeout=Config.NAVIGATION_TIMEOUT)

    def get_title(self) -> str:
        """Returns the page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Returns the current page URL."""
        return self.page.url

    def open_burger_menu(self):
        """Opens the hamburger menu."""
        self.burger_menu_button.click()
        self.logout_sidebar_link.wait_for(state="visible", timeout=Config.DEFAULT_TIMEOUT)

    def logout(self):
        """Logs out from the application via burger menu."""
        self.open_burger_menu()
        self.logout_sidebar_link.click()

    def get_cart_count(self) -> int:
        """Returns the current shopping cart badge count as an integer, 0 if not present."""
        if self.shopping_cart_badge.is_visible():
            text = self.shopping_cart_badge.inner_text().strip()
            return int(text) if text.isdigit() else 0
        return 0

    def go_to_cart(self):
        """Clicks the shopping cart badge/icon."""
        self.shopping_cart_link.click()

    def take_screenshot(self, name: str) -> str:
        """Takes a full page screenshot saved to screenshots/ directory."""
        file_path = SCREENSHOTS_DIR / f"{name}.png"
        self.page.screenshot(path=str(file_path), full_page=True)
        return str(file_path)
