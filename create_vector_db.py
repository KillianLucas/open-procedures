import os
import re
import json
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

folder_path = 'procedures'

# Structures to hold embeddings and texts
embeddings_data = []
texts_data = {}

# Iterate through files
for idx, filename in enumerate(os.listdir(folder_path)):
  if filename.endswith(".txt"):
    with open(os.path.join(folder_path, filename), 'r',
              encoding='utf-8') as file:
      # Read the content from the file
      content = file.read().strip()

      # Check if "trigger phrases:" is present in the content
      if content.startswith("trigger phrases:"):
        # Use regular expressions to find all phrases enclosed in quotes after "trigger phrases:"
        key_phrases_line = content.split("\n")[0]
        key_phrases = re.findall(r'"(.*?)"', key_phrases_line)

        # Extract the full text by taking everything after the first line
        full_text = "\n".join(content.split("\n")[1:]).strip()
      else:
        # If "trigger phrases:" is not present, consider the entire content as the full text
        key_phrases = []
        full_text = content

      # Store full text
      texts_data[str(idx)] = full_text
      if "system trigger phrases:" in full_text.split("\n")[0]:
        continue

      # Embed full text
      response = openai.Embedding.create(input=full_text,
                                         model="text-embedding-ada-002")
      embeddings_data.append({
        "id": idx,
        "embedding": response['data'][0]['embedding']
      })

      # Embed key phrases
      for phrase in key_phrases:
        response = openai.Embedding.create(input=phrase,
                                           model="text-embedding-ada-002")
        embeddings_data.append({
          "id": idx,
          "embedding": response['data'][0]['embedding']
        })

# Save embeddings and texts
with open('vector_db.json', 'w') as f:
  json.dump({"embeddings": embeddings_data}, f)

with open('text_db.json', 'w') as f:
  json.dump({"texts": texts_data}, f)

print("Embeddings and texts saved.")
