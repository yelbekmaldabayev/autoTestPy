from selenium.webdriver.common.by import By
from .BasePage import BasePage
from components.LoginFormComponent import LoginFormComponent


class LoginPage(BasePage):
    """
    Page Object for https://automationexercise.com/login
    Covers: valid login, invalid credentials, empty-form validation.
    """

    URL_PATH = "/login"

    # Common selectors
    LOGGED_IN_LINK = (By.XPATH, "//a[contains(text(),'Logged in as')]")
    LOGOUT_LINK = (By.XPATH, "//a[contains(@href, '/logout')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.login_component = LoginFormComponent(driver)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self):
        """Navigate to the login page and wait until the form is ready."""
        super().open(self.URL_PATH)
        self.login_component.wait_for_login_form()

    def logout_if_logged_in(self):
        """
        If an authenticated session is active, click Logout so the login
        form will actually be shown on the next open() call.
        """
        try:
            self.driver.find_element(*self.LOGOUT_LINK).click()
            self.wait_for_url_contains("/login")
        except Exception:
            pass  # Already logged out — nothing to do

    def open_as_guest(self):
        """Ensure logged-out state, then open the login page."""
        self.logout_if_logged_in()
        self.open()

    def login(self, email: str, password: str):
        """Fill in credentials and submit the login form."""
        self.login_component.login(email, password)

    def submit_empty_form(self):
        """Click Login without entering any credentials."""
        self.login_component.click_login_button()

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def is_logged_in(self) -> bool:
        return self.wait_for_element(self.LOGGED_IN_LINK).is_displayed()

    def is_error_displayed(self) -> bool:
        return self.login_component.get_error_message().is_displayed()

    def get_email_validation_message(self) -> str:
        """Return the browser-native HTML5 validation message on the email field."""
        email_el = self.login_component.get_email_input()
        return email_el.get_attribute("validationMessage")