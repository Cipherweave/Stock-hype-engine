from llama_cpp import Llama

# Specify the path to your .gguf file
model_path = "C:\ali\VS Coding\AIs\OrengutengLlama-3-8B-Lexi-Uncensored\Lexi-Llama-3-8B-Uncensored_F16.gguf"

# Load the model
llm = Llama(model_path=model_path)

# Generate text
prompt = "Once upon a time"
output = llm.llama_n_batch(prompt, max_tokens=100)  # Use the correct function name

print(output['choices'][0]['text'])