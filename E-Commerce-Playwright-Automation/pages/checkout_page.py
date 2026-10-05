from typing import Dict, List
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from utils.config import Config

class CheckoutPage(BasePage):
    """Page Object for Multi-Step Checkout (Information, Overview, Confirmation)."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Step One: Customer Information
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")
        self.cancel_button = page.locator("#cancel")
        self.error_container = page.locator("[data-test='error']")

        # Step Two: Overview & Summary
        self.overview_item_names = page.locator(".inventory_item_name")
        self.subtotal_label = page.locator(".summary_subtotal_label")
        self.tax_label = page.locator(".summary_tax_label")
        self.total_label = page.locator(".summary_total_label")
        self.payment_info_value = page.locator(".summary_value_label").first
        self.finish_button = page.locator("#finish")

        # Step Three: Complete
        self.complete_header = page.locator(".complete-header")
        self.complete_text = page.locator(".complete-text")
        self.back_home_button = page.locator("#back-to-products")

    # --- Step 1 Methods ---
    def fill_customer_info(
        self,
        first_name: str = Config.DEFAULT_FIRST_NAME,
        last_name: str = Config.DEFAULT_LAST_NAME,
        postal_code: str = Config.DEFAULT_POSTAL_CODE
    ):
        """Fills checkout customer information fields."""
        if first_name is not None:
            self.first_name_input.fill(first_name)
        if last_name is not None:
            self.last_name_input.fill(last_name)
        if postal_code is not None:
            self.postal_code_input.fill(postal_code)

    def click_continue(self):
        """Clicks the continue button on Step 1."""
        self.continue_button.click()

    def get_error_message(self) -> str:
        """Returns the validation error message from Step 1."""
        self.error_container.wait_for(state="visible", timeout=Config.DEFAULT_TIMEOUT)
        return self.error_container.inner_text().strip()

    # --- Step 2 Methods ---
    def get_overview_item_names(self) -> List[str]:
        """Returns list of product names displayed in the checkout overview."""
        return self.overview_item_names.all_inner_texts()

    def get_price_summary(self) -> Dict[str, float]:
        """Parses and returns Item Total, Tax, and Total prices."""
        subtotal_str = self.subtotal_label.inner_text().replace("Item total: $", "").strip()
        tax_str = self.tax_label.inner_text().replace("Tax: $", "").strip()
        total_str = self.total_label.inner_text().replace("Total: $", "").strip()
        return {
            "subtotal": float(subtotal_str),
            "tax": float(tax_str),
            "total": float(total_str)
        }

    def click_finish(self):
        """Clicks the finish button on the overview page to complete order."""
        self.finish_button.click()

    # --- Step 3 Methods ---
    def get_confirmation_header(self) -> str:
        """Returns confirmation header text (e.g., 'Thank you for your order!')."""
        self.complete_header.wait_for(state="visible", timeout=Config.DEFAULT_TIMEOUT)
        return self.complete_header.inner_text().strip()

    def is_order_successful(self) -> bool:
        """Verifies if order success header and back home button are visible."""
        return self.complete_header.is_visible() and self.back_home_button.is_visible()

    def back_to_home(self):
        """Navigates back to inventory page after order completion."""
        self.back_home_button.click()
