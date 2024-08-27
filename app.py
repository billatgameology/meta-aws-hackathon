import os
from flask import Flask

app = Flask(__name__)

@app.route('/ping')
def ping():
    return "Hello, World!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(debug=True, host='0.0.0.0', port=port)