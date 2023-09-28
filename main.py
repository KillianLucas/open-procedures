from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import re
import os
import json
import openai
import markdown
from sklearn.metrics.pairwise import cosine_similarity

# Set up OpenAI
openai.api_key = os.environ['OPENAI_API_KEY']

# Load the saved embeddings
with open('vector_db.json', 'r') as f:
  embedding_data = json.load(f)
  embeddings = [item['embedding'] for item in embedding_data['embeddings']]

# Load the saved texts
with open('text_db.json', 'r') as f:
  texts = json.load(f)['texts']


# Define the search function
def search(query):

  # Generate embedding for the query using OpenAI Ada
  response = openai.Embedding.create(input=query,
                                     model="text-embedding-ada-002")
  query_embedding = response['data'][0]['embedding']

  # Compute cosine similarity
  similarities = cosine_similarity([query_embedding], embeddings)[0]

  # Get the indices of the embeddings sorted by similarity
  sorted_indices = similarities.argsort()[::-1]

  # Collect unique top procedure IDs
  top_ids = set()
  top_procedures = []
  for index in sorted_indices:
    id_ = embedding_data['embeddings'][index]['id']
    if id_ not in top_ids:
      top_procedures.append(texts[str(id_)])
      top_ids.add(id_)
      if len(top_procedures
             ) == 2:  # Change this value to control the number of results
        break

  # Return the corresponding procedures
  return {"procedures": top_procedures}


app = FastAPI()


# GET endpoint for browser testing, small queries (GET is limited to ~2000 chars)
@app.get("/search/")
async def search_procedure_GET(query: str):
  return search(query)


# POST endpoint for large queries (GET is limited to ~2000 chars)
@app.post("/search/")
async def search_procedure_POST(request: Request):
  data = await request.json()
  query = str(data["query"])
  return search(query)


@app.get("/", response_class=HTMLResponse)
async def home():
  # Convert README.md into HTML
  with open('README.md', 'r') as file:
    content = file.read()

  # Remove ```python and ```bash language tags, which aren't properly converted
  content = content.replace("```python", "```").replace("```bash", "```")
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
    <body>
        {content}
    </body>
    </html>
    """
  return HTMLResponse(html_content)
