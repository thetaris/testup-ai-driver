import pytest
import logging
from pathlib import Path
from action_processor import DomAnalyzer  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Test cases for https://www.bogner.com/de-de/c/damen/specials/diesen-monat/570394/?prefn1=productLine&prefv1=bogner
class Testbogner_damen_neuheiten:

    @pytest.fixture
    def setup(self):
        # Setup code here, adjust as needed
        self.instance = DomAnalyzer()
        logging.info('Test setup completed')
        yield
        logging.info('Test teardown initiated')
        # Teardown code here, if any

    def test_case_1(self, setup):
        logging.info('Starting test case 1: buy any product')
        session_id = 1234
        user_prompt = "buy any product"
        # Locate and read the HTML file
        file_path = Path(__file__).parent.parent/ 'data'/ 'online'/ 'bogner_damen_neuheiten.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """"""
        expected_response = "#autoidtestup40"
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert actual_response == expected_response, f"Expected: #autoidtestup40, but got: {actual_response}"
        logging.info('Test case 1 completed successfully')

