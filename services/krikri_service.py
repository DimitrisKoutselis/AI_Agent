from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda"

model = AutoModelForCausalLM.from_pretrained("ilsp/Llama-Krikri-8B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("ilsp/Llama-Krikri-8B-Instruct")

model.to(device)

system_prompt = "Είσαι το Κρικρί, ένα εξαιρετικά ανεπτυγμένο μοντέλο Τεχνητής Νοημοσύνης για τα ελληνικα και εκπαιδεύτηκες από το ΙΕΛ του Ε.Κ. \"Αθηνά\"."
user_prompt = "Σε τι διαφέρει ένα κρικρί από ένα λάμα;"

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]
prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
input_prompt = tokenizer(prompt, return_tensors='pt').to(device)
outputs = model.generate(input_prompt['input_ids'], max_new_tokens=256, do_sample=True)

print(tokenizer.batch_decode(outputs)[0])
