import requests

def std_run(thread_id, assistant_id, client, location_id):
    # Fetching weather data from IPMA API
    url = f"https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{location_id}.json"
    try:
        response = requests.get(url)
        data = response.json()

        forecast = data['data'][0]
        max_temperature = forecast['tMax']
        rain_probability = forecast['precipitaProb']

        # Initiating a run with OpenAI assistant
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

        # Checking the completion status of the run
        if run.status == 'completed':
            # Retrieving messages from the thread
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            print(messages.data[0].content[0].text.value)
        else:
            print(run.status)

        # Preparing tool outputs (maximum temperature and rain probability)
        tool_outputs = []
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "get_max_temperature":
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": max_temperature
                })
            elif tool.function.name == "get_rain_probability":
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": rain_probability
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
            print(messages.data[0].content[0].text.value)
        else:
            print(run.status)

    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)

