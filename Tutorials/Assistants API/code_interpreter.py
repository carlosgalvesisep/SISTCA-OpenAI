import os
from dotenv import load_dotenv
from client import openai_client
from runners.standard_run import std_run
from runners.streaming_run import streaming_run

load_dotenv()

client = openai_client.create()

file = client.files.create(
    file=open("Tutorials/Assistants API/customers-100.csv", "rb"),
    purpose='assistants'
)

assistant = client.beta.assistants.create(
    instructions="Your purpose is to analyze the provided documents and to provide answers based on them.",
    model=os.getenv("MODEL"),
    tools=[{"type": "code_interpreter"}],
    tool_resources={
        "code_interpreter": {
        "file_ids": [file.id]
        }
    }
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Create a graph of the number of customers per country."
)

print(message.content[0].text.value + "\n")

file_id = std_run(thread.id, assistant.id, client)
#file_id = streaming_run(thread.id, assistant.id, client)

image_data = client.files.content(file_id=file_id)
image_data_bytes = image_data.read()

image_name = "graph.png"

with open(image_name, "wb") as file:
    file.write(image_data_bytes)

print(f"Graph saved as {image_name}.")