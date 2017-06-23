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
    """
    Connect Gene
    """

    def __init__(self):
        self.from_node = 0
        self.to_node = 0
        self.weight = 0
        self.enable = True

        self.innovation = 0

    def copy(self):
        new_gene = Gene()
        new_gene.from_node = self.from_node
        new_gene.to_node = self.to_node
        new_gene.weight = self.weight
        new_gene.enable = self.enable

        new_gene.innovation = self.innovation

        return new_gene


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
            "enable": 0,
        }

    def disjoint(self, genome):
        innovation1 = set([gene.innovation for gene in self.genes])
        innovation2 = set([gene.innovation for gene in genome.genes])
        disjoint = innovation1.symmetric_difference(innovation2)
        return len(disjoint) / max(len(self.genes), len(genome.genes))

    def weight_difference(self, genome):
        # innovation1 = dict([(gene.innovation, gene) for gene in self.genes])
        innovation2 = dict([(gene.innovation, gene) for gene in genome.genes])

        weight_sum = 0
        matching = 0

        for gene in self.genes:
            gene2 = innovation2.get(gene.innovation)
            if gene2:
                weight_sum += abs(gene.weight - gene2.weight)
                matching += 1

        return weight_sum / matching

    def distance(self, genome):
        return 0

    def weight_mutate(self, step):
        pass

    def link_mutate(self, is_bias):
        pass

    def node_mutate(self):
        pass

    def enable_mutate(self):
        pass

    def mutate(self):
        pass
