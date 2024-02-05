from gpt_api_spec import api_map, api_map_json
from md_converter import convert_to_md
import requests
import json
import os
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DomAnalyzer:
    gpt_api_key = os.getenv("API_KEY")
    gpt_model = os.getenv("GPT_MODEL")
    gpt_prompt = os.getenv("GPT_PROMPT", """
    You are a browser automation assistant. Your job is to analyze the already executed actions and determine the next actions needed to complete the provided task.
    The actions that you can take are:
    1.click (if you need to click something on the screen)
    2.enter_text (if you believe you need to write something)
    3.wait (when the previous    action changed the source code and you need the new source code)
    4.finish (at the end to know that we are done or if all actions has been executed)
    5.error ( the given task cannot be accomplished)
    You will be given:
    - a markdown of the currently visible section of the website you are on
    - a task, which you should try to execute on the current page
    - previously executed actions
    Analyze the already taken actions and write me a json list of actions that still have to be done (i.e. are not part of the previously executed actions).
    Each entry is an object of 4 fields, the fields are the following: 
    1.action: can be one of: click, enter_text, error, or finish. 
    2.css_selector: (only needed for click or enter-text), this is the css id of the html element('li', 'button', 'input', 'textarea', 'a').
    3.text: this is optional and contains the text you want to input in case of an enter-text action. 
    4.explanation: is why you chose this action. 
    5.description: detailed description of the action
    The output format should be {"steps":[{ "action":..,"css_selector":...., "text":..., "explanation":..., "description":...}]
    \n
    """)
    gpt_check_prompt = os.getenv("GPT_CHECK_PROMPT")

    def __init__(self):
        if self.gpt_model not in api_map:
            raise ValueError(f"Model '{self.gpt_model}' is not supported")

    def get_actions(self, deviceId, user_prompt, html_doc, actions_executed):

        logging.info(f"System input: {self.gpt_prompt}")
        markdown_content = convert_to_md(html_doc)

        # removing unneeded spaces
        logging.info(f"Markdown: {markdown_content}")
        user_content = f"Here is the Markdown: {markdown_content}.\nAnd this is your task: {user_prompt}"

        if actions_executed:
            user_content += f"\nAnd these are the previous actions: {actions_executed}"

        api_info = api_map_json[self.gpt_model]
        payload = api_info['payload'](self.gpt_model, self.gpt_prompt, user_content)
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
                logging.info(f"assistant_message_json_str = {assistant_message_json_str}")
                assistant_message_json_str = assistant_message_json_str.replace("```json", "").replace("```", "").strip()

                assistant_message = json.loads(assistant_message_json_str)
            except json.JSONDecodeError:
                raise Exception("Error decoding the extracted content as JSON.")

            logging.info(f"Tokens: {total_tokens}")
            # Store in new JSON object

            logging.info(f"Returning: {assistant_message}")
            return assistant_message
        else:
            raise Exception(f"No content found in response or invalid response format:{response_data}")

    def check_actions(self, deviceId, user_prompt, html_doc):

        markdown_content = convert_to_md(html_doc)

        # removing unneeded spaces
        logging.info(f"Markdown: {markdown_content}")
        final_content = f"This is markdown for my website: \"{markdown_content}\"\n{self.gpt_check_prompt}: \"{user_prompt}\""

        api_info = api_map[self.gpt_model]
        payload = api_info['payload'](self.gpt_model, final_content)
        logging.info(f"sending request {payload}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.gpt_api_key}"
        }

        # Send POST request to OpenAI API
        response = requests.post(api_info['endpoint'], headers=headers, json=payload)

        response_data = response.json()

        logging.info(f"Response from openai {response_data}")

        content = response_data['choices'][0]['message']['content']

    # Define keywords or phrases that indicate a negative response
        negative_indicators = ["no", "not possible", "cannot", "unable to"]

        # Check if any of the negative indicators are in the content
        if any(re.search(r'\b' + indicator + r'\b', content, re.IGNORECASE) for indicator in negative_indicators):
            return False

        # Define keywords or phrases that indicate a positive response
        positive_indicators = ["yes", "it is possible", "can", "able to"]

        # Check if any of the positive indicators are in the content
        return any(re.search(r'\b' + indicator + r'\b', content, re.IGNORECASE) for indicator in positive_indicators)

