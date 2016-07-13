# -*- coding: utf8 -*-

import time
import statsd
import psutil
import requests

from app import settings


config = settings.get_config()


class Collector(object):
    def __init__(self):
        self.cfg = settings.get_config()
        self.path = 'httpapi'
        self.conn = statsd.Connection(self.cfg['statsd']['host'],
                self.cfg['statsd']['port'])

    def collect(self):
        """
        Collect http api time.
        """
        t1 = time.time()
        req = requests.get('http://172.16.100.58/index.php?do=user.getNickName&uid=5016')
        t2 = time.time()

        gauge = statsd.Gauge('.'.join([self.cfg['default']['hostname'], self.path]), self.conn)
        gauge.send('get_time', round((t2 - t1), 3))
