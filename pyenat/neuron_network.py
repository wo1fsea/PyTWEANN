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

    def add_incoming(self, from_node, weight):
        self.incoming_link[from_node] = weight


class NeuronNetwork(object):
    def __init__(self):
        self.input_size = 0
        self.output_size = 0
        self.hidden_size = 0

        self.activate_order = None

        self.activation_function = sigmoid

        self.neurons = []

    def activate(self, inputs):
        assert len(inputs) == self.input_size, "wrong input data size."

        self.neurons[0].value = 1

        for i, data in enumerate(inputs):
            self.neurons[i + 1].value = data

        if self.activate_order is None:
            self.activate_order = self._gen_activate_order()

        for index in self.activate_order:
            neuron = self.neurons[index]
            self.activate_neuron(neuron)

        return tuple(map(lambda x: x.value, self.neurons[self.input_size + 1:self.input_size + self.output_size + 1]))

    def activate_neuron(self, neuron):
        if neuron.incoming_link:
            value = 0
            for i, weight in neuron.incoming_link.items():
                value += self.neurons[i].value * weight
            neuron.value = self.activation_function(value)

    def _get_requested_neurons(self):
        output_neurons = list(range(self.input_size + 1, self.input_size + self.output_size + 1))
        requested_neurons = {}
        for index in output_neurons:
            requested_neurons[index] = tuple(self.neurons[index].incoming_link.keys())

        while True:
            new_requested_neurons = {}
            for index in requested_neurons:
                for incoming_index in self.neurons[index].incoming_link:
                    if incoming_index not in requested_neurons:
                        new_requested_neurons[incoming_index] = tuple(self.neurons[incoming_index].incoming_link.keys())
            if not new_requested_neurons:
                break
            else:
                requested_neurons.update(new_requested_neurons)

        return requested_neurons

    def _gen_activate_order(self):
        activate_order = []
        passed_neurons = set(range(self.input_size + 1))
        requested_neurons = self._get_requested_neurons()
        output_neurons = [node for node in range(self.input_size + 1, self.input_size + 1 + self.output_size)]

        while True:
            min_num = len(requested_neurons)
            min_idx = -1
            for index, incoming_indexes in requested_neurons.items():
                if index in passed_neurons or index in output_neurons:
                    continue

                num = len(tuple(filter(lambda idx: idx not in passed_neurons, incoming_indexes)))
                if num <= min_num:
                    min_num = num
                    min_idx = index

                    if num == 0:
                        activate_order.append(index)
                        passed_neurons.add(index)
                    else:
                        break

            if min_num == len(requested_neurons):
                break

            if min_num != 0:
                activate_order.append(min_idx)
                passed_neurons.add(min_idx)

        for index in output_neurons:
            activate_order.append(index)

        return activate_order

    @staticmethod
    def create_with_genome(genome):
        neuron_network = NeuronNetwork()

        neuron_network.input_size = genome.input_size
        neuron_network.output_size = genome.output_size
        neuron_network.hidden_size = genome.hidden_size

        for i in range(neuron_network.input_size + neuron_network.output_size + neuron_network.hidden_size + 1):
            neuron_network.neurons.append(Neuron())

        for gene in genome.genes:
            if gene.enable:
                neuron_network.neurons[gene.to_node].add_incoming(gene.from_node, gene.weight)

        return neuron_network
