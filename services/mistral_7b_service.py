from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import List, Dict, Any
from utils.weather import get_current_weather

model_id = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = None
model = None

def init_model():
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="auto")
    print(f"Model {model_id} initialized successfully")

def generate_response(messages: List[Dict[str, str]], max_new_tokens: int = 256) -> str:
    global tokenizer, model
    if tokenizer is None or model is None:
        raise RuntimeError("Model not initialized. Call init_model() first.")
    
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

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
    
    print(f"\nUsing model: {model_id}")