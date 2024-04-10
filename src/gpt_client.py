import threading
import os
import logging
import requests
import json

from rate_limiter import RateLimiter
from gpt_api_spec import api_map_json
from dotenv import load_dotenv
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GptClient:
    # Load environment variables from .env file
    load_dotenv()
    gpt_api_key = os.getenv("OPENAI_API_KEY")
    x_api_key = os.getenv("X_API_KEY", "")
    max_requests_per_minute = os.getenv("MAX_REQUESTS", 20)
    max_tokens_per_minute = os.getenv("MAX_TOKENS", 160000)
    gpt_model = os.getenv("GPT_MODEL", "gpt-3.5-turbo-1106")

    def __init__(self):
        logging.debug("initiating GPT client")
        self.operation_lock = threading.Lock()
        self.rate_limiter = RateLimiter(max_requests_per_minute=20, max_tokens_per_minute=160000)

    def make_request(self, contents):
        if self.rate_limiter.wait_and_check():
            if "gpt-3.5-turbo-1106" in self.gpt_model:
                api_info = api_map_json["gpt-3.5-turbo-1106"]
            elif "gpt-3.5-turbo" in self.gpt_model:
                api_info = api_map_json["gpt-3.5-turbo"]
            elif "claude-3-opus-20240229" in self.gpt_model:
                api_info = api_map_json["claude-3-opus-20240229"]
            elif "claude-3-haiku-20240307" in self.gpt_model:
                api_info = api_map_json["claude-3-haiku-20240307"]
            else:
                raise Exception("Failed to get tokens to execute request")
            payload = api_info['payload'](self.gpt_model, contents)
            logging.info("##############################################################################################################")
            logging.info(f"sending:  {contents}")
            logging.info("##############################################################################################################")

            if self.gpt_model in ["claude-3-opus-20240229","claude-3-haiku-20240307"]:
                headers = {
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01",
                    "x-api-key": f"{self.x_api_key}"
                }
                response = requests.post(api_info['endpoint'], headers=headers, json=payload)
                return self.extract_response_claude(response)

            else:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.gpt_api_key}"
                }
                response = requests.post(api_info['endpoint'], headers=headers, json=payload)
                return self.extract_response_gpt(response)

        logging.error("Failed to get tokens to execute request")
        raise Exception("Failed to get tokens to execute request")

    def extract_response_gpt(self, response):
        response_data = response.json()

        logging.debug(f"Response from openai {response_data}")

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
                assistant_message = assistant_message_json_str
            except json.JSONDecodeError:
                raise Exception("Error decoding the extracted content as JSON.")

            return assistant_message
        elif "error" in response_data and response_data["error"].get("code", "") == 'context_length_exceeded':
            raise TokenLimitExceededError(response_data["error"].get("message", "Token limit exceeded"))
        elif "error" in response_data and response_data["error"].get("code", "") == 'rate_limit_exceeded':
            raise RateLimitExceededError(response_data["error"].get("message", "Rate limit exceeded"))
        else:
            raise Exception(f"No content found in response or invalid response format:{response_data}")

    def extract_response_claude(self, response):
        response_data = response.json()

        logging.info(f"Response from anthropic {response_data}")

        response_object_type = response_data.get('type', '')

        if "content" in response_data and len(response_data["content"]) > 0:
            if response_object_type == 'message':
                # Handling response for 'chat.completion'
                assistant_message_json_str = response_data["content"][0].get("text", {})
            # elif response_object_type == 'text_completion':
            #     # Handling response for 'text_completion'
            #     assistant_message_json_str = response_data["choices"][0].get("text", "")
            else:
                raise Exception("Unknown response object type.")

            total_tokens = response_data["usage"].get("input_tokens", 0)
            self.rate_limiter.add_token_consumed(total_tokens)

            try:
                # Parse the extracted content as JSON
                assistant_message_json_str = assistant_message_json_str.replace("```json", "").replace("```", "").strip()
                assistant_message = assistant_message_json_str
            except json.JSONDecodeError:
                raise Exception("Error decoding the extracted content as JSON.")

            return assistant_message
        elif "error" in response_data and response_data["error"].get("code", "") == 'context_length_exceeded':
            raise TokenLimitExceededError(response_data["error"].get("message", "Token limit exceeded"))
        elif "error" in response_data and response_data["error"].get("code", "") == 'rate_limit_exceeded':
            raise RateLimitExceededError(response_data["error"].get("message", "Rate limit exceeded"))
        else:
            raise Exception(f"No content found in response or invalid response format:{response_data}")


class TokenLimitExceededError(Exception):
    """GPT token limit exceeded"""
    pass


class RateLimitExceededError(Exception):
    """GPT token limit exceeded"""
    pass
