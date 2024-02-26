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
        assert_chatGPT_response(actual_response, expected_action, expected_css_selector, expected_text)
        logging.info('Test case 1 completed successfully')

    def test_case_2(self, setup, data_file_path):
        logging.info('Starting test case 2 (last_name): fill out the form on URL: https://mywebsite.testup.io/checkout/')
        session_id = 1234
        user_prompt = """fill out the form"""
        # Locate and read the HTML file
        file_path = data_file_path / 'myWebshop_checkout.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = [
            {
                'action': 'enter_text',
                'css_selector': '#billing_first_name',
                'text': 'Barbara',
                'explanation': 'Fill out the first name in the form',
                'description': "Enter the first name 'Barbara' in the form"
            }
        ]

        expected_action = """enter_text"""
        expected_css_selector = """#billing_last_name"""
        expected_text = """Doe"""
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, expected_action, expected_css_selector, expected_text)
        logging.info('Test case 2 completed successfully')

    def test_case_3(self, setup, data_file_path):
        logging.info(
            'Starting test case 3 (billing_country): fill out the form on URL: https://mywebsite.testup.io/checkout/')
        session_id = 1234
        user_prompt = """fill out the form. You can skip optional inputs"""
        # Locate and read the HTML file
        file_path = data_file_path / 'myWebshop_checkout.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = [
            {
                'action': 'enter_text',
                'css_selector': '#billing_first_name',
                'text': 'Barbara',
                'explanation': 'Fill out the first name in the form',
                'description': "Enter the first name 'Barbara' in the form"
            },
            {
                'action': 'enter_text',
                'css_selector': '#billing_last_name',
                'text': 'Doe',
                'explanation': 'Fill out the last name in the form',
                'description': "Enter the last name 'Doe' in the form"
            }
        ]

        expected_action = """click"""
        expected_css_selector = """#billing_country"""
        expected_text = """"""
        logging.debug(
            f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, expected_action, expected_css_selector, expected_text)
        logging.info('Test case 3 completed successfully')

    def test_case_4(self, setup, data_file_path):
        logging.info('Starting test case 4 (billing_address_1): fill out the form on URL: https://mywebsite.testup.io/checkout/')
        session_id = 1234
        user_prompt = """fill out the form. You can skip optional inputs"""
        # Locate and read the HTML file
        file_path = data_file_path / 'myWebshop_checkout.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = [
            {
                'action': 'enter_text',
                'css_selector': '#billing_first_name',
                'text': 'Barbara',
                'explanation': 'Fill out the first name in the form',
                'description': "Enter the first name 'Barbara' in the form"
            },
            {
                'action': 'enter_text',
                'css_selector': '#billing_last_name',
                'text': 'Doe',
                'explanation': 'Fill out the last name in the form',
                'description': "Enter the last name 'Doe' in the form"
            },
            {
                'action': 'enter_text',
                'css_selector': '#billing_country',
                'text': 'Germany',
                'explanation': 'Fill out the country in the form',
                'description': "Select the country 'Germany' in the form"
            }
        ]

        expected_action = """enter_text"""
        expected_css_selector = """#billing_address_1"""
        expected_text = """Fake St. 13"""
        logging.debug(f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, expected_action, expected_css_selector, expected_text)
        logging.info('Test case 4 completed successfully')

    def test_case_5(self, setup, data_file_path):
        logging.info(
            'Starting test case 5 (billing_postcode): fill out the form on URL: https://mywebsite.testup.io/checkout/')
        session_id = 1234
        user_prompt = """fill out the form. You can skip optional inputs"""
        # Locate and read the HTML file
        file_path = data_file_path / 'myWebshop_checkout.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = [
            {
                'action': 'enter_text',
                'css_selector': '#billing_first_name',
                'text': 'Barbara',
                'explanation': 'Fill out the first name in the form',
                'description': "Enter the first name 'Barbara' in the form"
            },
            {
                'action': 'enter_text',
                'css_selector': '#billing_last_name',
                'text': 'Doe',
                'explanation': 'Fill out the last name in the form',
                'description': "Enter the last name 'Doe' in the form"
            },
            {
                'action': 'enter_text',
                'css_selector': '#billing_country',
                'text': 'Germany',
                'explanation': 'Fill out the country in the form',
                'description': "Select the country 'Germany' in the form"
            },
            {
                'action': 'enter_text',
                'css_selector': '#billing_address_1',
                'text': 'Fake St. 13',
                'explanation': 'Fill out the street address in the form',
                'description': "Enter the street address 'Fake St. 13' in the form"
            }
        ]

        expected_action = """enter_text"""
        expected_css_selector = """#billing_postcode"""
        expected_text = """21614"""
        logging.debug(
            f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, expected_action, expected_css_selector, expected_text)
        logging.info('Test case 5 completed successfully')

    def test_case_6(self, setup, data_file_path):
        logging.info(
            'Starting test case 6 (billing_city): fill out the form on URL: https://mywebsite.testup.io/checkout/')
        session_id = 1234
        user_prompt = """fill out the form. You can skip optional inputs"""
        # Locate and read the HTML file
        file_path = data_file_path / 'myWebshop_checkout.html'
        logging.debug(f"Reading HTML file from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = [
            {
                'action': 'enter_text',
                'css_selector': '#billing_first_name',
                'text': 'Barbara',
                'explanation': 'Fill out the first name in the form',
                'description': "Enter the first name 'Barbara' in the form"
            },
            {
                'action': 'enter_text',
                'css_selector': '#billing_last_name',
                'text': 'Doe',
                'explanation': 'Fill out the last name in the form',
                'description': "Enter the last name 'Doe' in the form"
            },
            {
                'action': 'enter_text',
                'css_selector': '#billing_country',
                'text': 'Germany',
                'explanation': 'Fill out the country in the form',
                'description': "Select the country 'Germany' in the form"
            },
            {
                'action': 'enter_text',
                'css_selector': '#billing_address_1',
                'text': 'Fake St. 13',
                'explanation': 'Fill out the street address in the form',
                'description': "Enter the street address 'Fake St. 13' in the form"
            },
            {
                'action': 'enter_text',
                'css_selector': '#billing_postcode',
                'text': '21614',
                'explanation': 'Fill out the ZIP code in the form',
                'description': "Enter the ZIP code '21614' in the form"
            }
        ]

        expected_action = """enter_text"""
        expected_css_selector = """#billing_city"""
        expected_text = """Buxtehude"""
        logging.debug(
            f"Calling get_actions with session_id={session_id}, user_prompt='{user_prompt}', actions_executed={actions_executed}, html_content_length={len(html_content)} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, expected_action, expected_css_selector, expected_text)
        logging.info('Test case 6 completed successfully')

