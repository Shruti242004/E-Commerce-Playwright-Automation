import pytest
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.config import Config

@pytest.mark.checkout
class TestCheckout:
    """Test suite covering the complete end-to-end checkout flow and input validations."""

    def test_complete_checkout_end_to_end(
        self,
        authenticated_page: ProductsPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage
    ):
        """Test full end-to-end purchasing workflow from product selection to order confirmation."""
        product_name = "Sauce Labs Backpack"
        
        # 1. Add product to cart
        authenticated_page.add_product_to_cart(product_name)
        authenticated_page.go_to_cart()
        
        # 2. Proceed to checkout Step 1
        cart_page.proceed_to_checkout()
        
        # 3. Enter shipping / customer details
        checkout_page.fill_customer_info("Jane", "Smith", "10001")
        checkout_page.click_continue()
        
        # 4. Step 2 Overview verification
        overview_items = checkout_page.get_overview_item_names()
        assert product_name in overview_items
        
        price_summary = checkout_page.get_price_summary()
        assert price_summary["subtotal"] > 0
        assert price_summary["tax"] > 0
        assert round(price_summary["subtotal"] + price_summary["tax"], 2) == round(price_summary["total"], 2)
        
        # 5. Finish order
        checkout_page.click_finish()
        
        # 6. Step 3 Confirmation verification
        assert checkout_page.is_order_successful()
        assert "Thank you for your order!" in checkout_page.get_confirmation_header()
        
        # 7. Return to Products Catalog
        checkout_page.back_to_home()
        assert authenticated_page.is_inventory_displayed()
        assert authenticated_page.get_cart_count() == 0

    def test_checkout_validation_missing_first_name(
        self,
        authenticated_page: ProductsPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage
    ):
        """Test validation error when First Name is left empty on Checkout Step 1."""
        authenticated_page.add_product_to_cart("Sauce Labs Bike Light")
        authenticated_page.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_page.fill_customer_info(first_name="", last_name="Doe", postal_code="90210")
        checkout_page.click_continue()
        
        error = checkout_page.get_error_message()
        assert "Error: First Name is required" in error

    def test_checkout_validation_missing_last_name(
        self,
        authenticated_page: ProductsPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage
    ):
        """Test validation error when Last Name is left empty on Checkout Step 1."""
        authenticated_page.add_product_to_cart("Sauce Labs Bike Light")
        authenticated_page.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_page.fill_customer_info(first_name="John", last_name="", postal_code="90210")
        checkout_page.click_continue()
        
        error = checkout_page.get_error_message()
        assert "Error: Last Name is required" in error

    def test_checkout_validation_missing_postal_code(
        self,
        authenticated_page: ProductsPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage
    ):
        """Test validation error when Postal Code is left empty on Checkout Step 1."""
        authenticated_page.add_product_to_cart("Sauce Labs Bike Light")
        authenticated_page.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_page.fill_customer_info(first_name="John", last_name="Doe", postal_code="")
        checkout_page.click_continue()
        
        error = checkout_page.get_error_message()
        assert "Error: Postal Code is required" in error

    def test_checkout_price_calculation_multi_items(
        self,
        authenticated_page: ProductsPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage
    ):
        """Test subtotal and total calculations for multiple items during checkout."""
        items = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
        authenticated_page.add_multiple_products(items)
        authenticated_page.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_page.fill_customer_info("Alice", "Wonderland", "12345")
        checkout_page.click_continue()
        
        prices = checkout_page.get_price_summary()
        # Item total for Backpack ($29.99) + Bike Light ($9.99) = $39.98
        assert prices["subtotal"] == 39.98
        assert round(prices["subtotal"] + prices["tax"], 2) == round(prices["total"], 2)
