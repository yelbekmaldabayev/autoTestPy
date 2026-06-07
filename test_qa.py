import pytest
import os
from dotenv import load_dotenv

from selenium import webdriver

from pages.ProductsPage import ProductsPage
from pages.LoginPage import LoginPage
from pages.CartPage import CartPage

load_dotenv()

# FIXTURE - ONE BROWSER PER SESSION
@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # DISABLE THIS
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--window-size=1400,1000")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(1)
    yield driver
    driver.quit()


# CLASS 1 - PRODUCT SEARCH
class TestProductSearch:

    def test_search_returns_results(self, driver):
        # Steps: open products page, hide ads, type query, click search
        products_page = ProductsPage(driver)
        products_page.open()
        products_page.search("dress")

        # Assertion: at least one product card must appear
        products = products_page.get_product_cards()
        assert len(products) > 0, "Expected search results but got none"

    def test_search_result_count_displayed(self, driver):
        # Steps: open products page, search for a term, verify heading
        products_page = ProductsPage(driver)
        products_page.open()
        products_page.search("dress")

        # Assertion: results section heading contains "SEARCHED PRODUCTS"
        title_text = products_page.get_search_heading_text()
        assert "SEARCHED PRODUCTS" in title_text, (
            f"Expected 'SEARCHED PRODUCTS' heading, got: '{title_text}'"
        )

    def test_empty_search_shows_error(self, driver):
        # Steps: open products page, click search without any input
        products_page = ProductsPage(driver)
        products_page.open()
        products_page.submit_empty_search()

        # Assertion: features container is still displayed (no crash / redirect)
        assert products_page.is_product_grid_displayed(), "Expected features_items to be visible after empty search"


# CLASS 2 - LOGIN
class TestLogin:

    def test_valid_login(self, driver):
        # Steps: navigate to login, enter valid credentials, submit
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(os.getenv("LOGIN_EMAIL"), os.getenv("LOGIN_PASSWORD"))

        # Assertion: "Logged in as" link appears in the navbar
        assert login_page.is_logged_in(), "Expected 'Logged in as' to be visible after valid login"

    def test_invalid_password_shows_error(self, driver):
        # Steps: log out, navigate to login, enter wrong password, submit
        login_page = LoginPage(driver)
        login_page.open_as_guest()
        login_page.login("test@example.com", "wrongpass")

        # Assertion: error message is displayed
        assert login_page.is_error_displayed(), "Expected error message for wrong password"

    def test_invalid_email_format(self, driver):
        # Steps: log out, navigate to login, enter malformed email, submit
        login_page = LoginPage(driver)
        login_page.open_as_guest()
        login_page.login("invalid-email-format", "123456")

        # Assertion: server-side or client-side error is shown
        assert login_page.is_error_displayed(), "Expected error message for invalid email format"

    def test_empty_fields_show_error(self, driver):
        # Steps: log out, navigate to login, click submit without filling anything
        login_page = LoginPage(driver)
        login_page.open_as_guest()
        login_page.submit_empty_form()

        # Assertion: browser native validation message is set on the email field
        validation_message = login_page.get_email_validation_message()
        assert validation_message != "", (
            "Expected browser validation message on empty email field"
        )


# CLASS 3 - ADD TO CART
class TestAddToCart:

    def test_add_product_to_cart(self, driver):
        # Steps: open products page, hover first product, add to cart, verify modal
        products_page = ProductsPage(driver)
        products_page.open()
        products_page.add_first_product_to_cart()

        # Assertion 1: confirmation modal appears
        assert products_page.is_cart_modal_displayed(), "Expected cart confirmation modal to be visible"

        # Dismiss modal
        products_page.dismiss_cart_modal()

        # Navigate to the cart page and verify at least one item row exists
        cart_page = CartPage(driver)
        cart_page.open()
        cart_item_count = cart_page.get_cart_item_count()

        # Assertion 2: cart contains at least one product
        assert cart_item_count >= 1, (
            f"Expected at least 1 item in cart, found {cart_item_count}"
        )