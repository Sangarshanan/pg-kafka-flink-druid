import time
from kafka import KafkaConsumer

def get_bootstrap_servers():
    return ["localhost:9092"]

consumer = KafkaConsumer(
    "dbserver1.public.test",
    bootstrap_servers=get_bootstrap_servers(),
    value_deserializer=lambda x: x.decode('utf-8', errors='replace')
)

print(consumer.topics())

# for message in consumer:
#     print(message)
#     time.sleep(3)
