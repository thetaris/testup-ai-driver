from flask import Flask, jsonify, request, Response, redirect
import logging
import os
from dom_analyzer import DomAnalyzer

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Server")

dom_analyzer = DomAnalyzer()
@app.route('/api/prompt/<deviceId>', methods=['POST'])
def process_prompt(deviceId):
    logger.info("Received prompt from device: " + deviceId)
    data = request.get_json()

    # Extract 'html_doc' and 'user_prompt' from the JSON payload
    html_doc = data.get('html_doc')
    user_prompt = data.get('user_prompt')
    analysis_result = dom_analyzer.analyze(deviceId, user_prompt, html_doc)
    print(analysis_result)

    return jsonify(analysis_result)

if __name__ == '__main__':
    port = int(os.getenv("PORT", "5000"))
    app.run(host='0.0.0.0', port=port)
