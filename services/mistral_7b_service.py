from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = None
model = None

def init_model():
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="auto")
    print("Model initialized successfully")

def get_current_weather(location: str, format: str):
    """
    Get the current weather

    Args:
        location: The city and state, e.g. San Francisco, CA
        format: The temperature unit to use. Infer this from the users location. (choices: ["celsius", "fahrenheit"])
    """
    # Implement actual weather fetching logic here
    return f"The current weather in {location} is 22°{format[0].upper()}"

def ask_model(user_input: str):
    global tokenizer, model

    if tokenizer is None or model is None:
        raise RuntimeError("Model not initialized. Call init_model() first.")

    system_prompt = """You are an AI assistant designed to help students with their studies and academic tasks. Your primary goal is to provide clear, concise, and accurate information to support their learning. You have access to various tools and functions that can assist you in providing the most relevant and up-to-date information. Always strive to explain concepts in a way that's easy for students to understand, and encourage critical thinking and problem-solving skills. If a student asks for help with homework, guide them through the process rather than simply providing answers. When appropriate, use the available functions to fetch real-time data or perform calculations to enhance your responses."""

    conversation = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    tools = [get_current_weather]

    inputs = tokenizer.apply_chat_template(
        conversation,
        tools=tools,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    )

    inputs = inputs.to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=1000)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage
if __name__ == "__main__":
    user_question = "What's the weather like in Paris? And can you explain how weather patterns affect climate?"
    response = ask_model(user_question)
    print(response)