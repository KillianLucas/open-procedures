from sentence_transformers import SentenceTransformer
import os
import pickle

# Path to the folder containing text files
folder_path = 'procedures'

# Read the procedures from the text files
strings = []
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            procedure = file.read().strip()
            strings.append(procedure)

# Load a pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for the list of strings
embeddings = model.encode(strings)

# Save the embeddings and the list of strings to a file
with open('vector_db.pkl', 'wb') as f:
    pickle.dump((strings, embeddings), f)

print("Embeddings and procedures saved to vector_db.pkl")
