import pytest

import logging
from action_processor import DomAnalyzer
import json

class Test_action_processor:

    def test_parse_output(self, data_file_path):
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
        actual_response = DomAnalyzer().parse_output(output_str)

        assert actual_response == expected_response, "The actual response does not match the expected response."