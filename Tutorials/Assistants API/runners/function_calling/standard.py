import os
#from dotenv import load_dotenv
from openai import OpenAI

#load_dotenv()

#api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(#api_key=api_key
                )

def standard (thread_id, assistant_id):
    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id,
    )
    
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        print(messages)
    else:
        print(run.status)
    
    # Define the list to store tool outputs
    tool_outputs = []
    
    # Loop through each tool in the required action section
    for tool in run.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == "get_current_temperature":
            tool_outputs.append({
            "tool_call_id": tool.id,
            "output": "57"
            })
        elif tool.function.name == "get_rain_probability":
            tool_outputs.append({
            "tool_call_id": tool.id,
            "output": "0.06"
            })
    
    # Submit all tool outputs at once after collecting them in a list
    if tool_outputs:
        try:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=tool_outputs
            )
            print("Tool outputs submitted successfully.")
        except Exception as e:
            print("Failed to submit tool outputs:", e)
    else:
        print("No tool outputs to submit.")
    
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        print(messages)
    else:
        print(run.status)