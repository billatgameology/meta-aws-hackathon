import os
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'Hello, World!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  
    app.run(debug=True, host='0.0.0.0', port=port)