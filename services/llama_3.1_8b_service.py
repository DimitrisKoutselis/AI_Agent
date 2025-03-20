import requests
import json
from typing import List, Dict, Any
from utils.weather import current_weather


model_name = "llama3.1"
api_url = "http://localhost:11434/api/generate"

def init_model():
    print(f"Using ollama with model: {model_name}")

def get_current_weather(location: str, unit: str = "celsius") -> str:
    return f"The current weather in {location} is 22°{'C' if unit == 'celsius' else 'F'}"

def generate_response(messages: List[Dict[str, str]], max_tokens: int = 256) -> str:
    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "max_tokens": max_tokens
    }
    
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        return response.json()['response']
    else:
        raise Exception(f"Error from ollama API: {response.text}")

def parse_function_call(response: str) -> Dict[str, Any]:
    if "Function call:" not in response:
        return {}
    
    function_call = response.split("Function call:")[1].strip()
    function_name = function_call.split("(")[0].strip()
    args = function_call.split("(")[1].split(")")[0].split(",")
    args = [arg.strip().strip("'\"") for arg in args]
    
    return {"name": function_name, "arguments": args}

def process_query(query: str) -> str:
    messages = [
        {"role": "system", "content": "You are an AI assistant capable of answering questions and calling functions when necessary. Available functions: get_current_weather(location: str, unit: str = 'celsius')"},
        {"role": "user", "content": query}
    ]
    response = generate_response(messages)
    
    function_call = parse_function_call(response)
    if function_call:
        if function_call["name"] == "get_current_weather":
            weather_info = get_current_weather(*function_call["arguments"])
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "function", "name": "get_current_weather", "content": weather_info})
            final_response = generate_response(messages)
            return final_response
    
    return response

if __name__ == "__main__":
    init_model()
    
    print("Regular query:")
    print(process_query("Tell me a joke about pirates"))
    
    print("\nFunction calling query:")
    print(process_query("What's the weather like in London?"))
    
    print(f"\nUsing model: {model_name}")