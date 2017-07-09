# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/6/19
Description:
    config.py
----------------------------------------------------------------------------"""

default_config = {
    "input_size": 1,
    "output_size": 1,

    "feed_forward": True,

    "population": 150,

    # c1 = c2
    "lambda_disjoint": 1.,
    # c3
    "lambda_weights": 3.0,

    # delta_t
    "delta_threshold": 3.,

    "staleness_threshold": 15,

    "weight_mutation_chance": 0.25,
    "bias_mutation_chance": 0.4,
    "link_mutation_chance": 0.05,
    "node_mutation_chance": 0.03,
    "enable_mutation_chance": 0.2,
    "disable_mutation_chance": 0.4,
    "step_size": 0.1,

    "perturb_chance": 0.9,
    "crossover_chance": 0.75,
}


def new_config():
    return dict(default_config)
