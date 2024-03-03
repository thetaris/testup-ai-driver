import pytest

import logging
from action_processor import DomAnalyzer
import json

class Test_action_processor:

    def test_extract_steps(self, data_file_path):
        output_str = """
        The next action needed to complete the task is to click on the "Checkout" link.                                                                                                                                       
         Here are the steps to complete the task:                                                                                                                                                                                                                                                    
         {                                                                                                                                                                                                                                                                                         
         "steps": [                                                                                                                                                                                                                                                                                
             {                                                                                                                                                                                                                                                                                    
               "action": "click",                                                                                                                                                                                                                                                               
               "css_selector": "#autoidtestup21",                                                                                                                                                                                                                                               
             "explanation": "To navigate to the checkout page.",                                                                                                                                                                                                                             
             "description": "Click on the 'Checkout' link."                                                                                                                                                                                                                                   
             }                                                                                                                                                                                                                                                                                  
         ]                                                                                                                                                                                                                                                                                        
         }
        """
        expected_response = {
            "steps": [
                {
                    "action": "click",
                    "css_selector": "#autoidtestup21",
                    "explanation": "To navigate to the checkout page.",
                    "description": "Click on the 'Checkout' link."
                }
            ]
        }
        actual_response = DomAnalyzer().extract_steps(output_str)

        assert actual_response == expected_response, "The actual response does not match the expected response."


    def test_resolve_followup_duplicate(self):
        result = DomAnalyzer().resolve_followup(True, False, 'Action1')
        assert result == "Please note that the last action you provided is duplicate, so this action Action1 has already been executed"

    def test_resolve_followup_invalid(self):
        result = DomAnalyzer().resolve_followup(False, False, 'Action2')
        assert result == "Please note that the last action you provided is invalid given the provided markdown. Action2, please try again"

    def test_resolve_followup(self):
        result = DomAnalyzer().resolve_followup(False, True, 'Action3')
        assert result == ""