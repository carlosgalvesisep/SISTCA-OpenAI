from openai import OpenAI
from runner.run import std_run

client = OpenAI()

assistant = client.beta.assistants.create(
    instructions="You are a personal movie and series assistant. Use the provided functions and your knowledge to provide informations about movies and series.",
    model="gpt-3.5-turbo",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_cinema_info",
                "description": "Get the information for the top, number of choice from the user, movies/series from a specific genre/category. ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "description": "Type of media two give information about, movie or series",
                        },
                        "theme": {
                            "type": "string",
                            "description": "Information about the genre ou category of the type"
                        },
                        "quantity" : {
                            "type" : "number",
                            "description": "The quantity of movies/series"
                        }
                    },
                    "required": ["type","theme","quantity"]
                }
            }
        }
    ]
)

thread = client.beta.threads.create()

query = input("Ask: ")

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=query,
)

print(std_run(thread.id, assistant.id, client))