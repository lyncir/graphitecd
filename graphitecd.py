# -*- coding: utf8 -*-
import socket
import sys
import time
import statsd

import psutil

from daemon import Daemon
from app import settings


config = settings.get_config()
hostname = socket.gethostname()

conn = statsd.Connection(config['statsd']['host'], config['statsd']['port'])
gauge = statsd.Gauge('.'.join([hostname, 'cpu']), conn)


class GraphitecdDaemon(Daemon):
    def run(self):
        while True:
            cpu_percents = psutil.cpu_percent(percpu=True)
            for i in range(len(cpu_percents)):
                value = cpu_percents[i]
                metric_path = 'cpu{}.percent'.format(i)
                # print(time.time(), metric_path, value)
                gauge.send(metric_path, value)

            time.sleep(0.5)


if __name__ == "__main__":
    daemon = GraphitecdDaemon(config['default']['pid'])
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
