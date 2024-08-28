import os
import logging
from flask import Flask, request, jsonify
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

app = Flask(__name__)

# Configure logging based on environment variable
debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
log_level = os.getenv('LOG_LEVEL', 'DEBUG' if debug_mode else 'INFO').upper()

logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    return 'Hello, World!'

@app.route('/translate', methods=['POST'])
def translate():
    chat = ChatBedrock(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={"temperature": 0.1},
    )

    try:
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({"error": "No text provided"}), 400

        messages = [
            HumanMessage(
                content=f"Translate this sentence from English to French: {text}"
            )
        ]
        
        response = chat.invoke(messages)
        # Extract the content field from the response
        translation = response.content if hasattr(response, 'content') else str(response)    
        
        return jsonify({"translation": translation}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from util import describe_image_from_base64

@app.route('/describe_image', methods=['POST'])
def describe_image():
    data = request.get_json()
    base64_image = data.get('base64_image')
    return describe_image_from_base64(base64_image)

from bedrockSD import generate_image_from_description

@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.get_json()
    base64_image = data.get('base64_image')
    prompt = describe_image_from_base64(base64_image)
    
    if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

    base64_image_data = generate_image_from_description(prompt)
    
    if not base64_image_data:
            return jsonify({'error': 'Image generation failed'}), 500

    print(f"Response data: {base64_image_data}")
    
    return jsonify({'base64_image': base64_image_data}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  
    app.run(debug=True, host='0.0.0.0', port=port)