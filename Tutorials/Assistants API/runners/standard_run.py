import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def std_run (thread_id, assistant_id):
    run = client.beta.threads.runs.create_and_poll(
        thread_id = thread_id,
        assistant_id = assistant_id,
        instructions = "Please address the user as Jane Doe. The user has a premium account."
    )   

    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id = thread_id
        )
        return(messages.data[0].content[0].text.value)
    else:
        return(run.status)
