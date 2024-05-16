import os
from openai import OpenAI
#from client import openai_client
from runners.standard_run import std_run
from runners.function_calling.streaming_run import streaming_run

client = OpenAI()

assistant = client.beta.assistants.create(
    instructions="You are a weather bot. Use the provided functions to answer questions.",
    model="gpt-3.5-turbo",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_weather_data",
                "description": "Get the current weather forecast for the specified location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City or region for which to get the weather forecast",
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    ]
)


thread = client.beta.threads.create()

#Define the location name
location_name = "Lisboa"

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"How is the weather today in {location_name}?",
)
print(message.content[0].text.value + "\n")

#print(std_run(thread.id, assistant.id, client))
print(streaming_run(thread.id, assistant.id, client))