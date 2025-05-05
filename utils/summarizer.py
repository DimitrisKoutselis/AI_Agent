import torch
from transformers import BartForConditionalGeneration, BartTokenizer


def summarize_text(text, max_length=150, min_length=40):
    """
    Summarizes the given text using BART Large CNN model.
    
    Args:
        text (str): The text to summarize
        max_length (int, optional): Maximum length of the summary. Defaults to 150.
        min_length (int, optional): Minimum length of the summary. Defaults to 40.
    
    Returns:
        str: The generated summary
    """
    model_name = "facebook/bart-large-cnn"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True).to(device)
    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        min_length=min_length,
        max_length=max_length,
        early_stopping=True
    )
    
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary

if __name__ == "__main__":
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to intelligence displayed by animals including humans. 
    AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and 
    takes actions that maximize its chance of achieving its goals. The term "artificial intelligence" had previously been used to describe 
    machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". 
    This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, 
    which does not limit how intelligence can be articulated.
    """
    
    summary = summarize_text(sample_text)
    print(f"Summary: {summary}")
