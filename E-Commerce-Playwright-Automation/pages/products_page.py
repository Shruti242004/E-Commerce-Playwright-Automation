from typing import List
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage
from utils.config import Config

class ProductsPage(BasePage):
    """Page Object for the Inventory / Products Catalog Page."""

    # Sorting option values
    SORT_NAME_A_TO_Z = "az"
    SORT_NAME_Z_TO_A = "za"
    SORT_PRICE_LOW_TO_HIGH = "lohi"
    SORT_PRICE_HIGH_TO_LOW = "hilo"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_title = page.locator(".title")
        self.inventory_container = page.locator("#inventory_container").first
        self.inventory_items = page.locator(".inventory_item")
        self.inventory_item_names = page.locator(".inventory_item_name")
        self.inventory_item_prices = page.locator(".inventory_item_price")
        self.sort_select = page.locator("[data-test='product-sort-container']")
        self.active_sort_option = page.locator(".active_option")

    def is_inventory_displayed(self) -> bool:
        """Returns True if the inventory container and title are visible."""
        return self.inventory_container.is_visible() and self.page_title.is_visible()

    def get_header_title(self) -> str:
        """Returns the page subheader title (e.g., 'Products')."""
        return self.page_title.inner_text().strip()

    def get_all_product_names(self) -> List[str]:
        """Returns list of all visible product names."""
        return self.inventory_item_names.all_inner_texts()

    def get_all_product_prices(self) -> List[float]:
        """Returns list of all product prices as floats (e.g., [29.99, 9.99, ...])."""
        price_texts = self.inventory_item_prices.all_inner_texts()
        return [float(p.replace("$", "").strip()) for p in price_texts]

    def select_sort_option(self, value: str):
        """Sorts the catalog using the dropdown option value ('az', 'za', 'lohi', 'hilo')."""
        self.sort_select.select_option(value=value)

    def search_and_filter_products(self, keyword: str) -> List[str]:
        """
        Simulates product search / client-side filtering by matching the keyword
        against product names and descriptions in the catalog.
        """
        self.inventory_items.first.wait_for(state="visible", timeout=Config.DEFAULT_TIMEOUT)
        keyword_lower = keyword.lower()
        matched_products = []
        count = self.inventory_items.count()
        for i in range(count):
            item = self.inventory_items.nth(i)
            name = item.locator(".inventory_item_name").inner_text()
            desc = item.locator(".inventory_item_desc").inner_text()
            if keyword_lower in name.lower() or keyword_lower in desc.lower():
                matched_products.append(name)
        return matched_products

    def _get_item_card_by_name(self, product_name: str) -> Locator:
        """Locates the parent inventory item element containing the product name."""
        return self.inventory_items.filter(has=self.page.locator(".inventory_item_name", has_text=product_name))

    def add_product_to_cart(self, product_name: str):
        """Adds a specific product to the cart by its name."""
        card = self._get_item_card_by_name(product_name)
        card.locator("button:has-text('Add to cart')").click()

    def remove_product_from_catalog(self, product_name: str):
        """Removes a product directly from the catalog page button."""
        card = self._get_item_card_by_name(product_name)
        card.locator("button:has-text('Remove')").click()

    def is_remove_button_visible_for_product(self, product_name: str) -> bool:
        """Checks if the 'Remove' button is visible on the product card."""
        card = self._get_item_card_by_name(product_name)
        return card.locator("button:has-text('Remove')").is_visible()

    def add_multiple_products(self, product_names: List[str]):
        """Adds multiple products to cart given a list of names."""
        for name in product_names:
            self.add_product_to_cart(name)
