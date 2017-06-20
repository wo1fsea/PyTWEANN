# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/6/19
Description:
    pytweann.py
----------------------------------------------------------------------------"""

from . import config

class Environment(object):
    def __int__(self):
        pass

class PyTWEANN(object):
    def __init__(self, **kwargs):
        self.config = config.new_config()

        for k, v in kwargs:
            assert k in self.config, "Parameter key %s is not in config." % k
            self.config[k] = v

        self.environment = []

    def