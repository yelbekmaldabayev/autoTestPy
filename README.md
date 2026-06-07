# Automation Exercise — Selenium POM Test Suite

## Project structure

```
autoTestPy/
│
├── components/                 # Component layer (reusable UI elements)
│   ├── SearchComponent.py      # Search functionality with selectors
│   ├── LoginFormComponent.py   # Login form functionality with selectors
│   └── ProductCardComponent.py # Product card functionality with selectors
│
├── pages/                      # Page Object Model layer
│   ├── __init__.py
│   ├── BasePage.py            # Shared driver helpers (wait, navigate, hide_ads)
│   ├── ProductsPage.py        # /products  — search + add-to-cart
│   ├── LoginPage.py           # /login     — login form
│   └── CartPage.py            # /view_cart — cart verification
│
├── test_qa.py                  # Test layer (pytest classes)
│
└── .env                        # LOGIN_EMAIL and LOGIN_PASSWORD (not committed)
```

## Architecture

This project uses a **Page Object Model (POM)** pattern with three layers:

1. **Components** - Reusable UI components with embedded selectors (CSS/XPath)
   - Encapsulate specific UI functionality (search, login form, product cards)
   - Contain all selectors needed for their functionality
   - Provide methods for interacting with the UI elements

2. **Pages** - Page-level objects that use components
   - Represent full pages of the application
   - Use components to perform actions
   - Contain page-specific selectors where needed
   - Provide high-level page actions and queries

3. **Tests** - Test cases that use only page objects
   - No selectors (CSS/XPath) in test files
   - Only interact with page objects
   - Clean, readable test logic

## Setup

```bash
pip install selenium pytest python-dotenv
```

Create a `.env` file in the project root:

```
LOGIN_EMAIL=your@email.com
LOGIN_PASSWORD=yourpassword
```

## Run

```bash
# All tests
pytest test_qa.py -v

# With short traceback
pytest test_qa.py -v --tb=short

# Specific test class
pytest test_qa.py::TestProductSearch -v

# Specific test method
pytest test_qa.py::TestProductSearch::test_search_returns_results -v
```

## Test Coverage

- **TestProductSearch**: Product search functionality
  - test_search_returns_results
  - test_search_result_count_displayed
  - test_empty_search_shows_error

- **TestLogin**: Login functionality
  - test_valid_login
  - test_invalid_password_shows_error
  - test_invalid_email_format
  - test_empty_fields_show_error

- **TestAddToCart**: Add to cart functionality
  - test_add_product_to_cart
