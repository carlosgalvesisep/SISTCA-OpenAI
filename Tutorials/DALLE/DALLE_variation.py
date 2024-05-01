from IPython.display import display, Image
from openai import OpenAI
client = OpenAI()

response = client.images.create_variation(
  model="dall-e-2",
  image=open("image.png", "rb"),
  n=1,
  size="1024x1024"
)

image_url = response.data[0].url

print(image_url)
display(Image(url=image_url, width=400))