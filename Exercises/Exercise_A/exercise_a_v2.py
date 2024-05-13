# imports
import ast 
from openai import OpenAI
import pandas as pd 
import tiktoken 
from scipy import spatial  


client = OpenAI()

# TODO #4: Change the EMBEDDING_MODEL (ada)
EMBEDDING_MODEL = "text-embedding-ada-002"

GPT_MODEL = "gpt-3.5-turbo"

# TODO #5: Create a variable with the CSV file path
embeddings_path = "SISTCA_TEAM2.csv"

df = pd.read_csv(embeddings_path)
df['embedding'] = df['embedding'].apply(ast.literal_eval)

def strings_ranked_by_relatedness(query, df , relatedness_fn = lambda x, y: 1 - spatial.distance.cosine(x, y), top_n = 100) :
    
    # TODO 6: Make a request to the embeddings API with the query as input
    query_embedding_response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    
    query_embedding = query_embedding_response.data[0].embedding
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]

strings, relatednesses = strings_ranked_by_relatedness("open ai", df, top_n=5)

def num_tokens(text, model = GPT_MODEL):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def query_message(query,df, model, token_budget):
    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    introduction = 'Use the below articles on the document about OpenAI made by Team 2, composed by Patrícia Sousa, Carlos Alves, Jose Leal and Tiago Ribeiro, for SISTCA to answer the subsequent question. If the answer cannot be found in the articles, write "Sorry, the information you seek cannot be found in the document in question."'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_article = f'\n\nPDF article section:\n"""\n{string}\n"""'
        if (
            num_tokens(message + next_article + question, model)
            > token_budget
        ):
            break
        else:
            message += next_article
    return message + question


def ask(query, df = df, model = GPT_MODEL, token_budget = 4096 - 500, print_message = False):
    message = query_message(query, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    messages = [
        {"role": "system", "content": "You answer questions about the document made by Team2 for SISTCA about OpenAI."},
        {"role": "user", "content": message},
    ]
    
    # TODO 7: Make a request to the Chat Completions API
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    response_message = response.choices[0].message.content
    return response_message

print(ask("Tell me about whisper or tts")) 
print(ask("Give me the authors")) 
print(ask("What can you tell me about the document")) 
print(ask("Give me the document structure"))
