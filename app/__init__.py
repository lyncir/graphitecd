#! -*- coding: utf8 -*-

import os 
import logging
from logging import handlers

import settings

cfg = settings.get_config()

log_file = os.path.join(settings._basedir, cfg['default']['log_file'])
log_format = "[%(asctime)s] %(levelname)s - %(message)s"
handler = handlers.TimedRotatingFileHandler(log_file,
                                            when='midnight',
                                            interval=1,
                                            backupCount=0)
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

logger = logging.getLogger('graphitecd')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
