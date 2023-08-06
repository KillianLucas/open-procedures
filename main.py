from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

app = FastAPI()

# Load a pre-trained sentence transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load the saved embeddings and strings
with open('vector_db.pkl', 'rb') as f:
    strings, embeddings = pickle.load(f)

@app.get("/search/")
async def search_procedure(query: str):
    # Generate embedding for the query
    query_embedding = model.encode([query])

    # Compute cosine similarity between the query embedding and the saved embeddings
    similarities = cosine_similarity(query_embedding, embeddings)[0]

    # Get the index of the most similar embedding
    index = similarities.argmax()

    # Return the corresponding procedure
    return {"procedure": strings[index]}
