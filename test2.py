from openai import OpenAI
client = OpenAI(api_key='sk-proj-dQP4LNfKld1ElhklGMCMT3BlbkFJY1zOL3dwtuKFX5fsxJRt')


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
