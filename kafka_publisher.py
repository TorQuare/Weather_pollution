from kafka import KafkaProducer
import json
import requests
import time

API_KEY = 'eba2db0985f0c748f320ab917a0f3e36'
CITY = 'Gdańsk'
KAFKA_TOPIC = 'air_quality'
BROKER = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_air_quality():
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat=54.3521&lon=18.6466&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error fetching data: {response.status_code}')
        return None

while True:
    air_quality_data = fetch_air_quality()
    if air_quality_data:
        print(f'Publishing: {air_quality_data}')
        producer.send(KAFKA_TOPIC, air_quality_data)
    time.sleep(3600)
