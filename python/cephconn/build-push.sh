#!/bin/bash
docker build -t harbor.geniusafc.com/restrict/harbor-registry-migration:python3-stretch .
docker push harbor.geniusafc.com/restrict/harbor-registry-migration:python3-stretch
