import sys

from app import logger
from app import settings


def importName(modulename, name):
    try:
        module = __import__(modulename, globals(), locals(), [name])
    except ImportError:
        return None
    return getattr(module, name)


config = settings.get_config()


for extname in config['collectors']['enabled']:
    CollectorClass = importName("app.collectors." + extname, 'Collector')
    collector = CollectorClass()
    collector.collect()
