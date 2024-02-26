import pytest
import logging
from pathlib import Path
from test_utils import assert_chatGPT_response
from action_processor import DomAnalyzer

class TestmyWebshop_checkout:

    @pytest.fixture
    def setup(self):
        # Setup code here, adjust as needed
        self.instance = DomAnalyzer()
        logging.info('Test setup completed')
        yield
        logging.info('Test teardown initiated')
        # Teardown code here, if any

    def test_case_1(self, setup, data_file_path):
        logging.info('Starting test case 1: fill out the form on URL: https://mywebsite.testup.io/checkout/')
        session_id = 1234
        user_prompt = """fill out the form"""
        # Locate and read the HTML file
        file_path = data_file_path / 'myWebshop_checkout.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """"""
        expected_action = """enter_text"""
        expected_css_selector = """#billing_first_name"""
        expected_text = """Barbara"""
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, "enter_text", "#billing_first_name", "Barbara")
        logging.info('Test case 1 completed successfully')

