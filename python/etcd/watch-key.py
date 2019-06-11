import etcd3

etcd = etcd3.client(host='localhost', port=2379)

watch_count = 0
events_iterator, cancel = etcd.watch("/key/to/watch")
for event in events_iterator:
    print(event)
    print(event.key)
    print(event.value.decode())
    watch_count += 1
    if watch_count > 10:
        print("cancelling")
        cancel()
        break
