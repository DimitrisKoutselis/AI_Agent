import requests
from dotenv import load_dotenv
import os

load_dotenv('/home/msensis/Documents/Hackathon/AI_Agent/.env')
api_key = os.getenv('AZURE_API_KEY')


def call_grok(user_input, system_prompt=None):
    url = "https://iee2019082-diplo-resource.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = []
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    
    messages.append({
        "role": "user",
        "content": user_input
    })

    data = {
        "messages": messages,
        "max_completion_tokens": 16000,
        "temperature": 1,
        "top_p": 1,
        "model": "grok-3-mini"
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    response_json = response.json()
    return response_json['choices'][0]['message']['content']


if __name__ == '__main__':
    result = call_grok("What is wikipedia", "You are helpful")
    print(result)