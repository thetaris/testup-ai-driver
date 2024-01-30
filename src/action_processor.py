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
    gpt_prompt = os.getenv("GPT_PROMPT")
    gpt_check_prompt = os.getenv("GPT_CHECK_PROMPT")

    def __init__(self):
        if self.gpt_model not in api_map:
            raise ValueError(f"Model '{self.gpt_model}' is not supported")

    def get_actions(self, deviceId, user_prompt, html_doc):

        markdown_content = convert_to_md(html_doc)

        # removing unneeded spaces
        logging.info(f"Markdown: {markdown_content}")
        final_content = f"{markdown_content}\n{user_prompt}\n{self.gpt_prompt}"

        api_info = api_map_json[self.gpt_model]
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

