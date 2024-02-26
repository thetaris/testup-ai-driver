import pytest
import logging
from pathlib import Path
from test_utils import assert_chatGPT_response
from action_processor import DomAnalyzer

class Testbogner_damen_neuheiten:

    @pytest.fixture
    def setup(self):
        # Setup code here, adjust as needed
        self.instance = DomAnalyzer()
        logging.info('Test setup completed')
        yield
        logging.info('Test teardown initiated')
        # Teardown code here, if any

    def test_case_1(self, setup, data_file_path):
        logging.info('Starting test case 1: buy any product on URL: https://www.bogner.com/de-de/c/damen/specials/diesen-monat/570394/?prefn1=productLine&prefv1=bogner')
        session_id = 1234
        user_prompt = """buy any product"""
        # Locate and read the HTML file
        file_path = data_file_path / 'bogner_damen_neuheiten.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """"""
        expected_action = """click"""
        expected_css_selector = """#onetrust-accept-btn-handler"""
        expected_text = """"""
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, "click", "#onetrust-accept-btn-handler", "")
        logging.info('Test case 1 completed successfully')

