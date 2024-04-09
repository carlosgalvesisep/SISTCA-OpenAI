import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

audio_file= open("Tutorials/Whisper/audio.wav", "rb")
translation = client.audio.translations.create(
    model = "whisper-1", 
    file = audio_file,
    response_format="verbose_json",
)

print(f"Detected language: {translation.language}")
print(f"Transcribed text: {translation.text}")