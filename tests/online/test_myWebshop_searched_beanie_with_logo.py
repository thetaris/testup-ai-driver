import pytest
import logging
from pathlib import Path
from test_utils import assert_chatGPT_response
from action_processor import DomAnalyzer  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Test cases for https://mywebsite.testup.io/?s=beanie+with+logo&post_type=product
class TestmyWebshop_searched_beanie_with_logo:

    @pytest.fixture
    def setup(self):
        # Setup code here, adjust as needed
        self.instance = DomAnalyzer()
        logging.info('Test setup completed')
        yield
        logging.info('Test teardown initiated')
        # Teardown code here, if any

    def test_case_7(self, setup, data_file_path):
        logging.info('Starting test case 7: add beanie to cart')
        session_id = 1234
        user_prompt = "add beanie to cart"
        # Locate and read the HTML file
        file_path = data_file_path / 'myWebshop_searched_beanie_with_logo.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """"""
        expected_action = "click"
        expected_css_selector = "#autoidtestup41"
        expected_text = "Beanie added to cart"
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, "click", "#autoidtestup41", "Beanie added to cart")
        logging.info('Test case 7 completed successfully')

