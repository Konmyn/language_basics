#!/bin/bash
docker run -p 2379:2379 --rm -it -p 4001:4001 --name etcd \
	docker.io/k8s.gcr.io/etcd:3.2.24 \
	etcd --listen-client-urls 'http://0.0.0.0:2379' --advertise-client-urls 'http://0.0.0.0:2379'
