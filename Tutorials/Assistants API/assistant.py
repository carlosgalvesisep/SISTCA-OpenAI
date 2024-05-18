import os
from openai import OpenAI
from runners.standard_run import std_run
from runners.streaming_run import streaming_run


client = OpenAI()
assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  model=os.getenv("MODEL"),
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

print(message.content[0].text.value + "\n")

print(std_run(thread.id, assistant.id, client))
#print(streaming_run(thread.id, assistant.id, client))