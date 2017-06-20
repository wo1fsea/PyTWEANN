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

        input_size = 0
        output_size = 0
        hidden_size = 0

        self.neurons = []

        for i in range(input_size + output_size + hidden_size):
            self.neurons.append(Neuron())

        for gene in genome.genes:
            self.neurons[gene.to_node].add_incoming(gene)

    def evaluate(self, inputs):
        for i, data in enumerate(inputs):
            self.neurons[i].value = data

        for neuron in self.neurons:
            if neuron.incoming_link:
                value = 0
                for i, weight in neuron.incoming_link.items():
                    value += self.neurons[i] * weight
                neuron.value = sigmoid(value)

        output_size = 0
        return tuple(map(lambda x: x.value, self.neurons[:-output_size]))
