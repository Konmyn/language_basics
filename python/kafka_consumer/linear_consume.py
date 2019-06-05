from kafka import KafkaConsumer
from kafka import TopicPartition
from kafka import SimpleClient
from kafka.protocol.offset import OffsetRequest, OffsetResetStrategy
from kafka.common import OffsetRequestPayload
import json

brokers = ["10.1.10.207:9092", "10.1.10.208:9092", "10.1.10.209:9092"]
topic = "fluentbit.container"

consumer = KafkaConsumer(
    group_id="python_eater",
    bootstrap_servers=["10.1.10.207:9092", "10.1.10.208:9092", "10.1.10.209:9092"],
    # auto_offset_reset='earliest',
    # enable_auto_commit=True
    value_deserializer=lambda m: json.loads(m.decode('ascii'))
)
consumer.subscribe([topic])

count = 0
ns = set()
consumer.poll()
consumer.seek_to_beginning()
for message in consumer:
    # print(message.value)
    kuber = message.value.get("kubernetes")
    if kuber:
        nas = kuber.get("namespace_name")
        if nas:
            if nas not in ns:
                ns.add(nas)
        else:
            print(message.value)
    else:
        print(message.value)
    count += 1
    if count % 10000 == 0:
        print(count)
        print(ns)
    # if count > 5:
    #     break

print(count)
