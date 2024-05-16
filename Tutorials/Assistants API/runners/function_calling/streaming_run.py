from typing_extensions import override
from openai import AssistantEventHandler
 
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
    
def streaming_run (thread_id, assistant_id, client):

    class EventHandler(AssistantEventHandler):
        @override
        def on_event(self, event):

            # Retrieve events that are denoted with 'requires_action'
            # since these will have our tool_calls
            
            if event.event == 'thread.run.requires_action':
                run_id = event.data.id  # Retrieve the run ID from the event data
                self.handle_requires_action(event.data, run_id)
    
        def handle_requires_action(self, data, run_id):
            tool_outputs = []
            
            for tool in data.required_action.submit_tool_outputs.tool_calls:
                if tool.function.name == "get_weather_data":
                    location_id = get_location_id(json.loads(tool.function.arguments)["location"])
                    forecast = get_weather_data(location_id)
                    tool_outputs.append({"tool_call_id": tool.id,
                                        "output": f"Rain probability: {forecast['precipitaProb']}, Max temperature: {forecast['tMin']}, Min temperature: {forecast['tMax']}"
                                        })
            
            # Submit all tool_outputs at the same time
            self.submit_tool_outputs(tool_outputs, run_id)
    
        def submit_tool_outputs(self, tool_outputs, run_id):
            # Use the submit_tool_outputs_stream helper
            with client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=EventHandler(),
            ) as stream:
                for text in stream.text_deltas:
                    print(text, end="", flush=True)
                print()
    
    
    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        event_handler=EventHandler()
    ) as stream:
        stream.until_done()