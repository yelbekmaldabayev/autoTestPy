from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchComponent:
    """Component for product search functionality."""
    
    # Selectors
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    SEARCH_RESULTS_TITLE = (By.CSS_SELECTOR, ".title.text-center")
    PRODUCT_IMAGE_WRAPPER = (By.CSS_SELECTOR, ".product-image-wrapper")
    FEATURES_ITEMS = (By.CSS_SELECTOR, ".features_items")
    
    def __init__(self, driver):
        self.driver = driver
    
    def enter_search_term(self, term):
        """Enter search term in the search input."""
        search_input = self.driver.find_element(*self.SEARCH_INPUT)
        search_input.send_keys(term)
    
    def click_search_button(self):
        """Click the search button."""
        search_button = self.driver.find_element(*self.SEARCH_BUTTON)
        search_button.click()
    
    def search(self, term):
        """Perform a search with the given term."""
        self.enter_search_term(term)
        self.click_search_button()
    
    def wait_for_search_input(self, timeout=10):
        """Wait for search input to be present."""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.SEARCH_INPUT)
        )
    
    def get_search_results_title(self, timeout=10):
        """Get the search results title element."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.SEARCH_RESULTS_TITLE)
        )
    
    def get_product_cards(self, timeout=10):
        """Get all product card elements."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(self.PRODUCT_IMAGE_WRAPPER)
        )
    
    def get_features_items(self, timeout=10):
        """Get the features items container."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.FEATURES_ITEMS)
        )
