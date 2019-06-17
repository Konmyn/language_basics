#! /usr/bin/env python3

import json
import boto3
import sys


def get_bucket():
    with open('credentials-lab.json', 'r') as f:
        conn_info = json.loads(f.read())

    conn = boto3.resource(
        's3',
        endpoint_url=conn_info['endpoint_url'],
        aws_access_key_id=conn_info['access_key'],
        aws_secret_access_key=conn_info['secret_key']
    )

    bucket = conn.Bucket("k8s-lab-harbor")
    return bucket


def list_key(bucket):
    for i in bucket.objects.all():
        print(
            "{name}\t{size}\t{modified}".format(
                name=i.key, size=i.size, modified=i.last_modified
            )
        )


# delete specific key
def delete_key(bucket, key):
    print(bucket.delete_key(key))


# empty bucket
def clear_bucket(bucket):
    return bucket.objects.all().delete()


def run():
    bucket = get_bucket()
    list_key(bucket)
    if len(sys.argv) > 1 and sys.argv[-1] == "d":
        print("deleting all keys in bucket")
        clear_bucket(bucket)


def main():
    print("starting..")
    run()
    print("finishing..")


if __name__ == "__main__":
    main()
