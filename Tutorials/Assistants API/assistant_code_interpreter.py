import os
from openai import OpenAI


from runners.standard_run import std_run
from runners.streaming_run import streaming_run


client = OpenAI()


# Upload a file with an "assistants" purpose
file = client.files.create(
    file=open("SISTCA-OpenAI\Tutorials\Assistants API\customers-100.csv", "rb"),
    purpose='assistants'
)

assistant = client.beta.assistants.create(
    instructions="You are a personal math tutor. When asked a math question, write and run code to answer the question.",
    model="gpt-3.5-turbo",
    tools=[{"type": "code_interpreter"}],
    file_ids=[file.id]
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is the customer ID for Sheryl Baxter?"
)


print(message.content[0].text.value)

#print(std_run(thread.id, assistant.id))
print(streaming_run(thread.id, assistant.id))