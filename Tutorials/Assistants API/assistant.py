import os
#from dotenv import load_dotenv
from openai import OpenAI
from runners.standard_run import std_run
from runners.streaming_run import streaming_run

#load_dotenv()

#api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(#api_key=api_key
                )
  
assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  #tools=[{"type": "code_interpreter"}],
  model="gpt-3.5-turbo",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

print(message.content[0].text.value)

print(std_run(thread.id, assistant.id))
#print(streaming_run(thread.id, assistant.id))