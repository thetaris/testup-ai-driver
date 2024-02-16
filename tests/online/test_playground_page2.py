import pytest
import logging
from pathlib import Path
from action_processor import DomAnalyzer  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Test cases for https://thetaris.org/playground/?page=2
class Testplayground_page2:

    @pytest.fixture
    def setup(self):
        # Setup code here, adjust as needed
        self.instance = DomAnalyzer()
        logging.info('Test setup completed')
        yield
        logging.info('Test teardown initiated')
        # Teardown code here, if any

    def test_case_1(self, setup):
        logging.info('Starting test case 1: enter HelloWorld in the textbox')
        session_id = 1234
        user_prompt = "enter HelloWorld in the textbox"
        # Locate and read the HTML file
        file_path = Path(__file__).parent.parent/ 'data'/ 'online'/ 'playground_page2.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """"""
        expected_response = "#autoidtestup0"
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert actual_response == expected_response, f"Expected: #autoidtestup0, but got: {actual_response}"
        logging.info('Test case 1 completed successfully')

    def test_case_2(self, setup):
        logging.info('Starting test case 2: click ok')
        session_id = 1234
        user_prompt = "click ok"
        # Locate and read the HTML file
        file_path = Path(__file__).parent.parent/ 'data'/ 'online'/ 'playground_page2.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """"""
        expected_response = "#autoidtestup1"
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert actual_response == expected_response, f"Expected: #autoidtestup1, but got: {actual_response}"
        logging.info('Test case 2 completed successfully')

    def test_case_3(self, setup):
        logging.info('Starting test case 3: enter the text HelloWorld and then click ok')
        session_id = 1234
        user_prompt = "enter the text HelloWorld and then click ok"
        # Locate and read the HTML file
        file_path = Path(__file__).parent.parent/ 'data'/ 'online'/ 'playground_page2.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """{"action":"enter_text","css_selector":"#autoidtestup0","text":"HelloWorld","explanation":"To input text HelloWorld into the 'input' element with id 'autoidtestup0'","description":"Enter the text HelloWorld into the input field with id 'autoidtestup0'"}"""
        expected_response = "#autoidtestup1"
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert actual_response == expected_response, f"Expected: #autoidtestup1, but got: {actual_response}"
        logging.info('Test case 3 completed successfully')

