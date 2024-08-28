import os
from flask import Flask, request, jsonify
from bedrock import translate_to_french

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'Hello, World!'

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text', '')
    translation = translate_to_french(text)
    return jsonify({"translation": translation})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  
    app.run(debug=True, host='0.0.0.0', port=port)