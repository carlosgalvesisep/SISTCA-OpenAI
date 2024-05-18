import os
from openai import OpenAI


from runners.standard_run import std_run
client = OpenAI()

assistant = client.beta.assistants.create(
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    model="gpt-3.5-turbo",
    tools=[
        {
            "type": "function",
            "function":{
                "name": "Sum",
                "description": "Function to add 2 numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "First number"
                        },
                        "b": {
                            "type": "number",
                            "description": "Second number"
                        }
                    },
                    "required": ["a", "b"]
                }
            }
        }
    ]
)

thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Add the values [2,2]",
)


print(message.content[0].text.value)

print(std_run(thread.id, assistant.id))

