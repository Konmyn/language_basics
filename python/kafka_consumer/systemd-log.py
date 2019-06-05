from kafka import KafkaConsumer
from kafka import TopicPartition
import json

brokers = ["10.1.10.207:9092", "10.1.10.208:9092", "10.1.10.209:9092"]
# topic = "ops.kube-logs-fluentbit.stream.json.application"
# topic = "fluentd.log.systemd"
# topic = "fluentd.log.application"
# topic = "fluentd.log.kubernetes"
# topic = "filebeats.log.application"
topic = "fluentbit.systemd"


partition0 = TopicPartition(topic, 0)
partition1 = TopicPartition(topic, 1)
partition2 = TopicPartition(topic, 2)

min_time = max_time = None
total_count = 0

for i in range(3):
    partition = TopicPartition(topic, i)
    consumer = KafkaConsumer(
        group_id="python_eater",
        bootstrap_servers=brokers,
        value_deserializer=lambda m: json.loads(m.decode('ascii'))
    )

    consumer.assign([partition])

    consumer.seek(partition, 0)
    i = 0
    for message in consumer:
        log = message.value
        print(log["SYSLOG_IDENTIFIER"])
        if log["SYSLOG_IDENTIFIER"] != "kubelet":
            print(log)
        if min_time == None:
            min_time = log.get("timestamp")
        min_time = min(log.get("timestamp"), min_time)
        # i += 1
        # if i > 10:
        break

    last = consumer.end_offsets([partition])[partition]
    total_count += last
    consumer.seek(partition, last - 1)
    for message in consumer:
        log = message.value
        print(log["SYSLOG_IDENTIFIER"])
        if log["SYSLOG_IDENTIFIER"] != "kubelet":
            print(log)
        if max_time == None:
            max_time = log.get("timestamp")
        max_time = max(log.get("timestamp"), max_time)
        break

    consumer.close()

print("total count: ", total_count)
if "T" in str(min_time):
    # 2019-01-14T11:36:02.209Z
    from datetime import datetime
    min_time = datetime.strptime(min_time, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
    max_time = datetime.strptime(max_time, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()

print("min time: ", min_time)
print("max time: ", max_time)
print("duration: ", max_time-min_time)

