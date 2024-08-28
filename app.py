import os
from flask import Flask, request, jsonify
from bedrocktest import get_style_options


app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'Hello, World!'

# @app.route('/styles', methods=['POST'])
# def styles():
#     data = request.json
#     customer_input = data.get('customer_input', '')
#     styles = get_style_options(customer_input)
#     return jsonify(styles)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  
    app.run(debug=True, host='0.0.0.0', port=port)