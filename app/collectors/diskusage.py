# -*- coding: utf8 -*-

import statsd
import psutil

from app import settings


config = settings.get_config()


class Collector(object):
    def __init__(self):
        self.cfg = settings.get_config()
        self.path = 'diskusage'
        self.conn = statsd.Connection(self.cfg['statsd']['host'],
                self.cfg['statsd']['port'])

    def collect(self):
        """
        Collect disk usage stats.
        """
        parts = psutil.disk_partitions()
        for part in parts:
            usage = psutil.disk_usage(part.mountpoint)
            gauge = statsd.Gauge('.'.join([config['default']['hostname'], self.path,
                part.mountpoint]), self.conn)
            gauge.send('total', usage.total)
            gauge.send('used', usage.used)
            gauge.send('free', usage.free)
            gauge.send('percent', usage.percent)
