from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import re
import os
import json
import openai
import markdown
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
  # Convert README.md into HTML
  with open('README.md', 'r') as file:
    content = file.read()
  content = markdown.markdown(content)

  # Replace <p><code> with <pre><code> and </code></p> with </code></pre>
  content = re.sub(r'<p><code>(.*?)\n', r'<pre><code>\1\n', content)
  content = content.replace('</code></p>', '</code></pre>')

  # Serve the HTML at `/` using Water.css
  html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/dark.css">
        <title>Open Procedures</title>
    </head>
    <body class="prose p-4">
        {content}
    </body>
    </html>
    """
  return HTMLResponse(html_content)