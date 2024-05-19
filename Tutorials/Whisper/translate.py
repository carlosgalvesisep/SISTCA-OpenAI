import os
from openai import OpenAI


client = OpenAI()

audio_file= open("audio.wav", "rb")

translation = client.audio.translations.create(
    model = "whisper-1", 
    file = audio_file,
    response_format="text"
)
print(translation)