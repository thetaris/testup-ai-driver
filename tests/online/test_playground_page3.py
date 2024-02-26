import pytest
import logging
from pathlib import Path
from test_utils import assert_chatGPT_response
from action_processor import DomAnalyzer  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Test cases for https://thetaris.org/playground/?page=3
class Testplayground_page3:

    @pytest.fixture
    def setup(self):
        # Setup code here, adjust as needed
        self.instance = DomAnalyzer()
        logging.info('Test setup completed')
        yield
        logging.info('Test teardown initiated')
        # Teardown code here, if any

    def test_case_5(self, setup, data_file_path):
        logging.info('Starting test case 5: scroll down')
        session_id = 1234
        user_prompt = "scroll down"
        # Locate and read the HTML file
        file_path = data_file_path / 'playground_page3.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """"""
        expected_action = "scroll"
        expected_css_selector = ""
        expected_text = "Scrolled down"
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, "scroll", "", "Scrolled down")
        logging.info('Test case 5 completed successfully')

