# -*- coding: utf8 -*-

import time
import math
import statsd
import psutil

from app import settings


config = settings.get_config()


class Collector(object):
    def __init__(self):
        self.cfg = settings.get_config()
        self.path = 'diskio'
        self.conn = statsd.Connection(self.cfg['statsd']['host'],
                self.cfg['statsd']['port'])

    def collect(self):
        """
        Collect disk IO stats.
        """
        disk_before = psutil.disk_io_counters()
        time.sleep(1)
        disk_after = psutil.disk_io_counters()

        gauge = statsd.Gauge('.'.join([self.cfg['default']['hostname'], self.path]), self.conn)
        gauge.send('read_count', math.fabs(disk_after.read_count - disk_before.read_count))
        gauge.send('write_count', math.fabs(disk_after.write_count - disk_before.write_count))
        gauge.send('read_bytes', math.fabs(disk_after.read_bytes - disk_before.read_bytes))
        gauge.send('write_bytes', math.fabs(disk_after.write_bytes - disk_before.write_bytes))
