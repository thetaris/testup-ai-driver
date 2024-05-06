import threading
import os
import logging
import tiktoken
from pathlib import Path

import requests
import json

from rate_limiter import RateLimiter
from gpt_api_spec import api_map_json
from dotenv import load_dotenv
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GptClient:
    # Load environment variables from .env file
    path_to_env_file = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=path_to_env_file, verbose = True)

    gpt_api_key = os.getenv("OPENAI_API_KEY")
    x_api_key = os.getenv('X_API_KEY', "")
    max_requests_per_minute = os.getenv("MAX_REQUESTS", 10)
    max_tokens_per_minute = os.getenv("MAX_TOKENS", 160000)
    gpt_model = os.getenv("GPT_MODEL", "gpt-3.5-turbo-1106")

    def __init__(self):
        logging.info("initiating GPT client")
        self.operation_lock = threading.Lock()
        if "gpt" in self.gpt_model:
            self.rate_limiter = RateLimiter(max_requests_per_minute=20, max_tokens_per_minute=160000)
        elif "claude-3-opus" in self.gpt_model:
            self.rate_limiter = RateLimiter(max_requests_per_minute=10, max_tokens_per_minute=20000)
        elif "claude-3-haiku" in self.gpt_model:
            self.rate_limiter = RateLimiter(max_requests_per_minute=10, max_tokens_per_minute=50000)
        elif "claude-3-sonnet" in self.gpt_model:
            self.rate_limiter = RateLimiter(max_requests_per_minute=10, max_tokens_per_minute=40000)
        else:
            raise Exception("No Rate Limiter for this model configured")

    def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo-1106"):
        """Return the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if model in {
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-4-0314",
            "gpt-4-32k-0314",
            "gpt-4-0613",
            "gpt-4-32k-0613",
        }:
            tokens_per_message = 3
            tokens_per_name = 1
        elif model == "gpt-3.5-turbo-0301":
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif "gpt-3.5-turbo" in model:
            print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
            return messages.num_tokens_from_messages(messages, model="gpt-3.5-turbo-1106")
        elif "gpt-4" in model:
            print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
            return messages.num_tokens_from_messages(messages, model="gpt-4-0613")
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
            )
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

    def make_request(self, contents):

        if "gpt-3.5-turbo-1106" in self.gpt_model:
            api_info = api_map_json["gpt-3.5-turbo-1106"]
        elif "gpt-3.5-turbo" in self.gpt_model:
            api_info = api_map_json["gpt-3.5-turbo"]
        elif "claude-3-opus-20240229" in self.gpt_model:
            api_info = api_map_json["claude-3-opus-20240229"]
        elif "claude-3-haiku-20240307" in self.gpt_model:
            api_info = api_map_json["claude-3-haiku-20240307"]
        elif "claude-3-sonnet-20240229" in self.gpt_model:
            api_info = api_map_json["claude-3-sonnet-20240229"]



        payload = api_info['payload'](self.gpt_model, contents)
        num_token = self.num_tokens_from_messages(payload["messages"])
        self.rate_limiter.wait_and_check(num_token)

        if self.gpt_model in ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]:
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

            logging.info("##############################################################################################################")
            logging.info(f"sending:  {contents}")
            logging.info("##############################################################################################################")

            response = requests.post(api_info['endpoint'], headers=headers, json=payload)
            return self.extract_response_gpt(response)



    def extract_response_gpt(self, response):
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
        elif "error" in response_data and response_data["error"].get("type", "") == 'context_length_exceeded':
            raise TokenLimitExceededError(response_data["error"].get("message", "Token limit exceeded"))
        elif "error" in response_data and response_data["error"].get("type", "") == 'rate_limit_error':
            raise RateLimitExceededError(response_data["error"].get("message", "Rate limit exceeded"))
        else:
            raise Exception(f"No content found in response or invalid response format:{response_data}")


class TokenLimitExceededError(Exception):
    """GPT token limit exceeded"""
    pass


class RateLimitExceededError(Exception):
    """GPT token limit exceeded"""
    pass
