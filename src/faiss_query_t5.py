import faiss
import numpy as np
import json

from src.data_enum import Enum
from transformers import T5Tokenizer, T5ForConditionalGeneration

class FaissQueryT5:

    metadata = None
    neighbours = 3
    default_following_data = '\n Use following data: '
    default_question = "What are the trends in PM2.5 levels?"
    default_context = "Analyze the following air quality data:"
    default_prompt = "Analyze the air quality data below and summarize the trends in PM2.5, PM10, and SO2 levels over time:"

    def __init__(self):
        self.index = faiss.read_index(Enum.INDEX_FILE)
        self.t5_tokenizer = T5Tokenizer.from_pretrained("t5-small", legacy=True)
        self.t5_model = T5ForConditionalGeneration.from_pretrained("t5-small")

    def ask_t5_via_question(self, asked_question, context):
        self.metadata = self._load_metadata()

        input_text = (asked_question + context + " ".join(self.metadata[:self.neighbours]))

        return input_text, self._ask_t5(input_text)

    def ask_t5_via_prompt(self, prompt):
        self.metadata = self._load_metadata()

        input_text = prompt + ''.join(self.metadata[:self.neighbours])

        return input_text, self._ask_t5(input_text)

    def _ask_t5(self, input_text):
        self._show_best_data()

        input_ids = self.t5_tokenizer.encode(input_text, return_tensors="pt")
        outputs = self.t5_model.generate(input_ids)

        print("Generated Answer:", self.t5_tokenizer.decode(outputs[0], skip_special_tokens=True))
        return str(self.t5_tokenizer.decode(outputs[0], skip_special_tokens=True))

    def _found_neighbours(self):
        self.distances, self.indices = self.index.search(
            np.array([Enum.QUERY_VECTOR], dtype='float32'),
            self.neighbours
        )

    def _show_best_data(self):
        self._found_neighbours()

        print("Top documents:")

        for i, idx in enumerate(self.indices[0]):
            print(f"Rank {i+1}: {self.metadata[idx]} (Distance: {self.distances[0][i]})")

    @staticmethod
    def _load_metadata():
        metadata = []
        with open(Enum.METADATA_FILE, 'r') as file:
            filenames = json.load(file)

        for filedata in filenames:
            filename = filedata['filename']
            date = filedata['date']
            time = filedata['time']

            with open(Enum.METADATA_PATH + filename, 'r') as file:
                data = json.load(file)
                components_section = data['list'][0]['components']

                pm25 = components_section['pm2_5']
                pm10 = components_section['pm10']
                so2 = components_section['so2']
                metadata.append(
                    f' Date: {date}, Time: {time}, PM2.5: {pm25}, PM10: {pm10}, SO2: {so2}'
                )
        return metadata