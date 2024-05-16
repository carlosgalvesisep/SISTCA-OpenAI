import requests, json

def get_location_id(location_name):
    url = "https://api.ipma.pt/open-data/distrits-islands.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for location in data["data"]:
                if location["local"].lower() == location_name.lower():
                    return str(location["globalIdLocal"])
            return None  # Location not found
        else:
            print("Failed to fetch data:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None
    
def get_weather_data(location_id):
    url = f"https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{location_id}.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecast = data["data"][0]
            return forecast
        else:
            print("Failed to fetch data:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def std_run(thread_id, assistant_id, client):
    try:
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
            if tool.function.name == "get_weather_data":
                location_id = get_location_id(json.loads(tool.function.arguments)["location"])
                forecast = get_weather_data(location_id)
                tool_outputs.append({"tool_call_id": tool.id,
                                    "output": f"Rain probability: {forecast['precipitaProb']}, Max temperature: {forecast['tMin']}, Min temperature: {forecast['tMax']}"
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