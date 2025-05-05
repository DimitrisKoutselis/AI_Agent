from langdetect import detect
from transformers import AutoProcessor, SeamlessM4Tv2ForTextToText
import torch

def detect_and_translate(text):
    """
    Detects the language of the input text and translates it to English if it's not already in English.
    
    Args:
        text (str): The input text to detect and potentially translate
        
    Returns:
        tuple: (translated_text, language_code) where translated_text is the English translation
              if the original wasn't English, or the original text if it was already English,
              and language_code is the detected language code
    """
    try:
        language_code = detect(text)
        
        if language_code == 'en':
            return text, language_code
        
        model_id = "facebook/seamless-m4t-v2-large"
        processor = AutoProcessor.from_pretrained(model_id)
        model = SeamlessM4Tv2ForTextToText.from_pretrained(model_id)
        
        if torch.cuda.is_available():
            model = model.to('cuda')
        
        inputs = processor(text, return_tensors="pt")
        
        if torch.cuda.is_available():
            inputs = {key: value.to('cuda') for key, value in inputs.items()}
        
        outputs = model.generate(**inputs, tgt_lang="eng")
        translated_text = processor.decode(outputs[0], skip_special_tokens=True)
        
        return translated_text, language_code
    
    except Exception as e:
        print(f"Error in language detection or translation: {e}")
        return text, "en"


def translate_to_language(text, target_language_code):
    """
    Translates the input text to the specified target language.
    
    Args:
        text (str): The input text to translate
        target_language_code (str): The language code to translate to (e.g., 'fra' for French)
        
    Returns:
        str: The translated text in the target language
    """
    try:
        model_id = "facebook/seamless-m4t-v2-large"
        processor = AutoProcessor.from_pretrained(model_id)
        model = SeamlessM4Tv2ForTextToText.from_pretrained(model_id)
        
        if torch.cuda.is_available():
            model = model.to('cuda')
        
        inputs = processor(text, return_tensors="pt")
        
        if torch.cuda.is_available():
            inputs = {key: value.to('cuda') for key, value in inputs.items()}
        
        outputs = model.generate(**inputs, tgt_lang=target_language_code)
        translated_text = processor.decode(outputs[0], skip_special_tokens=True)
        
        return translated_text
    
    except Exception as e:
        print(f"Error in translation: {e}")
        return text


if __name__ == "__main__":
    sample_text = "Hello, how are you today?"
    translated, lang = detect_and_translate(sample_text)
    print(f"Detected language: {lang}")
    print(f"Translated text: {translated}")
    
    # Example of translating to French
    french_translation = translate_to_language(sample_text, "fra")
    print(f"French translation: {french_translation}")
