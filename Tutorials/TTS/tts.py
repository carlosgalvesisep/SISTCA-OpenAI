from pathlib import Path
from openai import OpenAI

# create an instance of OpenAI, the default construct gets the token from environment variables
# use client = OpenAI(api_key = «your_api_token») if you want to specific a token
client = OpenAI()


### steps needed to generate a random name for the file; this step is not necessarily required; it was only made to facilitate testing
import random

animal_names =  [
    "Bunny",
    "Kitten",
    "Puppy",
    "Panda",
    "Koala",
    "Otter",
    "Fawn",
    "Chipmunk",
    "Hedgehog",
    "Lamb"
]
first_name = random.choice(animal_names)
number = random.randint(1, 9999)

file_name = f"{first_name}{number}" 
### 

# create a path and a format to save the audio file
speech_file_path = Path(__file__).parent / f"{file_name}.mp3"

# send the api request, change the voice to one of the options available and the input to anything you want
response = client.audio.speech.create(
  model="tts-1",
  voice="shimmer",
  input="Hey, I'm a student in Lincenciatura de Engenharia de Telecomunicações e Informática in Instituto Superior de Engenharia do Porto, and I'm doing a tutorial in how to use open-a-i in my projects!"
)

# saves the audio file to specified path
response.stream_to_file(speech_file_path)

print(f"Audio saved under the name {file_name}, {speech_file_path}")


