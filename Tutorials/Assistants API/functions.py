import requests

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