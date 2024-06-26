import json
import logging
import sys
import os
sys.path.append('src')
from md_converter import convert_to_md


input_dir_path = 'data/input'

output_dir_path = 'data/output'

os.makedirs(output_dir_path, exist_ok=True)

for filename in os.listdir(input_dir_path):
    input_file_path = os.path.join(input_dir_path, filename)

    # Check if it's a file and not a directory
    if os.path.isfile(input_file_path):
        with open(input_file_path, 'r') as input_file:
            data = json.load(input_file)

        modified_json_line = []

        for item in data:
            # Check each message for the relevant content
            for message in item["messages"]:
                # Look for the specific phrases in the content
                if message["role"] == "assistant":
                    assistant_content = json.loads(message["content"])
                    try:
                        message["content"] = assistant_content[0]
                    except Exception as e:
                        logging.error(e)
                else:
                    if "Here is the Markdown" in message["content"] or "Here is the new markdown" in message["content"]:
                        # Extract the HTML content
                        html_content = message["content"]
                        # Convert the HTML to Markdown
                        markdown_content = convert_to_md(html_content)
                        # Replace the original content with the new Markdown content
                        message["content"] = markdown_content

            modified_json_line.append(json.dumps(item, ensure_ascii=False))

        # Construct the output file path
        output_file_path = os.path.join(output_dir_path, os.path.splitext(filename)[0] + '_md.jsonl')

        # Write the modified JSON string to the output file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(modified_json_line))

        print(f"The modified content has been written to '{output_file_path}'")