# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/6/19
Description:
    genome.py
----------------------------------------------------------------------------"""


class Gene(object):
    def __init__(self):
        self._from = 0
        self._to = 0
        self._weight = 0
        self._functioning = True

        self._innovation = 0

    def copy(self):
        new_gene = Gene()
        new_gene._from = self._from
        new_gene._to = self._to
        new_gene._weight = self._weight
        new_gene._functioning = self._functioning

        self._innovation = self._innovation

        return new_gene

    @property
    def from_node(self):
        return self._from

    @property
    def to_node(self):
        return self._to

    @property
    def weight(self):
        return self._weight

    @property
    def functioning(self):
        return self._functioning

    @property
    def innovation(self):
        return self._innovation


class Genome(object):
    def __init__(self):
        self.genes = []

        self.fitness = 0
        self.adjusted_fitness = 0

        self.neuron_networks = []
        self.max_neuron = 0

        self.mutation_rates = {
            "weight": 0,
            "bias": 0,
            "link": 0,
            "node": 0,
            "functioning": 0,
        }

    def weight_mutate(self, step):
        pass

    def link_mutate(self, is_bias):
        pass

    def node_mutate(self):
        pass

    def function_mutate(self):
        pass

    def mutate(self):
        pass
