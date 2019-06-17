#! /usr/bin/env python3
# http://docs.ceph.com/docs/master/radosgw/s3/python/

import json
import boto.s3.connection


def main():
    print("this script is deprecating!")
    print("this script is deprecating!!")
    print("this script is deprecating!!!")

    with open('credentials.json', 'r') as f:
        conn_info = json.loads(f.read())

    access_key = "WT43H5PBKCPRH9WA2Z9A"
    secret_key = "sgzOdZN380vBAXtyhjBX4jDmHM3ETmU8TxHjp5ED"
    host = "10.33.32.54"
    port = 7480

    print("starting..")
    conn = boto.connect_s3(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        host=host,
        port=port,
        is_secure=False,  # uncomment if you are not using ssl
        calling_format=boto.s3.connection.OrdinaryCallingFormat(),
    )

    print("make conn..")
    # buckets = conn.get_all_buckets()
    # print(buckets[0].name)

    # bucket = conn.create_bucket('k8s-lab-harbor')

    k8s_harbor = conn.get_bucket("k8s-lab-harbor")
    # k8s_harbor = conn.get_bucket("harbor-image")

    # print(k8s_harbor)

    # print(bucket)

    # for bucket in conn.get_all_buckets():
    #     print(conn)
    #     print("{name}\t{created}".format(name=bucket.name, created=bucket.creation_date))

    # print(list(k8s_harbor.list()))

    # for key in k8s_harbor.list():
    #     print(
    #         "{name}\t{size}\t{modified}".format(
    #             name=key.name, size=key.size, modified=key.last_modified
    #         )
    #     )

    for key in k8s_harbor.list():
        print(
            "{name}\t{size}\t{modified}".format(
                name=key.name, size=key.size, modified=key.last_modified
            )
        )
        # 删除该key
        # print(k8s_harbor.delete_key(key.name))


if __name__ == "__main__":
    main()
