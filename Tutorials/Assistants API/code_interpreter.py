import os
from dotenv import load_dotenv
from client import openai_client
from runners.standard_run import std_run
from runners.streaming_run import streaming_run

load_dotenv()

client = openai_client.create()

file = client.files.create(
    file=open("../customers-100.csv", "rb"),
    purpose='assistants'
)

assistant = client.beta.assistants.create(
    instructions="Your purpose is to analyze the provided documents and to provide answers based on them.",
    model=os.getenv("MODEL"),
    tools=[{"type": "code_interpreter"}],
    file_ids=[file.id]
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    #content="What is the customer ID for Sheryl Baxter?"
    content="Create a graph of the number of customers per country."
)

print(message.content[0].text.value + "\n")

run = client.beta.threads.runs.create_and_poll(
    thread_id = thread.id,
    assistant_id = assistant.id,
)   

if run.status == 'completed': 
    messages = client.beta.threads.messages.list(
        thread_id = thread.id
    )
    print(messages.data[0].content[0].type) 
    file_id = messages.data[0].content[0].image_file.file_id
    print(file_id)       

else:
    print(run.status)

image_data = client.files.content(file_id=file_id)
print(image_data)
image_data_bytes = image_data.read()

with open("graph.png", "wb") as file:
    file.write(image_data_bytes)


#print(std_run(thread.id, assistant.id, client))
#print(streaming_run(thread.id, assistant.id, client))