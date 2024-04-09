import os
from dotenv import load_dotenv
import whisper

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

audio = "Tutorials/Whisper/audio.wav"

model = whisper.load_model("medium")

result = model.transcribe(audio)

print(result["text"])

