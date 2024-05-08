def std_run (thread_id, assistant_id, client):    

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        print(messages.data[0].content[0].text.value)
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
        print(messages.data[0].content[0].text.value)
    else:
        print(run.status)