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

    "population": 300,

    "delta_disjoint": 2.,
    "delta_weights": 0.4,
    "delta_threshold": 1.,

    "stale_spacies": 15,

    "weight_mutation_chance": 0.25,
    "bias_mutation_chance": 0.4,
    "link_mutation_chance": 2.0,
    "node_mutation_chance": 0.5,
    "functioning_mutation_chance": 0.4,
    "step_size": 0.1,

    "perturb_chance": 0.9,
    "crossover_chance": 0.75,

    "max_nodes_size": 1000000,
}


def new_config():
    return dict(default_config)
