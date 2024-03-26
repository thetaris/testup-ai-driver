import json
import sys
sys.path.append('../src')
from md_converter import convert_to_md


input_file_path = '../data/input/training_data_html.json'

output_file_path = '../data/output/training_data_md.json'

with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

for item in data:
    # Check each message for the relevant content
    for message in item["messages"]:
        # Look for the specific phrases in the content
        if "Here is the Markdown" in message["content"] or "Here is the new markdown" in message["content"]:
            # Extract the HTML content
            html_content = message["content"]
            # Convert the HTML to Markdown
            markdown_content = convert_to_md(html_content)
            # Replace the original content with the new Markdown content
            message["content"] = markdown_content

# Convert the modified list back to a JSON string
modified_json_str = json.dumps(data, indent=2)

# Write the modified JSON string to the output file
with open(output_file_path, 'w') as output_file:
    output_file.write(modified_json_str)

print(f"The modified content has been written to '{output_file_path}'")