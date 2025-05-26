import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


def generate_response(user_input, system_prompt):
    load_dotenv('/home/msensis/Documents/Hackathon/AI_Agent/.env')
    azure_key = os.getenv('AZURE_API_KEY')
    endpoint = "https://iee2019082-diplo-resource.services.ai.azure.com/models"
    model_name = "DeepSeek-R1"

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(azure_key),
        api_version="2024-05-01-preview"
    )

    response = client.complete(
        messages=[
            SystemMessage(content=system_prompt),
            UserMessage(content=user_input),
        ],
        max_tokens=100,
        temperature=0.5,
        top_p=0.1,
        presence_penalty=0.0,
        frequency_penalty=0.2,
        model=model_name
    )

    return response.choices[0].message.content.strip()


if __name__ == '__main__':
    print(generate_response("What is the moon?", "You are helpful"))
