
import logging
from test_utils import assert_chatGPT_response


def execute_test_case(self, setup, data_file_path, case_id, user_prompt, file_name, expected_action, expected_css_selector, expected_text, url):
    logging.info(f'Starting test case {case_id}: {user_prompt} on the website: {url}')
    session_id = 1234  # Assuming this is constant for all cases; adjust if it varies
    # Locate and read the HTML file
    file_path = data_file_path / file_name
    logging.debug(f"Reading HTML file from: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    actions_executed = """"""
    logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)}")
    actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
    assert_chatGPT_response(actual_response, expected_action, expected_css_selector, expected_text)
    logging.info(f'Test case {case_id} completed successfully')