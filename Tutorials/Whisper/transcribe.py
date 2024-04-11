import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


audio_file = open("Tutorials/Whisper/audio.wav", "rb")

transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
<<<<<<< HEAD
    #response_format="text"
)
    
=======
    response_format="verbose_json"
)
print(f"Detected language: {transcription.language}")
>>>>>>> 3af14e3 (completed transcribe and translate functionalites)
print(transcription.text)