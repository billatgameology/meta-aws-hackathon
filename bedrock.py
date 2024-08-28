from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

def translate_to_french(text):
    chat = ChatBedrock(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={"temperature": 0.1},
    )

    messages = [
        HumanMessage(
            content=f"Translate this sentence from English to French: {text}"
        )
    ]

    response = chat.invoke(messages)
    # Extract the content field from the response
    translation = response.content if hasattr(response, 'content') else str(response)
    return translation

if __name__ == "__main__":
    text = "Hello, how are you?"
    translation = translate_to_french(text)
    print(translation)