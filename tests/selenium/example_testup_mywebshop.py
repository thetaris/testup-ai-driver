import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium_utils import SeleniumUtils  # Assuming this is a custom module


# Setup
def setup_driver():
    """Initialize and configure the Chrome WebDriver."""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment to enable headless mode
    chrome_options.add_argument("--start-fullscreen")  # Start in fullscreen mode
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def main():
    url = "https://mywebsite.testup.io/"
    driver = setup_driver()

    try:
        selenium_utils = SeleniumUtils()
        selenium_utils.set_local_driver(driver, url)

        # Test steps
        selenium_utils.execute_prompt("put any product in shopping cart")
        time.sleep(1)  # Wait for the page to update
        selenium_utils.execute_prompt("go to the shopping cart")

        try:
            input_element = selenium_utils.driver.find_element(By.CLASS_NAME, 'input-text.qty.text')
            quantity_value = int(input_element.get_attribute('value'))
            assert quantity_value == 1, "Product not added to cart."
            print("Product has been added to cart.")
        except NoSuchElementException:
            print("Did not navigate to shopping cart.")

        selenium_utils.execute_prompt(
            "go to the checkout page, the button to do so is at the bottom of the shopping cart page")

        # Validate navigation to the checkout page
        title_element = driver.find_element(By.CSS_SELECTOR, 'header.entry-header h1.entry-title')
        assert title_element.text == "Checkout", "Did not navigate to checkout, test failed."
        print("Successfully navigated to checkout.")
        time.sleep(10)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
