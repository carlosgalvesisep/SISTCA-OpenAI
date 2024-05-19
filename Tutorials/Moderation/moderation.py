import os
from openai import OpenAI


client = OpenAI()

response = client.moderations.create(input="I own a lot of guns which I intend to use, in order to harm people")

output = response.results[0]

print(output)