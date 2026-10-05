import pytest
from pages.products_page import ProductsPage

@pytest.mark.products
class TestProducts:
    """Test suite covering product listing, search/filter, and catalog sorting."""

    def test_products_catalog_loaded(self, authenticated_page: ProductsPage):
        """Test that product items are correctly loaded in the catalog."""
        names = authenticated_page.get_all_product_names()
        prices = authenticated_page.get_all_product_prices()
        
        assert len(names) > 0, "No products found in catalog"
        assert len(names) == len(prices), "Product count does not match price count"
        assert "Sauce Labs Backpack" in names

    def test_product_search_and_filter_matching(self, authenticated_page: ProductsPage):
        """Test search and filter functionality with matching keyword."""
        search_term = "Backpack"
        results = authenticated_page.search_and_filter_products(search_term)
        
        assert len(results) > 0, f"Expected results for '{search_term}', found none"
        for item in results:
            assert search_term.lower() in item.lower()

    def test_product_search_no_results(self, authenticated_page: ProductsPage):
        """Test search and filter when no items match search query."""
        results = authenticated_page.search_and_filter_products("NonExistentProductXYZ")
        assert len(results) == 0

    def test_sort_products_name_a_to_z(self, authenticated_page: ProductsPage):
        """Test sorting products by Name (A to Z)."""
        authenticated_page.select_sort_option(ProductsPage.SORT_NAME_A_TO_Z)
        names = authenticated_page.get_all_product_names()
        
        assert names == sorted(names), "Products are not sorted alphabetically A to Z"

    def test_sort_products_name_z_to_a(self, authenticated_page: ProductsPage):
        """Test sorting products by Name (Z to A)."""
        authenticated_page.select_sort_option(ProductsPage.SORT_NAME_Z_TO_A)
        names = authenticated_page.get_all_product_names()
        
        assert names == sorted(names, reverse=True), "Products are not sorted alphabetically Z to A"

    def test_sort_products_price_low_to_high(self, authenticated_page: ProductsPage):
        """Test sorting products by Price (low to high)."""
        authenticated_page.select_sort_option(ProductsPage.SORT_PRICE_LOW_TO_HIGH)
        prices = authenticated_page.get_all_product_prices()
        
        assert prices == sorted(prices), f"Prices are not sorted low to high: {prices}"

    def test_sort_products_price_high_to_low(self, authenticated_page: ProductsPage):
        """Test sorting products by Price (high to low)."""
        authenticated_page.select_sort_option(ProductsPage.SORT_PRICE_HIGH_TO_LOW)
        prices = authenticated_page.get_all_product_prices()
        
        assert prices == sorted(prices, reverse=True), f"Prices are not sorted high to low: {prices}"
