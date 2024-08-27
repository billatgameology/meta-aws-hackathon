import os
from flask import Flask
import json
import os
import sys
import boto3
import botocore

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'Hello, World!'

# @app.route('/test', methods=['GET'])
# def test():
#     module_path = ".."
#     sys.path.append(os.path.abspath(module_path))
#     from utils import bedrock

#     bedrock_runtime = bedrock.get_bedrock_client(
#         assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
#         region=os.environ.get("AWS_DEFAULT_REGION", None))

#     model_parameter = {"temperature": 0.0, "top_p": .5, "max_tokens_to_sample": 2000}

#     # If you'd like to try your own prompt, edit this parameter!
#     customer_input = "I am a male consultant in my 30s traveling to New York next week. What kind of outfit should I wear on my first day in the office? "

#     # first fetch possible styles and give options to customer
#     prompt = """

#     Human: list different style options for:
#     """ + customer_input + """ 

#     Assistant:"""
#     body = json.dumps({"prompt": prompt, "max_tokens_to_sample": 500})
#     modelId = "anthropic.claude-v2"  # change this to use a different version from the model provider
#     accept = "application/json"
#     contentType = "application/json"
#     claudeResponse = ""

#     response = bedrock_runtime.invoke_model(
#         body=body, modelId=modelId, accept=accept, contentType=contentType
#     )
#     response_body = json.loads(response.get("body").read())
#     styles_response = response_body.get("completion")
#     print(styles_response)


#     # Prepare input for fetching images for each of style
#     styles = [s.strip() for s in (list(filter(None, styles_response.splitlines()))[1:-1])]
#     print(*styles, sep='\n')
#     return 'Hello, Test!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  
    app.run(debug=True, host='0.0.0.0', port=port)