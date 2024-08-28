import boto3
import json
import base64

s3 = boto3.client('s3')
bedrock_runtime = boto3.client(service_name="bedrock-runtime")

SDXL_MODEL_ID = 'stability.stable-diffusion-xl-v1'

def lambda_handler(event, context):
    # Get the text prompt from the API request body
    body = json.loads(event['body'])
    prompt = body.get('prompt')

    # Prepare the request payload for the SDXL 1.0 model
    payload = {
        'text_prompts': [{'text': prompt}],
        'seed': 42,  # You can use a different seed value
        'style_preset': 'photographic'  # You can use a different style preset
    }

    # Invoke the SDXL 1.0 model
    response = bedrock_runtime.invoke_model(
        modelId=SDXL_MODEL_ID,
        body=json.dumps(payload)
    )

    # Handle the response from the model
    response_body = json.loads(response['body'].read().decode('utf-8'))
    base64_image_data = response_body["artifacts"][0].get("base64")

    # Upload the generated image to Amazon S3
    key = f'generated-image.png'

    return {
        'statusCode': 200,
        'body': json.dumps({'data': base64_image_data, 'name': key}),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }


if __name__ == '__main__':
    # Test case 1: Valid prompt
    event = {
        'body': json.dumps({'prompt': 'A beautiful sunset over the ocean'})
    }
    context = {}
    response = lambda_handler(event, context)
    print(f"Test case 1 response: {response}")

    # Save the image from the response body
    response_body = json.loads(response['body'])
    base64_image_data = response_body['data']
    image_bytes = base64.b64decode(base64_image_data)

    with open('generated_image.png', 'wb') as image_file:
        image_file.write(image_bytes)
    print("Image saved as 'generated_image.png'")