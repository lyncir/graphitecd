# -*- coding: utf8 -*-

import os
from configobj import ConfigObj


_basedir = os.path.abspath(os.path.dirname(__file__))


def get_config():
    config = ConfigObj(os.path.join(_basedir, 'config.cfg'))
    return config


if __name__ == '__main__':
    print get_config()
