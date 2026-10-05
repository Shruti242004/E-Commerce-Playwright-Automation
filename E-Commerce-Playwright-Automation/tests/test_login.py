import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import Config

@pytest.mark.login
class TestLogin:
    """Test suite covering authentication scenarios: valid login, invalid login, and logout."""

    def test_valid_login(self, login_page: LoginPage, products_page: ProductsPage):
        """Test successful login with standard user credentials."""
        login_page.navigate()
        login_page.login(Config.STANDARD_USER, Config.PASSWORD)
        
        # Verify user is redirected to the products/inventory page
        expect(login_page.page).to_have_url(f"{Config.BASE_URL}/inventory.html")
        assert products_page.is_inventory_displayed()
        assert products_page.get_header_title() == "Products"

    def test_invalid_login_wrong_credentials(self, login_page: LoginPage):
        """Test login failure with invalid username and password."""
        login_page.navigate()
        login_page.login("invalid_user", "wrong_password")
        
        error_msg = login_page.get_error_message()
        assert "Username and password do not match any user in this service" in error_msg

    def test_invalid_login_locked_out_user(self, login_page: LoginPage):
        """Test login error for locked-out user account."""
        login_page.navigate()
        login_page.login(Config.LOCKED_OUT_USER, Config.PASSWORD)
        
        error_msg = login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error_msg

    def test_invalid_login_empty_fields(self, login_page: LoginPage):
        """Test validation when submitting empty login fields."""
        login_page.navigate()
        login_page.click_login()
        
        error_msg = login_page.get_error_message()
        assert "Username is required" in error_msg

    def test_invalid_login_missing_password(self, login_page: LoginPage):
        """Test validation when username is provided without password."""
        login_page.navigate()
        login_page.enter_username(Config.STANDARD_USER)
        login_page.click_login()
        
        error_msg = login_page.get_error_message()
        assert "Password is required" in error_msg

    def test_logout(self, login_page: LoginPage, authenticated_page: ProductsPage):
        """Test logout functionality from the sidebar menu."""
        # User is already logged in via authenticated_page fixture
        assert authenticated_page.is_inventory_displayed()
        
        # Perform logout
        authenticated_page.logout()
        
        # Verify user is redirected back to login page
        expect(login_page.page).to_have_url(f"{Config.BASE_URL}/")
        assert login_page.is_login_page_displayed()
