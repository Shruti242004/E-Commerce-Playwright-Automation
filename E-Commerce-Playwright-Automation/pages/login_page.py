from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage
from utils.config import Config

class LoginPage(BasePage):
    """Page Object for the SauceDemo Login Page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_container = page.locator("[data-test='error']")
        self.login_logo = page.locator(".login_logo")

    def navigate(self):
        """Opens the login page."""
        self.navigate_to("/")

    def enter_username(self, username: str):
        """Types username into the username field."""
        self.username_input.fill(username)

    def enter_password(self, password: str):
        """Types password into the password field."""
        self.password_input.fill(password)

    def click_login(self):
        """Clicks the login submit button."""
        self.login_button.click()

    def login(self, username: str = Config.STANDARD_USER, password: str = Config.PASSWORD):
        """Performs a full login workflow."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Retrieves text from the error notification container."""
        self.error_container.wait_for(state="visible", timeout=Config.DEFAULT_TIMEOUT)
        return self.error_container.inner_text().strip()

    def is_login_page_displayed(self) -> bool:
        """Checks if login page elements are displayed."""
        return self.login_button.is_visible() and self.username_input.is_visible()
