import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# ============================================================
# FIXTURE — ОДИН БРАУЗЕР НА ВСЮ СЕССИЮ (МАКСИМАЛЬНОЕ УСКОРЕНИЕ)
# ============================================================
@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--window-size=1400,1000")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(1)  # быстрый implicit wait
    yield driver
    driver.quit()


# ============================================================
# CLASS 1 — PRODUCT SEARCH (TC-001, TC-002, TC-003)
# ============================================================
class TestProductSearch:

    def test_search_returns_results(self, driver):
        driver.get("https://automationexercise.com/products")
        wait = WebDriverWait(driver, 5)

        search_input = wait.until(
            EC.presence_of_element_located((By.ID, "search_product"))
        )
        search_input.send_keys("dress")
        driver.find_element(By.ID, "submit_search").click()

        products = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-image-wrapper"))
        )
        assert len(products) > 0

    def test_search_result_count_displayed(self, driver):
        driver.get("https://automationexercise.com/products")
        wait = WebDriverWait(driver, 5)

        wait.until(EC.presence_of_element_located((By.ID, "search_product"))).send_keys("dress")
        driver.find_element(By.ID, "submit_search").click()

        title = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".title.text-center"))
        )
        assert "SEARCHED PRODUCTS" in title.text.upper()

    def test_empty_search_shows_error(self, driver):
        driver.get("https://automationexercise.com/products")
        wait = WebDriverWait(driver, 5)

        driver.find_element(By.ID, "submit_search").click()

        error = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
        )
        assert error.is_displayed()


# ============================================================
# CLASS 2 — LOGIN (TC-004, TC-005, TC-006, TC-007)
# ============================================================
class TestLogin:

    def test_valid_login(self, driver):
        driver.get("https://automationexercise.com/login")
        wait = WebDriverWait(driver, 5)

        email = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-qa='login-email']")))
        password = driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']")
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']")

        #Вставь свои реальные данные
        email.send_keys("your_real_email@example.com")
        password.send_keys("your_real_password")
        login_btn.click()

        logged_in = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Logged in as')]"))
        )
        assert logged_in.is_displayed()

    def test_invalid_password_shows_error(self, driver):
        driver.get("https://automationexercise.com/login")
        wait = WebDriverWait(driver, 5)

        driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']").send_keys("test@example.com")
        driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys("wrongpass")
        driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()

        error = wait.until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'Your email or password is incorrect!')]"))
        )
        assert error.is_displayed()

    def test_invalid_email_format(self, driver):
        driver.get("https://automationexercise.com/login")
        wait = WebDriverWait(driver, 5)

        email = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-qa='login-email']")))
        password = driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']")
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']")

        email.send_keys("invalid-email-format")
        password.send_keys("123456")
        login_btn.click()

        error = wait.until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'Your email or password is incorrect!')]"))
        )
        assert error.is_displayed()

    def test_empty_fields_show_error(self, driver):
        driver.get("https://automationexercise.com/login")
        wait = WebDriverWait(driver, 5)

        driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()

        error = wait.until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'Your email or password is incorrect!')]"))
        )
        assert error.is_displayed()


# ============================================================
# CLASS 3 — ADD TO CART (TC-008 BONUS)
# ============================================================
class TestAddToCart:

    def test_add_product_to_cart(self, driver):
        driver.get("https://automationexercise.com/products")
        wait = WebDriverWait(driver, 5)

        first_product = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".product-image-wrapper"))
        )

        ActionChains(driver).move_to_element(first_product).perform()

        add_btn = first_product.find_element(By.CSS_SELECTOR, ".add-to-cart")
        add_btn.click()

        modal = wait.until(EC.presence_of_element_located((By.ID, "cartModal")))
        assert modal.is_displayed()

        continue_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.close-modal"))
        )
        continue_btn.click()

        cart = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/view_cart']"))
        )
        assert "1" in cart.text
