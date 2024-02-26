import pytest
import logging
from pathlib import Path
from test_utils import assert_chatGPT_response
from action_processor import DomAnalyzer

class TestmyWebshop_start:

    @pytest.fixture
    def setup(self):
        # Setup code here, adjust as needed
        self.instance = DomAnalyzer()
        logging.info('Test setup completed')
        yield
        logging.info('Test teardown initiated')
        # Teardown code here, if any

    def test_case_1(self, setup, data_file_path):
        logging.info('Starting test case 1: use search field to search for beanie with logo on URL: https://mywebsite.testup.io/')
        session_id = 1234
        user_prompt = """use search field to search for beanie with logo"""
        # Locate and read the HTML file
        file_path = data_file_path / 'myWebshop_start.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """"""
        expected_action = """click"""
        expected_css_selector = """#woocommerce-product-search-field-0"""
        expected_text = """Beanie with logo"""
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, "click", "#woocommerce-product-search-field-0", "Beanie with logo")
        logging.info('Test case 1 completed successfully')

