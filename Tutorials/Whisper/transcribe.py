import os
from openai import OpenAI


client = OpenAI()

audio_file = open("audio.wav", "rb")

transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="verbose_json"
)
print(f"Detected language: {transcription.language}")
print(transcription.text)