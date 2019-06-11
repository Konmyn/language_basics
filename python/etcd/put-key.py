# https://github.com/kragniz/python-etcd3
import etcd3
import random
import time

etcd = etcd3.client(host='localhost', port=2379)

for i in range(20):
    randint = str(random.randint(1, 999999))
    print(randint)
    r = etcd.put('/key/to/watch', randint)
    time.sleep(1)
