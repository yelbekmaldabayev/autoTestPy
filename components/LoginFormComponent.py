from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginFormComponent:
    """Component for login form functionality."""
    
    # Selectors
    LOGIN_FORM = (By.CSS_SELECTOR, ".login-form")
    LOGIN_EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    ERROR_MESSAGE = (By.XPATH, "//p[contains(text(),'Your email or password is incorrect!')]")
    
    def __init__(self, driver):
        self.driver = driver
    
    def enter_email(self, email):
        """Enter email in the login form."""
        email_input = self.driver.find_element(*self.LOGIN_EMAIL_INPUT)
        email_input.send_keys(email)
    
    def enter_password(self, password):
        """Enter password in the login form."""
        password_input = self.driver.find_element(*self.LOGIN_PASSWORD_INPUT)
        password_input.send_keys(password)
    
    def click_login_button(self):
        """Click the login button."""
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        login_button.click()
    
    def login(self, email, password):
        """Perform login with given credentials."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
    
    def wait_for_login_form(self, timeout=15):
        """Wait for login form to be present."""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.LOGIN_FORM)
        )
    
    def wait_for_email_input(self, timeout=15):
        """Wait for email input to be present."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.LOGIN_EMAIL_INPUT)
        )
    
    def get_email_input(self):
        """Get the email input element."""
        return self.driver.find_element(*self.LOGIN_EMAIL_INPUT)
    
    def get_error_message(self, timeout=10):
        """Get the error message element."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.ERROR_MESSAGE)
        )
