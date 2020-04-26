#!/bin/bash
docker build -t docker.io/restrict/harbor-registry-migration:python3-stretch .
docker push docker.io/restrict/harbor-registry-migration:python3-stretch
