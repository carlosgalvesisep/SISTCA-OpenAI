from openai import OpenAI
from runner.run import std_run

client = OpenAI()

def get_cinema_info(typeFilter, genreFilter, quantityFilter):
    try:
        assistant = client.beta.assistants.create(
            instructions="You are a personal film, tv show and book assistant. Use the provided functions and your knowledge to provide informations about movies and series.",
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
    except Exception as e:
        print("Error creating assistant:", e)
        return None

    if assistant is None:
        print("Assistant creation failed.")
        return None

    thread = client.beta.threads.create()

    query = f"get_cinema_info(type='{typeFilter}', theme='{genreFilter}', quantity={quantityFilter})"

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=query,
    )

    response = std_run(thread.id, assistant.id, client)
    
    return response