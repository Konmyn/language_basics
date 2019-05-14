#! /usr/bin/env python3

import os
import re
import concurrent.futures

# https://stackoverflow.com/questions/49822552/python-asyncio-typeerror-object-dict-cant-be-used-in-await-expression
# https://docs.python.org/3/library/concurrent.futures.html

# 10 packets transmitted, 10 received, 0% packet loss, time 9016ms
# rtt min/avg/max/mdev = 56.799/81.700/108.942/15.579 ms

p_statistic = (
    r"(\d+) packets transmitted, (\d+) received, (\d+)% packet loss, time (\d+)ms"
)
p_statistic = re.compile(p_statistic)

p_delay = r"rtt min/avg/max/mdev = (\d+.?\d*)/(\d+.?\d*)/(\d+.?\d*)/(\d+.?\d*) ms"
p_delay = re.compile(p_delay)

hostnames = list()

with open("ss_host.txt") as f:
    for i in f.readlines():
        if i.startswith("#"):
            continue
        else:
            hostnames.append(i.strip())


def ping_server(hostname, count=10):
    # response = os.system("ping -c 1 " + hostname)
    response = os.popen("ping -c {} {}".format(count, hostname)).read()

    packets_num, packets_received, packets_loss, total_time = None, None, None, None
    min_delay, avg_delay, max_delay, mdev_delay = None, None, None, None
    statistic = re.findall(p_statistic, response)
    if len(statistic) == 1:
        r = statistic[0]
        packets_num, packets_received, packets_loss, total_time = r
    delay = re.findall(p_delay, response)
    if len(delay) == 1:
        d = delay[0]
        min_delay, avg_delay, max_delay, mdev_delay = d

    result = {
        "packets_num": packets_num,
        "packets_received": packets_received,
        "packets_loss": packets_loss,
        "total_time": total_time,
        "min_delay": min_delay,
        "avg_delay": avg_delay,
        "max_delay": max_delay,
        "mdev_delay": mdev_delay,
    }

    return result


def main(count=10):
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(hostnames)) as executor:
        # Start the load operations and mark each future with its URL
        future_to_host = {
            executor.submit(ping_server, hostname, count): hostname
            for hostname in hostnames
        }
        result = list()
        for future in concurrent.futures.as_completed(future_to_host):
            host = future_to_host[future]
            try:
                data = future.result()
            except Exception as exc:
                print(host, exc)
            else:
                # print(host, data)
                data["host"] = host
                result.append(data)
        result = sorted(
            result,
            key=lambda x: (
                int(x["packets_loss"]),
                float(x["avg_delay"]) if x["avg_delay"] else 9999,
            ),
        )
        for i in result:
            print(
                ("{:>20}" * 3).format(
                    *(
                        "{}:".format(i["host"]),
                        "packets_loss {:>3}%".format(i["packets_loss"]),
                        "avg_delay {}".format(i["avg_delay"]),
                    )
                )
            )


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option(
        "-c",
        "--count",
        dest="count",
        type="int",
        help="counts for the ping command",
        default=10,
    )
    options, _ = parser.parse_args()
    main(options.count)
