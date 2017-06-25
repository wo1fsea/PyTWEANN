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
from . import environment


def create_environment(**kwargs):
    cfg = config.new_config()

    for k, v in kwargs.items():
        assert k in cfg, "Parameter key %s is not in config." % k
        cfg[k] = v

    return environment.Environment(cfg)
