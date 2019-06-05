from kafka import KafkaConsumer
from kafka import TopicPartition
from kafka import SimpleClient
from kafka.protocol.offset import OffsetRequest, OffsetResetStrategy
from kafka.common import OffsetRequestPayload

brokers = ["10.1.10.207:9092", "10.1.10.208:9092", "10.1.10.209:9092"]
# topic = "fluentbit.container"
topic = "fluentbit.application"

partition0 = TopicPartition(topic, 0)
partition1 = TopicPartition(topic, 1)
partition2 = TopicPartition(topic, 2)
# print(partition0)
# print(partition1)
# print(partition2)
# topic = "ops.kube-logs-fluentbit.stream.json.systemd"
# topic = "ops.kube-logs-fluentbit.stream.json.container"
# client = SimpleClient(brokers)

# partitions = client.topic_partitions[topic]
# print(partitions)

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer(
    group_id="python_eater",
    bootstrap_servers=["10.1.10.207:9092", "10.1.10.208:9092", "10.1.10.209:9092"],
    # auto_offset_reset='earliest',
    # enable_auto_commit=True
)
consumer.subscribe([topic])
# print(consumer.subscription())
# print(consumer.topics())
# print(consumer.partitions_for_topic("ops.kube-logs-fluentbit.stream.json.application"))
# print(consumer.beginning_offsets(["0"]))
count = 0
#dummy poll
consumer.poll()
#go to end of the stream
# consumer.seek_to_end()
#start iterate
# consumer.seek(partition0, 0)
# consumer.seek(partition1, 0)
# consumer.seek(partition2, 0)
consumer.seek_to_beginning()
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    # print(
    #     "%s:%d:%d: key=%s value=%s"
    #     % (message.topic, message.partition, message.offset, message.key, message.value)
    # )
    # print(message)
    print(message.value)
    # count += 1
    # if count > 5:
    #     break
