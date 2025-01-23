from kafka import KafkaConsumer
import json
import os
from datetime import datetime

KAFKA_TOPIC = 'air_quality'
BROKER = 'localhost:9092'
DOCUMENTS_DIR = './data/'

os.makedirs(DOCUMENTS_DIR, exist_ok=True)

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=BROKER,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    data = message.value
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = f"{DOCUMENTS_DIR}air_quality_{timestamp}.json"
    with open(file_name, 'w') as file:
        json.dump(data, file)
    print(f"Document created: {file_name}")