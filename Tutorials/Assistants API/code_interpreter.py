import os
from openai import OpenAI
from runners.standard_run import std_run
from runners.streaming_run import streaming_run


client = OpenAI()

file = client.files.create(
    file=open("resources/customers-100.csv", "rb"),
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
#file_id = streaming_run(thread.id, assistants.id, client)

image_data = client.files.content(file_id=file_id)
image_data_bytes = image_data.read()

image_name = "graph.png"

image_path = os.path.join("resources", image_name)

with open(image_path, "wb") as image_file:
    image_file.write(image_data_bytes)

print(f"Graph saved as {image_name}.")