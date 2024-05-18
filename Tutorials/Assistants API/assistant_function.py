import os
from openai import OpenAI

from runners.streaming_run_FC import streaming
from runners.standard_run_FC import standard
client = OpenAI()

assistant = client.beta.assistants.create(
    instructions="You are a weather bot. Use the provided functions to answer questions.",
    model="gpt-3.5-turbo",
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


#print(streaming(thread.id, assistant.id))
print(standard(thread.id, assistant.id))