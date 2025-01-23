import os
import json
import faiss
import numpy as np

DOCUMENTS_DIR = './data/'
INDEX_FILE = './faiss_index'

def load_documents():
    vectors = []
    metadata = []

    for filename in os.listdir(DOCUMENTS_DIR):

        if filename.endswith('.json'):

            with open(os.path.join(DOCUMENTS_DIR, filename), 'r') as file:
                data = json.load(file)

                date = filename.replace('air_quality_', '').replace('.json', '')
                date = date.split('_')
                components_section = data['list'][0]['components']

                pm25 = components_section['pm2_5']
                pm10 = components_section['pm10']
                so2 = components_section['so2']

                vectors.append([pm25, pm10, so2])
                metadata.append({'filename': filename, 'date': date[0], 'time': date[1]})

    return np.array(vectors, dtype='float32'), metadata

vectors, metadata = load_documents()

# Tworzenie FAISS index
dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(vectors)

# Zapisanie indeksu
faiss.write_index(index, INDEX_FILE)
with open('metadata.json', 'w') as f:
    json.dump(metadata, f)

print(f"Indexed {len(vectors)} documents.")