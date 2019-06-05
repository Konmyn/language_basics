from kafka import SimpleClient
from kafka.protocol.offset import OffsetRequest, OffsetResetStrategy
from kafka.common import OffsetRequestPayload

brokers = ["10.1.10.207:9092", "10.1.10.208:9092", "10.1.10.209:9092"]
topic = "ops.kube-logs-fluentbit.stream.json.application"
client = SimpleClient(brokers)

partitions = client.topic_partitions[topic]
offset_requests = [OffsetRequestPayload(topic, p, -1, 1) for p in partitions.keys()]

offsets_responses = client.send_offset_request(offset_requests)

for r in offsets_responses:
    print("partition = %s, offset = %s" % (r.partition, r.offsets[0]))
