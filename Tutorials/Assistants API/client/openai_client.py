""" 
If you have set your API Key as a system wide variable you may siply use:

from openai import OpenAI
    client = OpenAI()

"""

import os
from dotenv import load_dotenv
from openai import OpenAI

def create():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables.")
    
    return OpenAI(api_key=api_key)