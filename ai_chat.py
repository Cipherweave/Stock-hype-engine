
"""This page connects to the Custome AI we created in OpenAI and allows us to chat with it"""


from openai import OpenAI
try: # Retrieve the API key from the api_key.txt file
    with open ('api_key.txt', 'r') as file:
        API_KEY = file.read().strip()
    client = OpenAI(api_key=API_KEY)
except Exception: # If the API key is not found, print an error message
    print("API key not found, AI features will not work")
    client = None
    API_KEY = None


assistant = client.beta.assistants.retrieve(assistant_id='asst_DtEcZIRhdDOCXEgJjbmLude5')

thread = client.beta.threads.create()

while True:
    user_input = input("You: ")
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_input
    )

    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    )


    # then, list the messages in the thread
    messages = client.beta.threads.messages.list( 
        thread_id = thread.id,
    ) 

    # Print the messages
    message = messages.data[0]
    # print(message.content)
    print(message.role + ": " + message.content[0].text.value)
