from selenium.webdriver.common.action_chains import ActionChains
from .BasePage import BasePage
from components.SearchComponent import SearchComponent
from components.ProductCardComponent import ProductCardComponent
from selenium.webdriver.support import expected_conditions as EC

class ProductsPage(BasePage):
    """
    Page Object for https://automationexercise.com/products
    Covers: product search and add-to-cart flows.
    """

    URL_PATH = "/products"

    def __init__(self, driver):
        super().__init__(driver)
        self.search_component = SearchComponent(driver)
        self.product_card_component = ProductCardComponent(driver)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self):
        super().open(self.URL_PATH)
        self.search_component.wait_for_search_input()

    def search(self, query: str):
        """Type a query and submit the search form."""
        self.hide_ads()
        self.search_component.search(query)

    def submit_empty_search(self):
        """Click the search button without entering any text."""
        self.hide_ads()
        self.search_component.click_search_button()

    def add_first_product_to_cart(self):
        """
        Hover over the first product card and click its Add-to-cart button.
        Returns self for fluent chaining.
        """
        self.search_component.get_features_items()
        self.hide_ads()

        first_card = self.product_card_component.get_first_product_card()
        self.product_card_component.scroll_to_element(first_card)
        self.product_card_component.hover_over_element(first_card)
        self.product_card_component.click_add_to_cart(first_card)

        return self

    def dismiss_cart_modal(self):
        """Wait for the confirmation modal and click 'Continue Shopping'."""
        self.product_card_component.wait_for_cart_modal()
        self.product_card_component.click_continue_shopping()

    # ------------------------------------------------------------------
    # Queries  (return data that tests assert against)
    # ------------------------------------------------------------------

    def get_product_cards(self):
        return self.search_component.get_product_cards()

    def get_search_heading_text(self) -> str:
        heading = self.wait.until(
            EC.visibility_of(self.search_component.get_search_results_title())
        )
        return heading.text.upper()



    def is_product_grid_displayed(self) -> bool:
        return self.search_component.get_features_items().is_displayed()

    def is_cart_modal_displayed(self) -> bool:
        return self.product_card_component.wait_for_cart_modal().is_displayed()