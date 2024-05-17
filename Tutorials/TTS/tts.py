from pathlib import Path
from openai import OpenAI

# create an instance of OpenAI, the default construct gets the token from environment variables
client = OpenAI()


# create a path and a format to save the audio file
speech_file_path = Path(f"tts_audio.mp3")

# send the api request, change the voice to one of the options available and the input to anything you want
response = client.audio.speech.create(
  model="tts-1",
  voice="shimmer",
  input="Hey, I'm a student in Lincenciatura de Engenharia de Telecomunicações e Informática in Instituto Superior de Engenharia do Porto, and I'm doing a tutorial on how to use open-a.i in my projects!"
)

# saves the audio file to specified path
response.write_to_file(speech_file_path)


