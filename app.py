import os
import logging
from flask import Flask, request, jsonify
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
#from flaskcors import CORS

app = Flask(__name__)

#CORS(app, origins=["https://localhost:5173"])

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
    description = describe_image_from_base64(base64_image)
    return jsonify({"image_description": description}), 200


from bedrock import lambda_handler  # Import the lambda_handler function from bedrock.py
import json
import base64

@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.get_json()
    base64_image = data.get('base64_image')
    prompt = str(describe_image_from_base64(base64_image))
    sanitized_prompt = sanitize_prompt(prompt)
    
    print(sanitized_prompt)
    
    event = {
    'body': json.dumps({'prompt': sanitized_prompt})
}
    context = {}
    response = lambda_handler(event, context)

    # Save the image from the response body
    response_body = json.loads(response['body'])
    base64_image_data = response_body['data']

    return jsonify({
        "base64_image": base64_image_data,
        "prompt": sanitized_prompt
    }), 200

def sanitize_prompt(prompt):
    # Remove leading and trailing whitespace
    prompt = prompt.strip()
    
    # Replace newlines and tabs with spaces
    prompt = prompt.replace('\n', ' ').replace('\t', ' ')
    
    # Remove any double quotes to prevent JSON issues
    prompt = prompt.replace('"', '')
    
    # Optionally, limit the length of the prompt
    max_length = 500  # You can adjust this value
    if len(prompt) > max_length:
        prompt = prompt[:max_length] + '...'
    
    return prompt

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  
    app.run(debug=True, host='0.0.0.0', port=port)