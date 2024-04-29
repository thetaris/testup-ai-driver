from flask import Flask, jsonify, request, Response, redirect
import logging
import os
from action_processor import DomAnalyzer

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Server")


dom_analyzer = DomAnalyzer()
@app.route('/api/v1/prompt/<session_id>', methods=['POST'])
def process_prompt(session_id):
    data = request.get_json()

    # Extract 'html_doc' and 'user_prompt' from the JSON payload
    html_doc = data.get('html_doc')
    user_prompt = data.get('user_prompt')
    actions_executed = data.get("actions_executed")
    variable_map = data.get("variables_map")
    duplicate = data.get("duplicate", False)  # Defaulting to False if not provided
    valid = data.get("valid", False)  # Defaulting to False if not provided
    last_action = data.get("last_action")
    variable_map_str = dom_analyzer.variableMap_to_string(variable_map)
    analysis_result = dom_analyzer.get_actions(session_id, user_prompt, html_doc, actions_executed, variable_map_str, duplicate, valid, last_action)
    if check_action_status(analysis_result):
        dom_analyzer.print_prompt(session_id)
        logging.info(f"Returning: {analysis_result}")

    return jsonify(analysis_result)

def check_action_status(data):
    # Check if 'steps' key exists and is a list
    if 'steps' in data and isinstance(data['steps'], list):
        # Iterate through each step in the 'steps' list
        for step in data['steps']:
            # Use .get() to safely get 'action', defaulting to None if not found
            action_value = step.get('action', None)

            # Check if action_value is "error" or "finish"
            if action_value in ['error', 'finish']:
                return True
    # Return False if no action is "error" or "finish", or if 'steps' is not as expected
    return False


if __name__ == '__main__':
    port = int(os.getenv("PORT", "5000"))
    app.run(host='0.0.0.0', port=port)
