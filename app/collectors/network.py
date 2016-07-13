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
        self.path = 'network'
        self.conn = statsd.Connection(self.cfg['statsd']['host'],
                self.cfg['statsd']['port'])

    def collect(self):
        """
        Collect network interface stats.
        """
        pinc_before = psutil.net_io_counters(pernic=True)
        time.sleep(1)
        pinc_after = psutil.net_io_counters(pernic=True)

        nic_names = pinc_before.keys()
        for name in nic_names:
            stats_before = pinc_before[name]
            stats_after = pinc_after[name]
            gauge = statsd.Gauge('.'.join([self.cfg['default']['hostname'], self.path, name]), self.conn)
            gauge.send('bytes_sent', math.fabs(stats_after.bytes_sent - stats_before.bytes_sent))
            gauge.send('bytes_recv', math.fabs(stats_after.bytes_recv - stats_before.bytes_recv))
            gauge.send('packets_sent', math.fabs(stats_after.packets_sent - stats_before.packets_sent))
            gauge.send('packets_recv', math.fabs(stats_after.packets_recv - stats_before.packets_recv))
