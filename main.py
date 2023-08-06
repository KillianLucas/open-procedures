from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import os
import json
import openai
from sklearn.metrics.pairwise import cosine_similarity

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
  response = openai.Embedding.create(input=query,
                                     model="text-embedding-ada-002")
  query_embedding = response['data'][0]['embedding']

  # Compute cosine similarity between the query embedding and the saved embeddings
  similarities = cosine_similarity([query_embedding], embeddings)[0]

  # Get the index of the most similar embedding
  index = similarities.argmax()

  # Return the corresponding procedure
  return {"procedure": strings[index]}

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/dark.css">
        <title>Open Procedures</title>
    </head>
    <body>
        <h1>Open Procedures</h1>
        <p>Open Procedures is an open-source database of tiny, structured coding tutorials. We can query it semantically.</p>
        <p>Designed for language models to fetch information about how to complete a coding task, Open Procedures offers a simple and efficient way to access coding knowledge. It's built on an open-source platform and uses text embeddings to understand and respond to natural language queries.</p>
        <p>Here's how you can query the Open Procedures database:</p>
        <h2>Using Python:</h2>
        <pre><code>import requests
        query = 'How to reverse a string in Python?'
        response = requests.get('http://127.0.0.1:8000/search/', params={'query': query})
        print(response.json())</code></pre>
        <h2>Using cURL:</h2>
        <pre><code>curl -G 'http://127.0.0.1:8000/search/' --data-urlencode 'query=How to reverse a string in Python?'</code></pre>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)