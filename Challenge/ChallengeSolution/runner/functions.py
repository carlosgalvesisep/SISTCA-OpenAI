from openai import OpenAI

client = OpenAI()


def cinema(type,theme,quantity):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON. For each item you need to put the title, director,year, rating and small plot, if you dont have information about does topics just write NA"},
            {"role": "user", "content": f"Give me the top {quantity} {type} from this category/genre {theme}"}
        ] 
    )
    
    print(response.choices[0].message.content)      
    return response.choices[0].message.content