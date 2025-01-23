import faiss
import numpy as np
import json
from transformers import T5Tokenizer, T5ForConditionalGeneration

INDEX_FILE = './faiss_index'
METADATA_FILE = './metadata.json'
METADATA_PATH = './data/'
QUERY_VECTOR = [15, 25, 5]  # Przykładowe zapytanie (pm2_5, pm10, so2)

# Załaduj FAISS index
index = faiss.read_index(INDEX_FILE)

def load_metadata():
    metadata = []
    with open(METADATA_FILE, 'r') as file:
        filenames = json.load(file)
        x = filenames
    for filedata in filenames:
        filename = filedata['filename']
        date = filedata['date']
        time = filedata['time']

        with open(METADATA_PATH + filename, 'r') as file:
            data = json.load(file)
            components_section = data['list'][0]['components']

            pm25 = components_section['pm2_5']
            pm10 = components_section['pm10']
            so2 = components_section['so2']
            metadata.append(
                f'Date: {date}, Time: {time}, PM2.5: {pm25}, PM10: {pm10}, SO2: {so2}'
            )
    return metadata

metadata = load_metadata()

# Znajdź najbliższe sąsiady
k = 3
distances, indices = index.search(np.array([QUERY_VECTOR], dtype='float32'), k)

# Wyświetl wyniki
print("Top documents:")
for i, idx in enumerate(indices[0]):
    print(f"Rank {i+1}: {metadata[idx]} (Distance: {distances[0][i]})")

# T5 - Generowanie odpowiedzi
t5_tokenizer = T5Tokenizer.from_pretrained("t5-small", legacy=True)
t5_model = T5ForConditionalGeneration.from_pretrained("t5-small")

question = "What is the trend of air pollution changes?"
input_text = f"Question: {question} Context: {metadata[:k]}"
input_text2 = ("Analyze the following air quality data and describe the trend of air pollution changes: "
              + " ".join(metadata[:k]))
input_ids = t5_tokenizer.encode(input_text, return_tensors="pt")
outputs = t5_model.generate(input_ids)

print("Generated Answer:", t5_tokenizer.decode(outputs[0], skip_special_tokens=True))

input_ids = t5_tokenizer.encode(input_text2, return_tensors="pt")
outputs = t5_model.generate(input_ids)

print("Generated Answer:", t5_tokenizer.decode(outputs[0], skip_special_tokens=True))