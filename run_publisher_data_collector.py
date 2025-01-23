from src.kafka_to_doc import Subscriber
from src.kafka_publisher import Publisher
import multiprocessing

def run_publisher():
    publisher = Publisher()
    publisher.publish()

def run_subscriber():
    subscriber = Subscriber()
    subscriber.collect_data()

thread2 = multiprocessing.Process(target=run_subscriber())
thread1 = multiprocessing.Process(target=run_publisher())

thread1.start()
thread2.start()