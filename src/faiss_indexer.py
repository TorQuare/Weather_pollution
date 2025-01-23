import os
import json
import faiss
import numpy as np
from src.data_enum import Enum


class Indexer:

    def __init__(self):
        self.metadata = []

    def save_faiss_index(self):
        self._load_documents()
        self._create_faiss_index()

        faiss.write_index(self.index, Enum.INDEX_FILE)

        with open('metadata.json', 'w') as file:
            json.dump(self.metadata, file)

        print(f"Indexed {len(self.vectors)} documents.")

    def _load_documents(self):
        vectors = []
        for filename in os.listdir(Enum.DOCUMENTS_DIR):

            if filename.endswith('.json'):

                with open(os.path.join(Enum.DOCUMENTS_DIR, filename), 'r') as file:
                    data = json.load(file)

                    date = filename.replace('air_quality_', '').replace('.json', '')
                    date = date.split('_')
                    components_section = data['list'][0]['components']

                    pm25 = components_section['pm2_5']
                    pm10 = components_section['pm10']
                    so2 = components_section['so2']

                    vectors.append([pm25, pm10, so2])
                    self.vectors = np.array(vectors, dtype='float32')
                    self.metadata.append({'filename': filename, 'date': date[0], 'time': date[1]})

    def _create_faiss_index(self):
        dimension = self.vectors.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.vectors)
