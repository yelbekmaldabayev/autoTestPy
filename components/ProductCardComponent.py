from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class ProductCardComponent:
    """Component for product card functionality."""
    
    # Selectors
    PRODUCT_IMAGE_WRAPPER = (By.CSS_SELECTOR, ".product-image-wrapper")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".add-to-cart")
    CART_MODAL = (By.ID, "cartModal")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, ".btn.btn-success.close-modal")
    
    def __init__(self, driver):
        self.driver = driver
    
    def get_first_product_card(self, timeout=15):
        """Get the first product card element."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.PRODUCT_IMAGE_WRAPPER)
        )
    
    def scroll_to_element(self, element):
        """Scroll the element into view."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def hover_over_element(self, element):
        """Hover over the given element."""
        ActionChains(self.driver).move_to_element(element).perform()
    
    def get_add_to_cart_button(self, product_card):
        """Get the add to cart button from a product card."""
        return product_card.find_element(*self.ADD_TO_CART_BUTTON)
    
    def click_add_to_cart(self, product_card):
        """Click the add to cart button on a product card."""
        add_btn = self.get_add_to_cart_button(product_card)
        try:
            add_btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", add_btn)
    
    def wait_for_cart_modal(self, timeout=10):
        """Wait for cart modal to be visible."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.CART_MODAL)
        )
    
    def click_continue_shopping(self, timeout=10):
        """Click the continue shopping button in the modal."""
        continue_btn = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.CONTINUE_SHOPPING_BUTTON)
        )
        continue_btn.click()
