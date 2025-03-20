import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import ast
import gc
import re

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from utils.weather import current_weather, forecast_weather
from utils.news import get_top_news, get_news_by_keywords, format_news_response

model_id = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_id)

def get_current_weather(location: str, format: str):
    """
    Get the current weather.

    Args:
        location: The city and state, e.g. San Francisco, CA.
        format: The temperature unit to use. Infer this from the user's location. (choices: ["celsius", "fahrenheit"])
    """
    return current_weather(location, format)


def get_forecast_weather(location: str, days: int, format: str):
    """
    Get the weather forecast for the next 'days' days.

    Args:
        location: The city and state, e.g. San Francisco, CA.
        days: The number of days to forecast.
        format: The temperature unit to use. Infer this from the user's location. (choices: ["celsius", "fahrenheit"])
    """
    return forecast_weather(location, days, format)


def get_top_articles(country: str = "us", category: str = "general"):
    """
    Get the top articles for a given country and category.

    Args:
        country: The country to get articles for. (choices: ["us", "gb", "in", "au", "ca", "fr", "de", "it", "es", "br"])
        category: The category to get articles for. (choices: ["business", "entertainment", "general", "health", "science", "sports", "technology"])
    """
    return get_top_news(country, category)


def get_articles_by_keywords(keywords: str, language: str = "en"):
    """
    Get the articles that are about the given keywords. Get the news about the given keywords.

    Args:
        keywords: The keywords to search for.
        language: The language of the articles. (choices: ["en", "es", "fr", "de", "it", "ru", "zh", "pt", "ar", "nl"])
    """
    return get_news_by_keywords(keywords, language)


def ask_model(user_input: str):
    conversation = [
        {"role": "system", "content": "You are an AI assistant capable of answering questions and calling functions when necessary. Available functions: get_current_weather(location: str, format: str = 'celsius'), get_forecast_weather(location: str, days: int, format: str = 'celsius'), get_top_articles(country: str = 'us', category: str = 'general'), get_articles_by_keywords(keywords: str, language: str = 'en')"},
        {"role": "user", "content": user_input}
    ]
    tools = [get_current_weather, get_forecast_weather, get_top_articles, get_articles_by_keywords]

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
        try:
            # Ensure the string is a valid JSON-like structure
            last_array = ast.literal_eval(arrays[-1])
            if isinstance(last_array, list) and last_array:
                last_dict = last_array[0]
                if isinstance(last_dict, dict) and last_dict.get('name') == 'get_current_weather':
                    location = last_dict['arguments']['location']
                    format = last_dict['arguments'].get('format', 'celsius')
                    del model
                    gc.collect()
                    torch.cuda.empty_cache()
                    return get_current_weather(location, format)
                elif isinstance(last_dict, dict) and last_dict.get('name') == 'get_forecast_weather':
                    location = last_dict['arguments']['location']
                    days = last_dict['arguments']['days']
                    format = last_dict['arguments'].get('format', 'celsius')
                    del model
                    gc.collect()
                    torch.cuda.empty_cache()
                    return get_forecast_weather(location, days, format)
                elif isinstance(last_dict, dict) and last_dict.get('name') == 'get_top_articles':
                    country = last_dict.get('arguments', {}).get('country', 'us')
                    category = last_dict.get('arguments', {}).get('category', 'general')
                    del model
                    gc.collect()
                    torch.cuda.empty_cache()
                    return get_top_articles(country, category)
                elif isinstance(last_dict, dict) and last_dict.get('name') == 'get_articles_by_keywords':
                    keywords = last_dict.get('arguments', {}).get('keywords')
                    language = last_dict.get('arguments', {}).get('language', 'en')
                    del model
                    gc.collect()
                    torch.cuda.empty_cache()
                    if not keywords:
                        return "Please provide keywords."
                    return get_articles_by_keywords(keywords, language)
        except (SyntaxError, ValueError) as e:
            print("Error parsing the model's output:", e)
            return "Error: Unable to parse the model's response."
    else:
        del model
        print("No array found in the response.")
        return "No valid function call found in the response."

if __name__ == '__main__':
    answer = ask_model("Give me articles with keywords: \"climate change\"")
    try:
        print(format_news_response(answer))
    except Exception as e:
        print(answer)
