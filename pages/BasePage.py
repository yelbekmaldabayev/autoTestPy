from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Base class inherited by all page objects.
    Provides common driver helpers so page classes stay DRY.
    """

    BASE_URL = "https://automationexercise.com"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def open(self, path: str = ""):
        """Navigate to BASE_URL + path."""
        self.driver.get(f"{self.BASE_URL}{path}")

    # ------------------------------------------------------------------
    # Wait helpers
    # ------------------------------------------------------------------

    def wait_for_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def wait_for_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_url_contains(self, fragment: str):
        self.wait.until(EC.url_contains(fragment))

    # ------------------------------------------------------------------
    # Ad suppression (site-wide issue on automationexercise.com)
    # ------------------------------------------------------------------

    def hide_ads(self):
        """Hide all ad iframes to prevent click interception."""
        self.driver.execute_script(
            "document.querySelectorAll('iframe').forEach(el => el.style.display = 'none');"
        )