import os
from dotenv import load_dotenv
from client import openai_client
from runners.function_calling.standard_run import std_run
from runners.function_calling.streaming_run import streaming_run

load_dotenv()

client = openai_client.create()

assistant = client.beta.assistants.create(
    instructions="You are a weather bot. Use the provided functions to answer questions.",
    model=os.getenv("MODEL"),
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_current_temperature",
                "description": "Get the current temperature for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g., San Francisco, CA"
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
                        "description": "The city and state, e.g., San Francisco, CA"
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
    content="What's the weather in San Francisco today and the likelihood it'll rain?",
)

print(std_run(thread.id, assistant.id, client))
#print(streaming_run(thread.id, assistant.id, client))