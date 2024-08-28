from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage


chat = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0.1},
)

messages = [
    HumanMessage(
        content="Translate this sentence from English to French. I love programming."
    )
]

print(chat.invoke(messages))