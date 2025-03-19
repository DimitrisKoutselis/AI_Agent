import ast
import gc
import re

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from utils.weather import current_weather, forecast_weather

model_id = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_id)

def get_current_weather(location: str, format: str):
    """
    Get the current weather

    Args:
        location: The city and state, e.g. San Francisco, CA
        format: The temperature unit to use. Infer this from the users location. (choices: ["celsius", "fahrenheit"])
    """
    return current_weather(location, format)


def get_forecast_weather(location: str, days: int, format: str):
    """
    Get the weather forecast for the next 'days' days

    Args:
        location: The city and state, e.g. San Francisco, CA
        days: The number of days to forecast
        format: The temperature unit to use. Infer this from the users location. (choices: ["celsius", "fahrenheit"])
    """
    return forecast_weather(location, days, format)


def ask_model(user_input: str):
    conversation = [
        {"role": "system", "content": "You are an AI assistant capable of answering questions and calling functions when necessary. Available functions: get_current_weather(location: str, format: str = 'celsius')"},
        {"role": "user", "content": user_input}
    ]
    tools = [get_current_weather, get_forecast_weather]

    inputs = tokenizer.apply_chat_template(
                conversation,
                tools=tools,
                add_generation_prompt=True,
                return_dict=True,
                return_tensors="pt",
    )

    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="auto")

    inputs.to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=1000)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    arrays = re.findall(r'\[.*?]', answer)

    if arrays:
        last_array = ast.literal_eval(arrays[-1])

        try:
            if isinstance(last_array, list) and last_array:
                last_dict = last_array[0]
                if isinstance(last_dict, dict) and last_dict.get('name') == 'get_current_weather':
                    location = last_dict['arguments']['location']
                    format = last_dict['arguments'].get('format', 'celsius')
                    del model
                    gc.collect()
                    torch.cuda.empty_cache()
                    return get_current_weather(location, format)
                elif isinstance(last_array, list) and last_dict.get('name') == 'get_forecast_weather':
                    location = last_dict['arguments']['location']
                    days = last_dict['arguments']['days']
                    format = last_dict['arguments'].get('format', 'celsius')
                    del model
                    gc.collect()
                    torch.cuda.empty_cache()
                    return get_forecast_weather(location, days, format)
        except Exception as e:
            del model
            gc.collect()
            torch.cuda.empty_cache()
            return arrays
    else:
        del model
        print("No array found in the response.")


if __name__ == '__main__':
    ask_model("What's will the weather be in thessaloniki the next 2 days?")
