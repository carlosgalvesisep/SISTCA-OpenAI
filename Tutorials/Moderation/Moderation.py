import os

from openai import OpenAI
client = OpenAI()

response = client.moderations.create(input="I hate Chinese and black people ")

output = response.results[0]

print(output)

