import pytest
import logging
from pathlib import Path
from test_utils import assert_chatGPT_response
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

    def test_case_2(self, setup, data_file_path):
        logging.info('Starting test case 2: enter HelloWorld in the textbox')
        session_id = 1234
        user_prompt = "enter HelloWorld in the textbox"
        # Locate and read the HTML file
        file_path = data_file_path / 'playground_page2.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """"""
        expected_action = "enter_text"
        expected_css_selector = "#autoidtestup0"
        expected_text = "HelloWorld"
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, "enter_text", "#autoidtestup0", "HelloWorld")
        logging.info('Test case 2 completed successfully')

    def test_case_3(self, setup, data_file_path):
        logging.info('Starting test case 3: click ok')
        session_id = 1234
        user_prompt = "click ok"
        # Locate and read the HTML file
        file_path = data_file_path / 'playground_page2.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """"""
        expected_action = "click"
        expected_css_selector = "#autoidtestup1"
        expected_text = "OK clicked"
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, "click", "#autoidtestup1", "OK clicked")
        logging.info('Test case 3 completed successfully')

    def test_case_4(self, setup, data_file_path):
        logging.info('Starting test case 4: enter the text HelloWorld and then click ok')
        session_id = 1234
        user_prompt = "enter the text HelloWorld and then click ok"
        # Locate and read the HTML file
        file_path = data_file_path / 'playground_page2.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """{
          "steps": [
            {
              "action": "enter_text",
              "css_selector": "#autoidtestup0",
              "text": "HelloWorld",
              "explanation": "To input the text HelloWorld as instructed.",
              "description": "Enter the text HelloWorld in the input field."
            }
          ]
        }"""
        expected_action = "enter_text"
        expected_css_selector = "#autoidtestup1"
        expected_text = "HelloWorld, then OK clicked"
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, "enter_text", "#autoidtestup1", "HelloWorld, then OK clicked")
        logging.info('Test case 4 completed successfully')

