import openai
import os
import json

openai.api_key = os.environ['OPENAI_API_KEY']

# Path to the folder containing the text files
folder_path = 'procedures'

# Read the procedures from the text files
strings = []
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            procedure = file.read().strip()
            strings.append(procedure)

# Generate embeddings for the list of strings using OpenAI Ada
embeddings = []
for string in strings:
    response = openai.Embedding.create(
        input=string,
        model="text-embedding-ada-002"
    )
    embeddings.append(response['data'][0]['embedding'])

# Save the embeddings and the list of strings to a JSON file
with open('vector_db.json', 'w') as f:
    json.dump({'strings': strings, 'embeddings': embeddings}, f)

print("Embeddings and procedures saved to vector_db.json")