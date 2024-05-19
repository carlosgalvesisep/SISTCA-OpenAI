import os
from openai import OpenAI


client = OpenAI()

response = client.chat.completions.create(
  model=os.getenv("MODEL"),
  messages=[
    {"role": "system", "content": "You are a helpful football assistants."},
    {"role": "user", "content": "Who won the Euro back in 2016?"},
    {"role": "assistants", "content": "Portugal won the World Cup in 2016."},
    {"role": "user", "content": "Where was it played, what was the score of the final and who scored in that game?"}
  ]
)

print(response.choices[0].message.content)