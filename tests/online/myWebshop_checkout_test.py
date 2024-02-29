import pytest
import logging
from pathlib import Path
from test_utils import assert_chatGPT_response
from action_processor import DomAnalyzer


class TestmyWebshop_checkout:

    @pytest.fixture
    def setup(self, data_file_path):
        # Initialize DomAnalyzer instance and read HTML content once
        self.instance = DomAnalyzer()
        file_path = data_file_path / 'myWebshop_checkout.html'
        with open(file_path, 'r', encoding='utf-8') as file:
            self.html_content = file.read()
        self.session_id = 1234
        self.user_prompt = """fill out the form. You can skip optional inputs"""
        self.variables_map = {
            "First_name": "Barbara",
            "Last_name": "Doe",
            "Country": "Germany",
            "Street_address": "Fake St. 13",
            "ZIP": 21614,
            "City": "Buxtehude",
            "Phone": "089123456789",
            "Email": "demo@testup.io"
        }
        self.variables_string = self.instance.variableMap_to_string(self.variables_map)

        logging.info('Test setup completed')
        yield
        logging.info('Test teardown initiated')

    def execute_test_case(self, actions_executed, expected_action, expected_css_selector, expected_text):
        logging.debug(
            f"Calling get_actions with session_id={self.session_id}, user_prompt='{self.user_prompt}', actions_executed={actions_executed}, html_content_length={len(self.html_content)} ")
        actual_response = self.instance.get_actions(self.session_id, self.user_prompt, self.html_content,
                                                    actions_executed, self.variables_string)
        assert_chatGPT_response(actual_response, expected_action, expected_css_selector, expected_text)

    def test_case_1(self, setup):
        actions_executed = ""
        self.execute_test_case(actions_executed, "enter_text", "#billing_first_name", "Barbara")
        logging.info('Test case 1 completed successfully')

    def test_case_2(self, setup):
        actions_executed = [
            {
                'action': 'enter_text',
                'css_selector': '#billing_first_name',
                'text': 'Barbara',
                'explanation': 'Fill out the first name in the form',
                'description': "Enter the first name 'Barbara' in the form"
            }
        ]
        self.execute_test_case(actions_executed, "enter_text", "#billing_last_name", "Doe")
        logging.info('Test case 2 completed successfully')

    def test_case_3(self, setup):
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
        self.execute_test_case(actions_executed, "click", "#billing_country", "")
        logging.info('Test case 3 completed successfully')

    def test_case_4(self, setup):
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
        self.execute_test_case(actions_executed, "enter_text", "#billing_address_1", "Fake St. 13")
        logging.info('Test case 4 completed successfully')

    def test_case_5(self, setup):
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
        self.execute_test_case(actions_executed, "enter_text", "#billing_postcode", "21614")
        logging.info('Test case 5 completed successfully')

    def test_case_6(self, setup):
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
        self.execute_test_case(actions_executed, "enter_text", "#billing_city", "Buxtehude")
        logging.info('Test case 6 completed successfully')

    def test_case_7(self, setup):
        actions_executed = [
            {"action": "enter_text", "css_selector": "#first_name", "text": "Barbara",
             "explanation": "Fill in first name",
             "description": "Enter the first name 'Barbara' into the appropriate field."},
            {"action": "enter_text", "css_selector": "#last_name", "text": "Doe", "explanation": "Fill in last name",
             "description": "Enter the last name 'Doe' into the appropriate field."},
            {"action": "enter_text", "css_selector": "#country", "text": "Germany", "explanation": "Fill in country",
             "description": "Enter the country 'Germany' into the appropriate field."},
            {"action": "enter_text", "css_selector": "#street_address", "text": "Fake St. 13",
             "explanation": "Fill in street address",
             "description": "Enter the street address 'Fake St. 13' into the appropriate field."},
            {"action": "enter_text", "css_selector": "#zip_code", "text": "21614", "explanation": "Fill in ZIP code",
             "description": "Enter the ZIP code '21614' into the appropriate field."},
            {"action": "enter_text", "css_selector": "#city", "text": "Buxtehude", "explanation": "Fill in city",
             "description": "Enter the city 'Buxtehude' into the appropriate field."},
            {"action": "enter_text", "css_selector": "#phone", "text": "089123456789",
             "explanation": "Fill in phone number",
             "description": "Enter the phone number '089123456789' into the appropriate field."},
            {"action": "enter_text", "css_selector": "#email", "text": "demo@testup.io", "explanation": "Fill in email",
             "description": "Enter the email 'demo@testup.io' into the appropriate field."}
        ]
        self.execute_test_case(actions_executed, "finish", "", "")
        logging.info('Test case 7 completed successfully')
