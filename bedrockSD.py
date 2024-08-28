import json
import boto3



def generate_image_from_description(prompt):
    s3 = boto3.client('s3')
    bedrock_runtime = boto3.client(service_name="bedrock-runtime")

    SDXL_MODEL_ID = 'stability.stable-diffusion-xl-v1'

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

    # # Handle the response from the model
    # print(response.keys())
    # image_data = response['body'].read().decode('utf-8')
    # # Upload the generated image to Amazon S3
    # key = f'generated-image.png'

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps({'data':image_data,'name':key}),
    #     'headers': {
    #         'Access-Control-Allow-Origin': '*'
    #     }
    # }
    
    

 # Handle the response from the model
    response_body = response['body'].read().decode('utf-8')
    response_data = json.loads(response_body)

    # Extract the base64 string of the generated image
    base64_image_data = response_data['artifacts'][0]['base64']

    return base64_image_data