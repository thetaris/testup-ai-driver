import textwrap
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import action_processor
import logging
import time
from user_exceptions import PromptActionException
from user_exceptions import SeleniumBrokenLinkException
from test_steps import TestSteps
from selenium.webdriver.common.action_chains import ActionChains




class SeleniumAiUtils:
    DRIVER_TIMEOUT_SECONDS = 120
    EMPTY_HTML_DOCUMENT = "<html><head></head><body></body></html>"

    def __init__(self):
        self.driver = None
        self.url = None
        self.dom_analyzer = action_processor.DomAnalyzer()


    def set_local_driver(self, driver, url):
        self.driver = driver
        self.url = url
        try:
            # Open the website
            self._load_initial_page()
        except Exception as e:
            if self.driver:
                print("Disconnecting driver")
                self.driver.quit()
            raise e

    def close_local_driver(self):
        if self.driver is None:
            # Log an info message if self.driver is already None
            logging.info("The driver is already closed.")
        else:
            # Only attempt to quit and set to None if self.driver is not None
            self.driver.quit()
            self.driver = None

    def connect_driver(self, selenium_grid_url, caps, url):
        self.url = url
        try:
            self._retry_on_exception(3, 3, lambda: self._initialize_driver(selenium_grid_url, caps))
            self._retry_on_exception(3, 3, self._load_initial_page, skip_exceptions=[SeleniumBrokenLinkException])
        except Exception as e:
            if self.driver:
                print("Disconnecting driver")
                self.driver.quit()
            raise e

    def _initialize_driver(self, selenium_grid_url, caps):
        self.driver = webdriver.Remote(command_executor=selenium_grid_url, desired_capabilities=caps)
        self.driver.implicitly_wait(self.DRIVER_TIMEOUT_SECONDS)

    def _load_initial_page(self):
        try:
            self.driver.get(self.url)
        except WebDriverException:
            raise SeleniumBrokenLinkException(f"URL '{self.url}' is not reachable.")
        if self.driver.page_source == self.EMPTY_HTML_DOCUMENT:
            raise SeleniumBrokenLinkException(f"URL '{self.url}' is not reachable.")

    def go_to_url(self, url):
        self.url = url
        self._load_initial_page()



    def _retry_on_exception(self, max_attempts, retry_period_sec, func, skip_exceptions=[]):
        for attempt in range(max_attempts):
            try:
                func()
                break
            except Exception as e:
                if any(isinstance(e, exc) for exc in skip_exceptions):
                    raise
                if attempt < max_attempts - 1:
                    time.sleep(retry_period_sec)
                else:
                    raise

    def execute_prompt(self, prompt, variables_map = "- no variables available -"):
        self.dom_analyzer = action_processor.DomAnalyzer()

        if prompt == "":
            print("Empty prompt.")
            return True

        accumulated_actions = []
        current_step = 0
        #        session_id = str(uuid.uuid4())
        last_action = None
        consecutive_action_count = 1
        consecutive_failure_count = 0
        is_duplicate = False
        is_valid = True

        while True:
            if consecutive_action_count > 5:
                raise PromptActionException(
                    "Generative AI is stuck at the same action, please try again")
            if consecutive_failure_count > 5:
                raise PromptActionException(
                    "Generative AI generated invalid actions consecutively, please try again")
            if current_step > 100:
                break

            self._assign_auto_generated_ids()
            visible_dom = self._get_visible_dom()
        #file_path = 'example.txt'
        # with open(file_path, 'a') as file:
        #     file.write("#############################################################################################\n")
        #     file.write(f"HTML: {visible_dom}\n")
        #     file.write("#############################################################################################\n")

            try:
                response = self.dom_analyzer.get_actions(1234, prompt, visible_dom, accumulated_actions, variables_map, is_duplicate, is_valid, last_action)
                response = TestSteps(response)
            except Exception as ex:
                logging.error("Failed to call Prompt Service: %s", ex)
                raise PromptActionException("Failed to get Action from Generative AI model")

            if not response.steps:
                consecutive_failure_count += 1
                last_action = None
                continue

            index = 0

            if last_action == response.steps[index]:
                consecutive_action_count += 1
                is_duplicate = True
                if consecutive_action_count > 5:
                    raise PromptActionException(
                        "Generative AI is stuck at the same action, please try again")
                index += 1
                continue
            else:
                consecutive_action_count = 1
                is_duplicate = False

            step = response.steps[index]
            if step.action == "enter_text":
                try:
                    while True:
                        step = response.steps[index]
                        last_action = step
                        self._execute_action_for_prompt(step)
                        is_valid = True
                        consecutive_failure_count = 0
                        accumulated_actions.append(step)
                        index += 1

                        if not(0 <= index < len(response.steps) and response.steps[index].action == "enter_text"):
                            break

                    if index < len(response.steps) and response.steps[index].action == "key_enter":
                        time.sleep(1)
                        last_action = response.steps[index]
                        self._execute_action_for_prompt(response.steps[index])
                        is_valid = True
                        consecutive_failure_count = 0
                        accumulated_actions.append(step)
                        index += 1


                except Exception:
                    is_valid = False
                    consecutive_failure_count += 1
                    continue
            else:
                try:
                    last_action = step
                    if not self._execute_action_for_prompt(step):
                        break
                    is_valid = True
                    consecutive_failure_count = 0
                    accumulated_actions.append(step)
                except Exception:
                    is_valid = False
                    consecutive_failure_count += 1
                    continue

            time.sleep(3)

        if not accumulated_actions:
            raise PromptActionException("No actions were executed")

    def _execute_action_for_prompt(self, content):
        try:
            if content.action == "click":
                self._assert_css_selector_exists(content)
                self._click_element(content.css_selector)

            elif content.action == "enter_text":
                self._assert_css_selector_exists(content)
                self._enter_text_in_element(content.css_selector, content.text)

            elif content.action == "key_enter":
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.ENTER).perform()

            elif content.action == "error":
                return False

            elif content.action == "scroll":
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

            elif content.action == "finish":
                # Handle finish action, potentially ending the prompt execution loop
                return False

            return True

        except NoSuchElementException as ex:
            # Log the error using your preferred logging framework
            print(f"Failed to find element {content.css_selector}: {ex}")
            raise PromptActionException(
                "Failed to execute action, Generative AI returned invalid action")
        except Exception as ex:
            # Log the error using your preferred logging framework
            print(f"Failed to execute prompt action: {ex}")
            raise PromptActionException("Failed to execute action generative AI action")

        # If an unsupported action is provided
        raise ValueError(f"Unsupported action: {content.action}")

    def _assert_css_selector_exists(self, action):
        if action.css_selector is None:
            raise PromptActionException("Action cannot be executed without a CSS selector")

    def _click_element(self, css_selector):
        try:
            self.driver.find_element(By.CSS_SELECTOR, css_selector).click()
            logging.info("SELENIUM: clicked on the element with the css id: "+css_selector)
        except:
            raise NoSuchElementException("SELENIUM: Could not click on the element with the CSS id: "+css_selector)


    def _enter_text_in_element(self, css_selector, text):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
            element.send_keys(text)
            logging.info("SELENIUM: entered the following text in the element with the css id: "+css_selector+"    text: "+text)
        except:
            raise NoSuchElementException("SELENIUM: Could not enter text in the element with the CSS id: "+css_selector)

    def _assign_auto_generated_ids(self):
        js_script = textwrap.dedent("""
                function generateUniqueId(index) {
                    var now = new Date();
                    var timestamp = now.getMinutes().toString() + now.getSeconds().toString();
                    return "idTUp" + index + "T" + timestamp;
                }
        
                const elements = document.querySelectorAll('li, button, input, textarea, [type=text], a');
                elements.forEach((el, index) => {
                    if (!el.id) {
                        el.id = generateUniqueId(index);
                    }
                });    
                """).strip()

        self.driver.execute_script(js_script)

    def _get_visible_dom(self):
        js_script = textwrap.dedent("""
    
                function isElementInViewport(el) {
                    var rect = el.getBoundingClientRect();
                    return (
                        rect.top >= 0 &&
                        rect.left >= 0 &&
                        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
                    );
                }
    
                function isElementVisible(el) {
                    return el.offsetWidth > 0 && el.offsetHeight > 0 && window.getComputedStyle(el).visibility !== 'hidden';
                }
    
    
                var allElements = document.querySelectorAll('body *');
                var visibleElements = Array.from(allElements)
                    .filter(el => isElementInViewport(el) && isElementVisible(el));
    
                // Filter out child elements
                var filteredElements = visibleElements.filter(el => {
                    return !visibleElements.some(parentEl => parentEl !== el && parentEl.contains(el));
                });
    
                var visibleElementsHtml = filteredElements.map(el => el.outerHTML).join('\\n');
                return visibleElementsHtml;
    
                """).strip()

        return str(self.driver.execute_script(js_script))
