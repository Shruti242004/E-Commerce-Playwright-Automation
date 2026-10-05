from typing import List
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class CartPage(BasePage):
    """Page Object for the Shopping Cart Page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_items = page.locator(".cart_item")
        self.cart_item_names = page.locator(".inventory_item_name")
        self.cart_item_prices = page.locator(".inventory_item_price")
        self.continue_shopping_button = page.locator("#continue-shopping")
        self.checkout_button = page.locator("#checkout")

    def get_cart_items_names(self) -> List[str]:
        """Returns the list of product names currently in the cart."""
        return self.cart_item_names.all_inner_texts()

    def get_cart_items_count(self) -> int:
        """Returns the total number of line items in the cart."""
        return self.cart_items.count()

    def _get_cart_item_by_name(self, product_name: str) -> Locator:
        """Locates the cart item container containing the specified product name."""
        return self.cart_items.filter(has=self.page.locator(".inventory_item_name", has_text=product_name))

    def remove_item(self, product_name: str):
        """Clicks the 'Remove' button for a given product in the cart."""
        item = self._get_cart_item_by_name(product_name)
        item.locator("button:has-text('Remove')").click()

    def remove_all_items(self):
        """Removes all items from the cart one by one."""
        remove_buttons = self.page.locator(".cart_item button:has-text('Remove')")
        while remove_buttons.count() > 0:
            remove_buttons.first.click()

    def continue_shopping(self):
        """Clicks the Continue Shopping button to navigate back to Products."""
        self.continue_shopping_button.click()

    def proceed_to_checkout(self):
        """Clicks the Checkout button to navigate to Checkout Step 1."""
        self.checkout_button.click()

    def is_cart_empty(self) -> bool:
        """Checks if the cart has no items."""
        return self.cart_items.count() == 0
