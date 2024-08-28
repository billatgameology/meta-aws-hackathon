import logging
from flask import jsonify
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)

def describe_image_from_base64(base64_image):
    if not base64_image:
        return jsonify({'error': 'No base64 image provided'}), 400

    chat = ChatBedrock(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={"temperature": 0.1},
    )

    messages = [
        HumanMessage(
            content=[
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": base64_image,
                    },
                },
                {"type": "text", "text": "Describe what is in this image."},
            ]
        )
    ]

    try:
        response = chat.invoke(messages)
        image_description = response.content if hasattr(response, 'content') else str(response)
        return jsonify({'image_description': image_description}), 200
    except Exception as e:
        logger.error(f"Error during image description: {str(e)}")
        return jsonify({'error': str(e)}), 500