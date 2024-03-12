import threading
import os
import logging
import requests
import json

from rate_limiter import RateLimiter
from gpt_api_spec import api_map, api_map_json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GptClient:

    gpt_api_key = os.getenv("OPENAI_API_KEY")
    max_requests_per_minute = os.getenv("MAX_REQUESTS", 20)
    max_tokens_per_minute = os.getenv("MAX_TOKENS", 160000)
    gpt_model = os.getenv("GPT_MODEL", "gpt-3.5-turbo-1106")

    def __init__(self):
        self.operation_lock = threading.Lock()
        self.rate_limiter = RateLimiter(max_requests_per_minute=20, max_tokens_per_minute=160000)

    def make_request(self, contents):
        if self.rate_limiter.wait_and_check():
            logging.info("Going to make request")
            api_info = api_map_json[self.gpt_model]
            payload = api_info['payload'](self.gpt_model, contents)
            logging.info(f"sending request {payload}")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.gpt_api_key}"
            }

            response = requests.post(api_info['endpoint'], headers=headers, json=payload)
            return self.extract_response(response)
        logging.error("Failed to get tokens to execute request")
        raise Exception("Failed to get tokens to execute request")

    def extract_response(self, response):
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
            self.rate_limiter.add_token_consumed(total_tokens)

            try:
                # Parse the extracted content as JSON
                assistant_message_json_str = assistant_message_json_str.replace("```json", "").replace("```", "").strip()
                logging.info(f"return assistant_message_json_str = {assistant_message_json_str}")
                logging.info(f"final assistant_message_json_str = {assistant_message_json_str}")

                assistant_message = assistant_message_json_str
            except json.JSONDecodeError:
                raise Exception("Error decoding the extracted content as JSON.")

            logging.info(f"Tokens: {total_tokens}")
            # Store in new JSON object
            logging.info(f"Returning: {assistant_message}")
            return assistant_message
        else:
            raise Exception(f"No content found in response or invalid response format:{response_data}")

