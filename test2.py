from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Orenguteng/Llama-3-8B-Lexi-Uncensored-GGUF"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Optionally, save the model and tokenizer to a directory
model.save_pretrained("C:\ali\VS Coding\AIs\OrengutengLlama-3-8B-Lexi-Uncensored")
tokenizer.save_pretrained("C:\ali\VS Coding\AIs\OrengutengLlama-3-8B-Lexi-Uncensored")