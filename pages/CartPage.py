from selenium.webdriver.common.by import By
from .BasePage import BasePage


class CartPage(BasePage):
    """
    Page Object for https://automationexercise.com/view_cart
    Covers: verifying items exist in the cart.
    """

    URL_PATH = "/view_cart"

    # Selectors
    CART_ITEMS_TABLE_ROWS = (By.CSS_SELECTOR, "#cart_info_table tbody tr")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self):
        super().open(self.URL_PATH)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_cart_item_count(self) -> int:
        """Return the number of product rows currently in the cart."""
        rows = self.wait_for_elements(self.CART_ITEMS_TABLE_ROWS)
        return len(rows)