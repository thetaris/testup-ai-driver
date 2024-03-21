import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_utils import SeleniumUtils  # Assuming this is a custom module


def setup_driver():
    """Initializes and returns a Chrome WebDriver with specified options."""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    # chrome_options.add_argument("window-size=1920x1080")  # Set specific resolution
    chrome_options.add_argument("--start-fullscreen")  # Start in fullscreen mode

    return webdriver.Chrome(options=chrome_options)


def check_wikipedia_page_title(driver, expected_title):
    """Checks if the current page's title matches the expected title."""
    try:
        title_element = driver.find_element(By.ID, "firstHeading")
        page_title = title_element.text
        assert page_title == expected_title, f"Title does not match. Expected '{expected_title}', got '{page_title}'."
        print(f"Title '{page_title}' matches.")
    except NoSuchElementException:
        print(f"Test failed, didn't navigate to {expected_title}. The element does not exist.")
        raise
    except AssertionError as e:
        print(e)
        raise


def main():
    driver = setup_driver()
    url = "https://wikipedia.com/"
    mySelenium = SeleniumUtils()

    try:
        mySelenium.set_local_driver(driver, url)

        # Test Steps
        mySelenium.execute_prompt("go to the English section and then search for 'Trudering-Riem'")

        mySelenium.execute_prompt("click on 'Trudering-Riem' and then navigate from there to 'messestadt-riem'")

        check_wikipedia_page_title(driver, "Messestadt Riem")

        mySelenium.execute_prompt("go to 'Munich-Ubahn'. The link to this site might be at the bottom of the page")

        check_wikipedia_page_title(driver, "Munich U-Bahn")

        print("Test finished successfully.")

    finally:
        # Cleanup
        driver.quit()


if __name__ == "__main__":
    main()
