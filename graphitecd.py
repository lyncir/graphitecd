# -*- coding: utf8 -*-

import sys
import time
import traceback
from daemon import Daemon

from app import settings
from app import logger


config = settings.get_config()


def importName(modulename, name):
    try:
        module = __import__(modulename, globals(), locals(), [name])
    except ImportError:
        return None
    return getattr(module, name)


class GraphitecdDaemon(Daemon):
    def run(self):
        while True:
            try:
                for extname in config['collectors']['enabled']:
                    CollectorClass = importName("app.collectors." + extname, 'Collector')
                    collector = CollectorClass()
                    collector.collect()
            except:
                logger.error(traceback.format_exc())
                sys.exit(2)
            time.sleep(10)


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

