from kafka import KafkaConsumer
import json
import os
from src.data_enum import Enum
from datetime import datetime

class Subscriber:

    def __init__(self):
        os.makedirs(Enum.DOCUMENTS_DIR, exist_ok=True)
        self.consumer = KafkaConsumer(
            Enum.KAFKA_TOPIC,
            bootstrap_servers=Enum.BROKER,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def collect_data(self):
        print('works')
        for message in self.consumer:
            data = message.value
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            file_name = f"{Enum.DOCUMENTS_DIR}air_quality_{timestamp}.json"
            with open(file_name, 'w') as file:
                json.dump(data, file)
            print(f"Document created: {file_name}")