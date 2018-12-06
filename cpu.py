# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2018-11-21 14:28:01 (+0800)
    :last modified date: 2018-12-06 14:02:52 (+0800)
    :last modified by: lyncir
"""
import socket
import time
import asyncio
import psutil

from aiostatsd.client import StatsdClient


hostname = socket.gethostname()


async def collect_cpu(client):
    cpu_percents, cur_time = psutil.cpu_percent(percpu=True), time.time()

    for i in range(len(cpu_percents)):
        value = cpu_percents[i]

        metric_path = '{}.cpu{}.percent'.format(hostname, i)

        # send statsd
        print(cur_time, metric_path, value)
        # client.send_gauge(metric_path, value)


async def main():
    client = StatsdClient('192.168.32.231', 8125)
    asyncio.ensure_future(client.run())

    while True:
        await collect_cpu(client)
        await asyncio.sleep(5)

    await client.stop()


if __name__ == '__main__':
    asyncio.run(main())
