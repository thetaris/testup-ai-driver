import pytest
import logging
from pathlib import Path
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

    def test_case_1(self, setup):
        logging.info('Starting test case 1: scroll down')
        session_id = 1234
        user_prompt = "scroll down"
        # Locate and read the HTML file
        file_path = Path(__file__).parent.parent/ 'data'/ 'online'/ 'playground_page3.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = """"""
        expected_response = ""
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert actual_response == expected_response, f"Expected: , but got: {actual_response}"
        logging.info('Test case 1 completed successfully')

