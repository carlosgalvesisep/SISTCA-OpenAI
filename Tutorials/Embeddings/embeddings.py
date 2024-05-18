import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI


client = OpenAI()


response1 = client.embeddings.create(
    input="We are testing to see if this string has any similarities to another one.",
    model="text-embedding-3-small"
)

embeddings1 = response1.data[0].embedding

response2 = client.embeddings.create(
    input="We're experimenting to determine if this string bears resemblance to another.",
    model="text-embedding-3-small"
)

embeddings2 = response2.data[0].embedding

embeddings1 = np.array(embeddings1).reshape(1, -1)
embeddings2 = np.array(embeddings2).reshape(1, -1)

similarity_score = cosine_similarity(embeddings1, embeddings2)

final_score = float(format(similarity_score[0][0], ".2f"))

print("Similarity: ", final_score)

if final_score < 0.25:
    print("Totally Different")
elif final_score <= 0.5:
    print("Different")
elif final_score <= 0.75:
    print("Parcial Equal")
elif final_score <= 0.90:
    print("Almost Equal")
elif final_score <= 1:
    print("Equal")
else:
    print("Unknown value")