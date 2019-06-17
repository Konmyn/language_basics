#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import boto3
import sys
from botocore.exceptions import ClientError

PATH = "/data/registry/"


def main(path):

    with open('credentials.json', 'r') as f:
        conn_info = json.loads(f.read())
    s3_conn = boto3.resource(
        's3',
        endpoint_url=conn_info['endpoint_url'],
        aws_access_key_id=conn_info['access_key'],
        aws_secret_access_key=conn_info['secret_key']
    )
    bucket = s3_conn.Bucket(conn_info['bucket'])

    for i in os.walk(path):
        current_path, _, files = i
        for f in files:
            file_path = os.path.join(current_path, f)

            print(file_path)
            key = file_path[len(path):]

            try:
                bucket.Object(key=key).load()
                print("file exists")
                continue
            except ClientError as e:
                assert e.response['Error']['Code'] == "404"

                bucket.upload_file(
                    Filename=file_path,
                    Key=key
                )

                print("uploaded")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else PATH
    if path.endswith("/"):
        main(path)
    else:
        print("please include ending / for the path")
