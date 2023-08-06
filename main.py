from fastapi import FastAPI
import openai
import json
from sklearn.metrics.pairwise import cosine_similarity
import os

openai.api_key = os.environ['OPENAI_API_KEY']

app = FastAPI()

# Load the saved procedures and embeddings
with open('vector_db.json', 'r') as f:
    data = json.load(f)
    strings = data['strings']
    embeddings = data['embeddings']

@app.get("/search/")
async def search_procedure(query: str):
    # Generate embedding for the query using OpenAI Ada
    response = openai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_embedding = response['data'][0]['embedding']

    # Compute cosine similarity between the query embedding and the saved embeddings
    similarities = cosine_similarity([query_embedding], embeddings)[0]

    # Get the index of the most similar embedding
    index = similarities.argmax()

    # Return the corresponding procedure
    return {"procedure": strings[index]}