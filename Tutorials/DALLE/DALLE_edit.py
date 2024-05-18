from openai import OpenAI
from IPython.display import display, Image  


client = OpenAI()

response = client.images.edit(
  model="dall-e-2",
  image=open("original.png", "rb"),
  mask=open("mask.png", "rb"),
  prompt="A hand holding a sandwich",
  n=1,
  size="1024x1024"
)
image_url = response.data[0].url

print(image_url)
display(Image(url=image_url, width=400)) 
