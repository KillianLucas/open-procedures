# This is used by Open Interpreter ^0.1.8.
# It's simply {text: embedding, another_text: another_embedding}

import os
import json
import numpy as np
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction as setup_embed

# Set up the embedding function
embed_function = setup_embed()

folder_path = 'procedures'

db = {}

# Iterate through files
for idx, filename in enumerate(os.listdir(folder_path)):
  if filename.endswith(".txt"):
    with open(os.path.join(folder_path, filename), 'r',
              encoding='utf-8') as file:
      # Read the content from the file
      content = file.read().strip()

      # Extract the full text
      full_text = content

      # Embed full text using Chroma
      embedding = np.squeeze(embed_function([full_text]))

      # Store in db
      db[full_text] = embedding

# Save embeddings
with open('procedures_db.json', 'w') as f:
  json.dump(db, f)