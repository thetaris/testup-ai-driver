from bs4 import BeautifulSoup
from markdownify import markdownify as md
from gpt_api_spec import api_map
import requests
import re
import sys
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DomAnalyzer:
    gpt_api_key = os.getenv("API_KEY")
    gpt_model = os.getenv("GPT_MODEL")
    gpt_prompt = os.getenv("GPT_PROMPT")

    def __init__(self):
        if self.gpt_model not in api_map:
            raise ValueError(f"Model '{self.gpt_model}' is not supported")

    def analyze(self, deviceId, user_prompt, html_doc):

        html_doc = re.sub('<script[^>]*>[^<]*</script>', '', html_doc)

        html_doc = re.sub('<link .*?/>', '', html_doc)

        html_doc = re.sub('<img[^>]*>', '', html_doc)

        html_doc = re.sub('<!--.*?-->', '', html_doc)

        html_doc = re.sub('data-link-behaviour="[^"]*"', '', html_doc, flags=re.DOTALL)

        html_doc = re.sub('data-modalopenparam="[^"]*"', '', html_doc, flags=re.DOTALL)

        html_doc = re.sub('data-loadedonopen="[^"]*"', '', html_doc, flags=re.DOTALL)

        html_doc = re.sub('data-tabber-content="[^"]*"', '', html_doc, flags=re.DOTALL)

        html_doc = re.sub('style="[^"]*"', '', html_doc, flags=re.DOTALL)

        html_doc = re.sub('role="[^"]*"', '', html_doc, flags=re.DOTALL)

        html_doc = re.sub('height="[^"]*"', '', html_doc, flags=re.DOTALL)

        html_doc = re.sub('color="[^"]*"', '', html_doc, flags=re.DOTALL)

        html_doc = re.sub('width="[^"]*"', '', html_doc, flags=re.DOTALL)

        html_doc = re.sub('x="[^"]*"', '', html_doc, flags=re.DOTALL)

        html_doc = re.sub('y="[^"]*"', '', html_doc, flags=re.DOTALL)

        html_doc = re.sub('href="[^"]*"', '', html_doc, flags=re.DOTALL)

        html_doc = re.sub(r'<source[^>]*>', '', html_doc, flags=re.DOTALL)
        html_doc = re.sub(r'<svg.*?>.*?</svg>', '', html_doc, flags=re.DOTALL)

        logging.info(f"html_doc: {html_doc}")

        logging.info('------------------------------------------------')
        logging.info('------------------------------------------------')
        logging.info('------------------------------------------------')
        logging.info('------------------------------------------------')
        logging.info('------------------------------------------------')

        markdown_content = self.convert_to_md(html_doc)

        markdown_content = re.sub('\s+', ' ', markdown_content)

        # removing unneeded spaces
        logging.info(f"Markdown: {markdown_content}")
        final_content = f"{markdown_content}\n{user_prompt}\n{self.gpt_prompt}"

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

    def convert_to_md(self, dom):
        soup = BeautifulSoup(dom, 'html.parser')

        for tag in soup.find_all(['li', 'button', 'input', 'textarea', 'a'], id=True):
            # Initialize an empty list to hold the desired attributes
            desired_attributes = []

            for attr, value in tag.attrs.items():
                if attr != 'class':
                    desired_attributes.append(f'{attr}="{value}"')

            # Join the desired attributes into a single string
            attributes_str = ' '.join(desired_attributes)

            # Replace tag with a modified version that includes only the desired attributes
            tag.replace_with(f'<{tag.name}.postfix {attributes_str}>{tag.get_text()}</{tag.name}>')

        # Convert the modified HTML to Markdown
        markdown = md(str(soup), strip=['span'])

        # Remove '.postfix' from tag names in the Markdown content
        markdown = re.sub(r'(\w+)\.postfix', r'\1', markdown)

        return markdown
