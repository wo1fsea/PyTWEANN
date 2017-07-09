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

import random

from .neuron_network import NeuronNetwork


class Gene(object):
    """
    Connect Gene
    """

    def __init__(self):
        self.from_node = 0
        self.to_node = 0
        self.weight = 0
        self.enable = True

    @staticmethod
    def generate_innovation(from_node, to_node):
        return "%d-%d" % (from_node, to_node)

    @property
    def innovation(self):
        return self.generate_innovation(self.from_node, self.to_node)

    def copy(self):
        new_gene = Gene()
        new_gene.from_node = self.from_node
        new_gene.to_node = self.to_node
        new_gene.weight = self.weight
        new_gene.enable = self.enable

        return new_gene


class Genome(object):
    def __init__(self, environment, init_with_full_connection=False):
        self.environment = environment

        self.genes = []

        self._fitness = 0

        self.global_rank = 0

        self.neuron_network = None

        config = self.environment.config

        self.input_size = config["input_size"]
        self.output_size = config["output_size"]
        self.hidden_size = 0

        self.mutation_rates = {
            "weight": config["weight_mutation_chance"],
            "bias": config["bias_mutation_chance"],
            "link": config["link_mutation_chance"],
            "node": config["node_mutation_chance"],
            "enable": config["enable_mutation_chance"],
            "disable": config["disable_mutation_chance"],
            "step_size": config["step_size"],
        }

        for i in range(self.input_size):
            for j in range(self.output_size):
                from_node = i + 1
                to_node = self.input_size + j

                new_gene = Gene()
                new_gene.from_node = from_node
                new_gene.to_node = to_node
                new_gene.weight = self.random_weight()

                self.genes.append(new_gene)

    @staticmethod
    def random_weight():
        return random.random() * 4 - 2

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        if not self.environment.best_genome or self.environment.best_genome.fitness < value:
            self.environment.best_genome = self
        self._fitness = value

    def disjoint(self, genome):
        innovation1 = set([gene.innovation for gene in self.genes])
        innovation2 = set([gene.innovation for gene in genome.genes])
        disjoint = innovation1.symmetric_difference(innovation2)
        return len(disjoint) / max(len(self.genes), len(genome.genes), 1)

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

        return weight_sum / matching if matching else 0

    def distance(self, genome):
        config = self.environment.config
        return config["lambda_disjoint"] * self.disjoint(genome) + config["lambda_weights"] * self.weight_difference(
            genome)

    def weight_mutate(self):
        step_size = self.mutation_rates["step_size"]
        perturb_chance = self.environment.config["perturb_chance"]
        for gene in self.genes:
            if random.random() < perturb_chance:
                gene.weight = gene.weight + random.random() * 2 * step_size - step_size
            else:
                gene.weight = self.random_weight()

    def random_node(self, input_excluded=False):
        start_index = self.input_size + 1 if input_excluded else 0
        nodes = range(start_index, self.input_size + self.output_size + self.hidden_size + 1)
        return random.choice(nodes)

    def contains_link(self, from_node, to_node):
        return any(map(lambda gene: gene.from_node == from_node and gene.to_node == to_node, self.genes))

    def link_mutate(self, is_bias):
        from_node = self.random_node(False) if not is_bias else 0
        to_node = self.random_node(True)

        if self.environment.config["feed_forward"]:
            if from_node == to_node:
                return

            from_node, to_node = min(from_node, to_node), max(from_node, to_node)
            if self.input_size + 1 <= from_node < self.input_size + self.output_size + 1 < to_node:
                from_node, to_node = to_node, from_node

        innovation = Gene.generate_innovation(from_node, to_node)
        if any(map(lambda x: x.innovation == innovation, self.genes)):
            return

        new_gene = Gene()
        new_gene.from_node = from_node
        new_gene.to_node = to_node
        new_gene.weight = self.random_weight()

        self.genes.append(new_gene)

    def node_mutate(self):
        if not self.genes:
            return

        gene = random.choice(self.genes)
        if not gene.enable:
            return

        gene1 = gene.copy()
        gene1.to_node = self.input_size + self.output_size + self.hidden_size + 1
        gene1.weight = 1
        self.genes.append(gene1)

        gene2 = gene.copy()
        gene2.from_node = self.input_size + self.output_size + self.hidden_size + 1
        self.genes.append(gene2)

        gene.enable = False

        self.hidden_size += 1

    def enable_disable_mutate(self, enable):
        candidates = list(filter(lambda x: x.enable == enable, self.genes))

        if not candidates:
            return

        gene = random.choice(candidates)
        gene.enable = not gene.enable

    def mutation_rates_mutate(self):
        for mutation, rate in self.mutation_rates.items():
            if random.randint(0, 1):
                self.mutation_rates[mutation] *= 0.95
            else:
                self.mutation_rates[mutation] *= 1.05263

    def mutate(self):
        self.neuron_network = None

        self.mutation_rates_mutate()

        # problems
        if random.random() < self.mutation_rates["weight"]:
            self.weight_mutate()

        p = self.mutation_rates["link"]
        while p > 0:
            if random.random() < p:
                self.link_mutate(False)
            p -= 1

        p = self.mutation_rates["bias"]
        while p > 0:
            if random.random() < p:
                self.link_mutate(True)
            p -= 1

        p = self.mutation_rates["node"]
        while p > 0:
            if random.random() < p:
                self.node_mutate()
            p -= 1

        p = self.mutation_rates["disable"]
        while p > 0:
            if random.random() < p:
                self.enable_disable_mutate(False)
            p -= 1

        p = self.mutation_rates["enable"]
        while p > 0:
            if random.random() < p:
                self.enable_disable_mutate(True)
            p -= 1

    def crossover(self, genome):
        if self.fitness < genome.fitness:
            return genome.crossover(self)

        innovation1 = dict([(gene.innovation, gene) for gene in self.genes])
        innovation2 = dict([(gene.innovation, gene) for gene in genome.genes])

        child = Genome(self.environment)
        for innovation, gene1 in innovation1.items():
            gene2 = innovation2.get(innovation)
            if gene2 and gene2.enable and random.randint(0, 1):
                child.genes.append(gene2)
            else:
                child.genes.append(gene1)

        child.hidden_size = self.hidden_size
        child.mutation_rates = dict(self.mutation_rates)

        return child

    def copy(self):
        new_genome = Genome(self.environment)

        new_genome.genes = [gene.copy() for gene in self.genes]

        new_genome.fitness = self.fitness

        new_genome.neuron_network = None
        new_genome.hidden_size = self.hidden_size

        new_genome.mutation_rates = dict(self.mutation_rates)
        return new_genome

    def get_neuron_network(self):
        if not self.neuron_network:
            self.neuron_network = NeuronNetwork.create_with_genome(self)
        return self.neuron_network
