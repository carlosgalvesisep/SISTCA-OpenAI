from openai import OpenAI
client = OpenAI()
from IPython.display import display, Image # comfirmar 

response = client.images.edit(
  model="dall-e-2",
  image=open("original.png", "rb"),
  mask=open("mask.png", "rb"),
  prompt="A sunlit indoor lounge area with a pool containing a flamingo",
  n=1,
  size="1024x1024"
)
image_url = response.data[0].url

print(image_url)
display(Image(url=image_url, width=400)) # comfirmar 
