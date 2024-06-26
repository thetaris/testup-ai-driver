import datetime
import os
import time

import pytest
import logging
import pandas as pd
from dotenv import load_dotenv

from action_processor import DomAnalyzer, convert_keys_to_lowercase
from gpt_client import GptClient, RateLimitExceededError
import json


class TestmyWebshop_test:

    @pytest.fixture
    def setup(self):
        # Initialize an empty DataFrame with relevant columns
        self.results_df = pd.DataFrame(columns=["Test Name", "Task", "Attempt", "Score", "Total", "Score Percentage"])
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Define a directory for test results
        results_dir = "logs"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)  # Ensure the directory exists

        self.result_file = os.path.join(results_dir, f"test_results_{timestamp}.csv")

        # Load environment variables from .env file
        load_dotenv()
        logging.info('Test setup completed')
        self.gpt_client = GptClient()
        self.action_processor = DomAnalyzer()

        yield
        logging.info('Test teardown initiated')
        # Teardown code here, if any

    def test_training_data(self, setup, data_file_path):
        file_path = data_file_path / 'training_data.jsonl'
        counter = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                counter = counter+1
                print(f"Processing message {counter}")
                data = json.loads(line)
                max_attempts = 1
                for attempt in range(max_attempts):
                    prompts = []
                    total = 0
                    score = 0
                    task = ""
                    for message in data['messages']:
                        if message['role'] in ['user', 'system']:
                            prompts.append({'role': message['role'], 'message': message['content']})
                            search_phrase = 'Perform the task delimited by triple quotes: """'
                            start_index = message['content'].find(search_phrase)
                            if start_index != -1:
                                start_index += len(search_phrase)
                                end_index = message['content'].find('"""', start_index)
                                task = message['content'][start_index:end_index].strip()
                        elif message['role'] == 'assistant':
                            total = total+1
                            try:
                                response = self.gpt_client.make_request(prompts)
                                logging.info(f"actual: {response}")
                                logging.info(f"training_data: {message['content']}")
                                result = convert_keys_to_lowercase(self.action_processor.extract_steps(response))

                                if not result or result == {}:  # Check if the response is empty
                                    continue
                                assistant_actions = convert_keys_to_lowercase(json.loads(message['content']))
                                matched = False

                                counter = 0
                                for expected_item in assistant_actions:
                                    counter += 1
                                    if not matched:
                                        step = result.get('steps', [{}])[0]
                                        expected_action = expected_item.get('action', '').lower()
                                        if counter == 1:
                                            first_action = expected_action

                                        actual_action = step.get('action', '').lower()

                                        if expected_action == "finish" or expected_action == "scroll":
                                            if actual_action == expected_action:
                                                matched = True
                                            break

                                        if expected_action == actual_action:
                                            css_match = expected_item.get('css_selector', '') == step.get('css_selector', '')
                                            text_match = True
                                            if expected_action == 'enter_text':
                                                text_match = expected_item.get('text', '').lower() == step.get('text', '').lower()
                                            matched = css_match and text_match

                                    if matched:
                                        break

                                if matched:
                                    score += 1
                            except Exception as e:
                                logging.error(e)
                            finally:
                                prompts.append({'role': message['role'], 'message': first_action})
                    if attempt == 0:
                        logging.info(f"Task:{task}")
                    logging.info(f"Attempt#{attempt+1}: Score: {score}/{total}")

                    # Construct a new DataFrame for the current test results and concatenate it with the main DataFrame
                    new_row = pd.DataFrame({
                        "Test Name": [f"Test for {data_file_path.name}"],
                        "Task": [task],
                        "Attempt": [attempt + 1],
                        "Score": [score],
                        "Total": [total],
                        "Score Percentage": [f"{(score / total * 100) if total > 0 else 0}%"]
                    })
                    self.results_df = pd.concat([self.results_df, new_row], ignore_index=True)

        # Save results to CSV after all tests are completed
        self.results_df.to_csv(self.result_file, index=False)
        logging.info('Test case 1 completed successfully')

