from gpt_api_spec import api_map, api_map_json
from md_converter import convert_to_md
from cachetools import TTLCache
import requests
import json
import os
import logging
import re
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DomAnalyzer:
    gpt_api_key = os.getenv("OPENAI_API_KEY")
    gpt_model = os.getenv("GPT_MODEL", "gpt-3.5-turbo-1106")
    gpt_prompt = os.getenv("GPT_PROMPT", """
     You are a browser automation assistant. Your job is to analyze the already executed actions and determine the next actions needed to complete the provided task.
    The actions that you can take are:
    1. click (if you need to click something on the screen)
    2. enter_text (if you believe you need to write something)
    3. wait (when the previous action changed the source code and you need the new source code)
    4. finish (at the end to know that we are done or if all actions have been executed)
    5. error ( the given task cannot be accomplished)
    You will be given:
    - a markdown of the currently visible section of the website you are on
    - A list of already executed actions that we no longer need to execute. They should not be in the output at all
    - a task, that you should try to execute on the current page (remember to not repeat already executed actions)
    
    Each entry is an object of 5 fields, the fields are the following:
    1. action: can be one of: click, enter_text, wait, error, or finish.
    2. css_selector: (only needed for click or enter-text), this is the css id of the html element(\'li\', \'button\', \'input\', \'textarea\', \'a\'). Always use the ID of the element as css selector!
    3. text: this is optional and contains the text you want to input in case of an enter-text action. 
    4. explanation: this is why you chose this action.
    5. description: detailed description of the action
    The output format should be {"steps":[{ "action":..,"css_selector":...., "text":..., "explanation":..., "description":...}]}
    \n
    """)
    gpt_check_prompt = os.getenv("GPT_CHECK_PROMPT")
    session_histories = {}
    system_input_default = """
    You are a testautomation system. Your job is to analyze the already executed actions and determine the next actions needed to complete the provided task.
    
    The actions that you can take are:
        1. click (if you need to click something on the screen)
        2. enter_text (if you believe you need to write something)
        3. scroll (if you are instructed to scroll or scrolling is needed to complete action)
        4. finish (at the end to know that we are done or if all actions have been executed)
        5. error ( the given task cannot be accomplished)

     Each entry is an object of 5 fields, the fields are the following:
        1. action: can be one of: click, enter_text, wait, error, or finish.
        2. css_selector: (only needed for click or enter-text), this is the css id of the html element('li', 'button', 'input', 'textarea', 'a'), example #id.
        3. text: this is optional and contains the text you want to input in case of an enter-text action. 
        4. explanation: this is why you chose this action.
        5. description: detailed description of the action
        The output format should be {"steps":[{ "action":..,"css_selector":...., "text":..., "explanation":..., "description":...}]}
    """

    user_input_default = """\n\nAlready executed actions:\n @@@last_played_actions@@@ \n 
    \n\nAnd this is your task: @@@task@@@
    \n\nYou can use the information given by this set of variables to complete your task: 
    \n @@@variables@@@
    \n\nImagine you already executed the given list of \"previous actions\", what actions remain to complete the following task, (remember to just return "finish" if you think you are done with your task):
    \n - @@@task@@@ \n

    \n Here is the Markdown: @@@markdown@@@
    """


    def __init__(self):
        self.session_histories = TTLCache(maxsize=1000, ttl=3600)
        if self.gpt_model not in api_map:
            raise ValueError(f"Model '{self.gpt_model}' is not supported")

    def get_actions(self, session_id, user_prompt, html_doc, actions_executed, variables_string="- no variables available -", user_input=user_input_default, system_input=system_input_default):

        markdown_content = convert_to_md(html_doc)

        # removing unneeded spaces
        logging.info(f"Markdown: {markdown_content}")


        executed_actions_str = '\n'.join([f"{idx+1}.{self.format_action(action)}" for idx, action in enumerate(actions_executed)])
        user_input = user_input.replace("@@@last_played_actions@@@", executed_actions_str)
        system_input = system_input.replace("@@@last_played_actions@@@", executed_actions_str)

        user_input = user_input.replace("@@@markdown@@@", markdown_content)
        system_input = system_input.replace("@@@markdown@@@", markdown_content)

        user_input = user_input.replace("@@@task@@@", user_prompt)
        system_input = system_input.replace("@@@task@@@", user_prompt)

        user_input = user_input.replace("@@@variables@@@", variables_string)
        system_input = system_input.replace("@@@variables@@@", variables_string)

        assistant_prompt = []
        assistant_prompt.extend(action for action in actions_executed)
        logging.info(f"Assistant prompt: {assistant_prompt}")

        api_info = api_map_json[self.gpt_model]
        payload = api_info['payload'](self.gpt_model, system_input, user_input, assistant_prompt)
        logging.info(f"sending request {payload}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.gpt_api_key}"
        }

        # Send POST request to OpenAI API
        response = requests.post(api_info['endpoint'], headers=headers, json=payload)

        response_data = response.json()

        logging.info(f"Response from openai {response_data}")

        response_object_type = response_data.get('object', '')

        if "choices" in response_data and len(response_data["choices"]) > 0:
            if response_object_type == 'chat.completion':
                # Handling response for 'chat.completion'
                assistant_message_json_str = response_data["choices"][0].get("message", {}).get("content", "")
            elif response_object_type == 'text_completion':
                # Handling response for 'text_completion'
                assistant_message_json_str = response_data["choices"][0].get("text", "")
            else:
                raise Exception("Unknown response object type.")

            total_tokens = response_data["usage"].get("total_tokens", 0)

            try:
                # Parse the extracted content as JSON
                assistant_message_json_str = assistant_message_json_str.replace("```json", "").replace("```", "").strip()
                logging.info(f"return assistant_message_json_str = {assistant_message_json_str}")
                assistant_message_json_str = self.extract_steps(assistant_message_json_str)
                logging.info(f"final assistant_message_json_str = {assistant_message_json_str}")

                assistant_message = assistant_message_json_str
            except json.JSONDecodeError:
                raise Exception("Error decoding the extracted content as JSON.")

            logging.info(f"Tokens: {total_tokens}")
            # Store in new JSON object
            assistant_message = self.parse_output(assistant_message)
            logging.info(f"Returning: {assistant_message}")
            return assistant_message
        else:
            raise Exception(f"No content found in response or invalid response format:{response_data}")

    def format_action(self, action):
        return f"{{\"action\": \"{action['action']}\", \"css_selector\": \"{action['css_selector']}\", \"Text\": \"{action['text']}\", \"explanation\": \"{action['explanation']}\", \"description\": \"{action['description']}\"}}"

    def extract_steps(self, json_str):
        # Attempt to find the JSON start, assuming it might be embedded in a larger string
        json_start = json_str.find('{"steps"')
        if json_start != -1:
            json_str = json_str[json_start:]
        try:
            data = json.loads(json_str)
            return data
        except json.JSONDecodeError:
            print("Error decoding JSON")
            return []

    def variableMap_to_string(self, input_map):

        if not input_map:
            return "- no variables available -"

        # Initialize an empty string
        output_string = "\n\nYou can use the information given by this set of variables to complete your task:\n"
        # Iterate through the map to format the string
        for index, (key, value) in enumerate(input_map.items(), start=1):
            output_string += f"-{key} = {value}\n"
        # Remove the last newline character for clean output
        return output_string.rstrip()

    def parse_output(self, assistant_message):
        # First, try to parse the entire message as JSON
        try:
            data = json.loads(assistant_message)
            if 'steps' in data:
                return data
        except json.JSONDecodeError:
            pass
        pattern = r'(\{.*"steps".*\})'
        matches = re.findall(pattern, assistant_message, re.DOTALL)

        for match in matches:
            try:
                potential_json = match
                parsed_json = json.loads(potential_json)
                if 'steps' in parsed_json:
                    return parsed_json
            except json.JSONDecodeError as e:
                continue

        logging.info("Unable to parse JSON structure from the message")
        return None
