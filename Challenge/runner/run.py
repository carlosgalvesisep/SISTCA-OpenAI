import json
from runner.functions import cinema

def std_run (thread_id, assistant_id, client):
    run = client.beta.threads.runs.create_and_poll(
        thread_id = thread_id,
        assistant_id = assistant_id,
        instructions = "Please return the information in a bullet list"
    )   

    if run.status == 'completed': 

        messages = client.beta.threads.messages.list(
            thread_id = thread_id
        )

        # This code acts upon the presence of image files when using code interpreter
        if messages.data[0].content[0].type == 'image_file':
            return(messages.data[0].content[0].image_file.file_id)
        else:
            print(run.status)

        return(messages.data[0].content[0].text.value)        
    
    # The following code is used to handle tool/function calls

    # Preparing tool outputs
    tool_outputs = []
    for tool in run.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == "get_cinema_info":
            information = cinema(json.loads(tool.function.arguments)["type"],json.loads(tool.function.arguments)["theme"],json.loads(tool.function.arguments)["quantity"])
            tool_outputs.append({"tool_call_id": tool.id,
                                "output": f" information JSON: {information}"
                                })

    # Submitting tool outputs and polling for completion status
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

    # Retrieving messages after tool output submission
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data[0].content[0].text.value
    else:
        print(run.status)