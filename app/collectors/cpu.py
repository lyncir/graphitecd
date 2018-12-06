# -*- coding: utf8 -*-

import socket
import time
import statsd
import psutil

from app import settings


config = settings.get_config()


class Collector(object):
    def __init__(self):
        self.cfg = settings.get_config()
        self.path = 'cpu'
        self.conn = statsd.Connection(self.cfg['statsd']['host'],
                self.cfg['statsd']['port'])

    def collect(self):
        """
        Collect cpu stats.
        """
        cpu_percents = psutil.cpu_percent(percpu=True)

        gauge = statsd.Gauge('.'.join([self.cfg['default']['hostname'], self.path]), self.conn)
        for c in cpu_time._fields:
            value = getattr(cpu_time, c)
            gauge.send(c, value)
