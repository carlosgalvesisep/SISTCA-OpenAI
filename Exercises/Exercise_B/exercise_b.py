from pathlib import Path
from openai import OpenAI


client = OpenAI()

# load the audio file
audio_input = open("Exercises/Exercise_B/audio.wav", "rb")


# transcribe contents and detect the input language
transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_input,
    response_format="verbose_json"
)

detected_language = transcription.language


# translate the transcription to another language using chatCompletions
output_language = "french"

translation = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"Translate the following text to {output_language}: {transcription.text}"}
    ]
)

translated_text = translation.choices[0].message.content


# output the translated audio file
translated_audio = client.audio.speech.create(
  model="tts-1",
  voice="shimmer",
  input=translated_text
)


output_file_path = Path(__file__).parent / f"translation.mp3"

translated_audio.write_to_file(output_file_path)


# test the output

print(f"Detected language: {detected_language} \n")
print(f"Transcribed text: {transcription.text} \n")

print(f"Translated text: {translated_text} \n")
print(f"Translated audio file saved to {output_file_path}")
