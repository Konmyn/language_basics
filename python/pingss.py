#! /usr/bin/env python3

import os
import re
import asyncio

# https://stackoverflow.com/questions/49822552/python-asyncio-typeerror-object-dict-cant-be-used-in-await-expression
# 10 packets transmitted, 10 received, 0% packet loss, time 9016ms
# rtt min/avg/max/mdev = 56.799/81.700/108.942/15.579 ms

p_statistic = r"(\d+) packets transmitted, (\d+) received, (\d+)% packet loss, time (\d+)ms"
p_statistic = re.compile(p_statistic)

p_delay = r"rtt min/avg/max/mdev = (\d+.?\d*)/(\d+.?\d*)/(\d+.?\d*)/(\d+.?\d*) ms"
p_delay = re.compile(p_delay)

hostnames = [
    "jp.a.cloudss.win",
    "hk.a.cloudss.win",
    "hk.b.cloudss.win",
    "hk.c.cloudss.win",
    "hk.d.cloudss.win",
    "sg.a.cloudss.win",
    "sg.b.cloudss.win",
    "kr.a.cloudss.win",
    "kr.b.cloudss.win",
    "tw.a.cloudss.win",
    "tw.b.cloudss.win",
    "us.a.cloudss.win",
    "us.b.cloudss.win",
    "us.c.cloudss.win",
    "ru.a.cloudss.win",
    "mo.a.cloudss.win",
    "in.a.cloudss.win",
]


async def ping_server(hostname):
    # response = os.system("ping -c 1 " + hostname)
    response = await os.popen("ping -c 1 " + hostname).read()

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
        "mdev_delay": mdev_delay
    }

    return result


async def main():
    tasks = [ping_server(i) for i in hostnames]
    result = await asyncio.gather(*tasks)
    print(result)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
