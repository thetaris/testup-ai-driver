import time

from selenium.webdriver.common.by import By

from selenium_utils import SeleniumUtils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

###############################################
#################  SETUP  #####################
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Enable headless mode
#chrome_options.add_argument("window-size=1920x1080")  # Set resolution to 1080p
chrome_options.add_argument("--start-fullscreen")  # This line ensures full screen mode

# Initialize the WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)
url = "https://ebay.com/"


try:
    mySelenium = SeleniumUtils()
    mySelenium.set_local_driver(driver, url)

    ###############################################
    ############# TESTSTEPS   #####################
    ###############################################

    mySelenium.execute_prompt("""search for a used ps4 game "assassins creed" """)

    mySelenium.execute_prompt("""add product to watchlist""")
    # Find the element
    input_element = mySelenium.driver.find_element(By.CLASS_NAME, 'input-text.qty.text')
    # Get the value attribute
    quantity_value = input_element.get_attribute('value')
    if not quantity_value == 1:
        raise Exception("product not added to cart")

    mySelenium.execute_prompt("""go to checkout""")
    time.sleep(1)




    ###############################################
    ############## CLEEANUP   #####################
    ###############################################

finally:
    # Close the browser
    driver.quit()

