from selenium_utils import SeleniumUtils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

###############################################
#################  SETUP  #####################
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Enable headless mode
chrome_options.add_argument("window-size=1920x1080")  # Set resolution to 1080p

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

