from kafka import KafkaProducer
import json
import requests
import time
from src.data_enum import Enum


class Publisher:

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=Enum.BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def publish(self):
        while True:
            air_quality_data = self._fetch_air_quality()
            if air_quality_data:
                print(f'Publishing: {air_quality_data}')
                self.producer.send(Enum.KAFKA_TOPIC, air_quality_data)
            time.sleep(3600)

    @staticmethod
    def _fetch_air_quality():
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat=54.3521&lon=18.6466&appid={Enum.API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error fetching data: {response.status_code}')
            return None


