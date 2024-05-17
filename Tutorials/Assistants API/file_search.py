from openai import OpenAI
 
# choose the model
GPT_MODEL = "gpt-3.5-turbo"
 
# initialize the client
client = OpenAI()
 
# create an assistant with the instructions about his job
assistant = client.beta.assistants.create(
  name="Music Information Assistant",
  instructions="You are an expert music analyst. Use you knowledge base to answer questions about music artist and their work.",
  model=GPT_MODEL,
  tools=[{"type": "file_search"}],
)

# create a vector store to store your information
vector_store = client.beta.vector_stores.create(name="Music Information")

# add files, it is possible to add multiple
file_paths = ["file_search_information.txt"]
file_streams = [open(path, "rb") for path in file_paths]
 
# upload the files and add them to the vector store
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)

# update the assistant with the vector store created
assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

# upload the user provided file to OpenAI
message_file = client.files.create(
  file=open("file_search_information.txt", "rb"), purpose="assistants"
)
 

# what do you want to ask/tell about the files
message_input = "How many artists do you know about, and what are their albums?"
 
# create a thread and attach the file to the message
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
 


# run the thread until it's in a terminal state.
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

# retrieve the necessary information 
messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

# get the answer and print it
message_content = messages[0].content[0].text

print(message_content.value)
