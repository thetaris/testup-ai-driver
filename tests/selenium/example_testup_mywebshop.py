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
url = "https://mywebsite.testup.io/"


try:
    mySelenium = SeleniumUtils()
    mySelenium.set_local_driver(driver, url)

    ###############################################
    ############# TESTSTEPS   #####################
    ###############################################



    mySelenium.execute_prompt("""put any product in shopping cart""")
    time.sleep(1)
    mySelenium.execute_prompt("""go to the shopping cart""")
    try:
        # Find the element
        input_element = mySelenium.driver.find_element(By.CLASS_NAME, 'input-text.qty.text')
        # Get the value attribute
        quantity_value = int(input_element.get_attribute('value'))
        if not quantity_value == 1:
            raise Exception("product not added to cart")
        else:
            print("Product has been added to cart")
    except:
        print("did not navigate to shopping cart")
    mySelenium.execute_prompt("""go to the checkout page, the button to do so is at the bottom of the shopping cart page""")
    # Find the <h1> tag directly using a CSS selector
    title_element = driver.find_element(By.CSS_SELECTOR, 'header.entry-header h1.entry-title')
    title_text = title_element.text

    if title_text != "Checkout":
        print("did not navigate to checkout, test failed")
    else:
        print("Successfully navigated to checkout")
    time.sleep(1)


    ###############################################
    ############### CLEANUP   #####################
    ###############################################

finally:
    # Close the browser
    driver.quit()

