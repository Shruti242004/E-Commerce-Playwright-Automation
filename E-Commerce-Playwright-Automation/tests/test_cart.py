import pytest
from pages.products_page import ProductsPage
from pages.cart_page import CartPage

@pytest.mark.cart
class TestCart:
    """Test suite covering cart management: adding, viewing, and removing products."""

    def test_add_single_product_to_cart(self, authenticated_page: ProductsPage, cart_page: CartPage):
        """Test adding a single product to cart and verifying in cart view."""
        product_to_add = "Sauce Labs Backpack"
        
        authenticated_page.add_product_to_cart(product_to_add)
        assert authenticated_page.get_cart_count() == 1
        assert authenticated_page.is_remove_button_visible_for_product(product_to_add)
        
        authenticated_page.go_to_cart()
        cart_items = cart_page.get_cart_items_names()
        assert product_to_add in cart_items
        assert cart_page.get_cart_items_count() == 1

    def test_add_multiple_products_to_cart(self, authenticated_page: ProductsPage, cart_page: CartPage):
        """Test adding multiple products to cart and verifying total badge count."""
        products_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt"
        ]
        
        authenticated_page.add_multiple_products(products_to_add)
        assert authenticated_page.get_cart_count() == len(products_to_add)
        
        authenticated_page.go_to_cart()
        cart_items = cart_page.get_cart_items_names()
        assert len(cart_items) == len(products_to_add)
        for product in products_to_add:
            assert product in cart_items

    def test_remove_product_from_catalog_page(self, authenticated_page: ProductsPage):
        """Test removing an added product directly from the product catalog page."""
        product = "Sauce Labs Onesie"
        
        authenticated_page.add_product_to_cart(product)
        assert authenticated_page.get_cart_count() == 1
        
        authenticated_page.remove_product_from_catalog(product)
        assert authenticated_page.get_cart_count() == 0

    def test_remove_product_from_cart_page(self, authenticated_page: ProductsPage, cart_page: CartPage):
        """Test removing an item from within the cart page."""
        products = ["Sauce Labs Fleece Jacket", "Sauce Labs Bike Light"]
        authenticated_page.add_multiple_products(products)
        
        authenticated_page.go_to_cart()
        assert cart_page.get_cart_items_count() == 2
        
        # Remove one item
        cart_page.remove_item("Sauce Labs Bike Light")
        assert cart_page.get_cart_items_count() == 1
        assert "Sauce Labs Bike Light" not in cart_page.get_cart_items_names()
        assert "Sauce Labs Fleece Jacket" in cart_page.get_cart_items_names()

    def test_continue_shopping_navigation(self, authenticated_page: ProductsPage, cart_page: CartPage):
        """Test navigating back to product catalog from cart via 'Continue Shopping'."""
        authenticated_page.go_to_cart()
        cart_page.continue_shopping()
        
        assert authenticated_page.is_inventory_displayed()
        assert "inventory.html" in cart_page.get_url()
