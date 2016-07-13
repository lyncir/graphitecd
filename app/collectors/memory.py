# -*- coding: utf8 -*-

import time
import statsd
import psutil

from app import settings


config = settings.get_config()


class Collector(object):
    def __init__(self):
        self.cfg = settings.get_config()
        self.path = 'memory'
        self.conn = statsd.Connection(self.cfg['statsd']['host'],
                self.cfg['statsd']['port'])

    def collect(self):
        """
        Collect memory stats.
        """
        mem = psutil.virtual_memory()

        gauge = statsd.Gauge('.'.join([self.cfg['default']['hostname'], self.path]), self.conn)
        for m in mem._fields:
            value = getattr(mem, m)
            gauge.send(m, value)
