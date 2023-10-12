# This is used by Open Interpreter ^0.1.8.
# It's simply [{text: embedding}, {text: embedding}, ...]

import os
import json
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction as setup_embed

print("setting up function")
# Set up the embedding function
embed_function = setup_embed()

folder_path = 'procedures'

# Structures to hold embeddings and texts
embeddings_data = []

print("going through files")
# Iterate through files
for idx, filename in enumerate(os.listdir(folder_path)):
  if filename.endswith(".txt"):
    print("filename:", filename)
    with open(os.path.join(folder_path, filename), 'r',
              encoding='utf-8') as file:
      # Read the content from the file
      content = file.read().strip()

      # Extract the full text
      full_text = content

      # Embed full text using Chroma
      print("embedding...")
      embedding = embed_function(full_text)
      print("done!")

      # Store in desired format
      embeddings_data.append({full_text: embedding})

# Save embeddings
with open('procedures_db.json', 'w') as f:
  json.dump(embeddings_data, f)

print("Created `procedures_db.py`.")
