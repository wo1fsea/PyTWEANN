# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/6/19
Description:
    neuron_network.py
----------------------------------------------------------------------------"""

import math


def sigmoid(x):
    return 2 / (1 + math.exp(-4.9 * x)) - 1


class Neuron(object):
    def __init__(self):
        self.incoming_link = {}
        self.value = 0

    def add_incoming(self, gene):
        self.incoming_link[gene.from_node] = gene.weight


class NeuronNetwork(object):
    def __init__(self, genome):

        self.genome = genome

        self.input_size = self.genome.input_size
        self.output_size = self.genome.output_size
        self.hidden_size = self.genome.hidden_size

        self.neurons = []

        for i in range(self.input_size + self.output_size + self.hidden_size + 1):
            self.neurons.append(Neuron())

        for gene in genome.genes:
            if gene.enable:
                self.neurons[gene.to_node].add_incoming(gene)

    def evaluate(self, inputs):
        assert len(inputs) == self.input_size, "wrong input data size."

        self.neurons[0].value = 1

        for i, data in enumerate(inputs):
            self.neurons[i + 1].value = data

        for i in range(self.hidden_size):
            neuron = self.neurons[self.input_size + self.output_size + 1 + i]
            self.evaluate_neuron(neuron)

        for i in range(self.output_size):
            neuron = self.neurons[self.input_size + 1 + i]
            self.evaluate_neuron(neuron)

        return tuple(map(lambda x: x.value, self.neurons[self.input_size + 1:self.input_size + self.output_size + 1]))

    def evaluate_neuron(self, neuron):
        if neuron.incoming_link:
            value = 0
            for i, weight in neuron.incoming_link.items():
                value += self.neurons[i].value * weight
            neuron.value = sigmoid(value)


def main():
    from genome import Genome, Gene
    from environment import Environment
    from config import new_config
    config = new_config()
    config["input_size"] = 2
    config["output_size"] = 1
    environment = Environment(config)
    genome = Genome(environment)
    gene1 = Gene()
    gene1.from_node = 1
    gene1.to_node = 3
    gene1.weight = 1
    gene2 = Gene()
    gene2.from_node = 2
    gene2.to_node = 3
    gene2.weight = 2
    genome.genes.append(gene1)
    genome.genes.append(gene2)
    neron_network = NeuronNetwork(genome)
    print(neron_network.evaluate([1, -0.1]))


if __name__ == '__main__':
    main()
