# from llama_cpp import Llama

# # Specify the path to your .gguf file
# model_path = "C:\ali\VS Coding\AIs\OrengutengLlama-3-8B-Lexi-Uncensored\Lexi-Llama-3-8B-Uncensored_F16.gguf"

# # Load the model
# llm = Llama(model_path=model_path)

# # Generate text
# prompt = "Once upon a time"
# output = llm.llama_n_batch(prompt, max_tokens=100)  # Use the correct function name

# print(output['choices'][0]['text'])


# sk-proj-dQP4LNfKld1ElhklGMCMT3BlbkFJY1zOL3dwtuKFX5fsxJRt

from openai import OpenAI

# First, create an instance of the OpenAI class
client = OpenAI(api_key="sk-proj-dQP4LNfKld1ElhklGMCMT3BlbkFJY1zOL3dwtuKFX5fsxJRt")

# then, create an assistant
assistant = client.beta.assistants.create(
    name = "My homie",
    instructions = "act like a homie and a gym bro. be cool with me",
    tools = [{"type": "code_interpreter"}],
    model = "gpt-3.5-turbo",
)

# then, create a thread. thread is for conversation between user and assistant
thread = client.beta.threads.create()
# print(thread)   

# then, create a message in the thread. messages are the actual conversation
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = "hey, what's up?"
)
# print(message)

# then, create a run. run is for running the assistant
run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id,
)


# then, retrieve the run meaning get the response from the assistant
run = client.beta.threads.runs.retrieve(
    thread_id = thread.id,
    run_id = run.id,    
)

# then, list the messages in the thread
messages = client.beta.threads.messages.list( 
    thread_id = thread.id,
) 

# Print the messages
for message in reversed(messages.data):
    print(message.content)
    print(message.role + ": " + message.content[1].text.value)

