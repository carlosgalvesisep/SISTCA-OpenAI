import os
from openai import OpenAI
from runners.standard_run import std_run
 

client = OpenAI()
 
assistant = client.beta.assistants.create(
  name="Music Information Assistant",
  instructions="You are an expert music analyst. Use you knowledge base to answer questions about music artist and their work.",
  model=os.getenv("MODEL"),
  tools=[{"type": "file_search"}],
)

vector_store = client.beta.vector_stores.create(name="Music Information")

file_paths = ["resources/file_search_information.txt"]
file_streams = [open(path, "rb") for path in file_paths]
 
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)

assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

message_file = client.files.create(
  file=open("resources/file_search_information.txt", "rb"), purpose="assistants"
)

message_input = "How many artists do you know about, and what are their albums?"
 
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": message_input,
      "attachments": [
        { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
      ],
    }
  ]
)
 
print(std_run(thread.id, assistant.id, client))