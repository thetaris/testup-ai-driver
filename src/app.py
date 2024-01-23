from flask import Flask, jsonify, request, Response, redirect
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Server")

@app.route('/api/prompt/<deviceId>', methods=['POST'])
def process_prompt(deviceId):
    logger.info("Received prompt from device: " + deviceId)
    print(request.data)
    return { "result": "success" }

if __name__ == '__main__':
    port = int(os.getenv("PORT", "5000"))
    app.run(host='0.0.0.0', port=port)
