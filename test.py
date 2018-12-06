# -*- coding: utf8 -*-
import socket
import time
import statsd

import psutil

from app import settings


config = settings.get_config()
hostname = socket.gethostname()

conn = statsd.Connection(config['statsd']['host'], config['statsd']['port'])
gauge = statsd.Gauge('.'.join([hostname, 'cpu']), conn)


while True:
    cpu_percents = psutil.cpu_percent(percpu=True)
    for i in range(len(cpu_percents)):
        value = cpu_percents[i]
        metric_path = 'cpu{}.percent'.format(i)
        print(time.time(), metric_path, value)
        gauge.send(metric_path, value)

    time.sleep(1)
