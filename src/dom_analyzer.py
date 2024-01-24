from bs4 import BeautifulSoup
from markdownify import markdownify as md
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
        final_content = f"{markdown_content}\n {user_prompt} \nwrite me the steps to take as a json list. Each entry is an object of 3 fields, first field is action which can be one of: click, enter_text, wait. The second field is css_selector. The third field is optional text. Only return json"

        payload = {
            "model": "gpt-3.5-turbo-1106",
            "messages": [{"role": "user", "content": final_content}]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.gpt_api_key}"
        }

        # Send POST request to OpenAI API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        response_data = response.json()

        logging.info(f"Response from openai {response_data}")

        if "choices" in response_data and len(response_data["choices"]) > 0:
            assistant_message_json_str = response_data["choices"][0].get("message", {}).get("content", "")
            total_tokens = response_data["usage"].get("total_tokens", 0)

            try:
                # Parse the extracted content as JSON
                assistant_message = json.loads(assistant_message_json_str)
            except json.JSONDecodeError:
                raise Exception("Error decoding the extracted content as JSON.")

            # Store in new JSON object
            extracted_data = {
                "extracted_content": assistant_message,
                "total_tokens": total_tokens
            }

            logging.info(f"Returning: {extracted_data}")
            return extracted_data
        else:
            raise Exception(f"No content found in response or invalid response format:{response_data}")

    def convert_to_md(self, dom):
        soup = BeautifulSoup(dom, 'html.parser')

        for tag in soup.find_all(['li', 'button', 'input', 'textarea', 'a'], id=True):
            logging.info(f"found {tag}")

            # Initialize an empty list to hold the desired attributes
            desired_attributes = []

            # Preserve 'id' attribute
            if 'id' in tag.attrs:
                desired_attributes.append(f'id="{tag.attrs["id"]}"')

            # Preserve 'value' attribute, if it exists
            if 'value' in tag.attrs:
                desired_attributes.append(f'value="{tag.attrs["value"]}"')

            # Join the desired attributes into a single string
            attributes_str = ' '.join(desired_attributes)

            # Replace tag with a modified version that includes only the desired attributes
            tag.replace_with(f'<{tag.name}.postfix {attributes_str}>{tag.get_text()}</{tag.name}>')

        # Convert the modified HTML to Markdown
        markdown = md(str(soup), strip=['span'])

        # Remove '.postfix' from tag names in the Markdown content
        markdown = re.sub(r'(\w+)\.postfix', r'\1', markdown)

        return markdown

        return markdown
