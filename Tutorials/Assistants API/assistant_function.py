import os
from openai import OpenAI
#from client import openai_client
from runners.function_calling.standard_run import std_run

client = OpenAI()

assistant = client.beta.assistants.create(
    instructions="You are a weather bot. Use the provided functions to answer questions.",
    model="gpt-3.5-turbo",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_max_temperature",
                "description": "Get the max temperature for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The country, e.g., Portugal, 1110600"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["Celsius", "Fahrenheit"],
                            "description": "The temperature unit to use. Infer this from the user's location."
                        }
                    },
                    "required": ["location", "unit"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_rain_probability",
                "description": "Get the probability of rain for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "location": {
                        "type": "string",
                        "description": "The country, e.g., Portugal, 1110600"
                    }
                    },
                    "required": ["location"]
                }
            }
        }
    ]
)



thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What's the max temperature for today in Portugal and the likelihood it'll rain?",
)

location_id = "1110600"  # Portugal´s ID

print(std_run(thread.id, assistant.id, client, location_id))