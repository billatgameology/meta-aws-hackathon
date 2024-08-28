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


    return base64_image_data