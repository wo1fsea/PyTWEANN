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
	def __init__(self):
		self.input_size = 0
		self.output_size = 0
		self.hidden_size = 0

		self.activate_order = None

		self.activate_function = sigmoid

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
			neuron.value = self.activate_function(value)

	# @staticmethod
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

		while True:
			min = len(requested_neurons)
			min_idx = -1
			for index, incoming_indexes in requested_neurons.items():
				if index in passed_neurons:
					continue

				num = len(tuple(filter(lambda idx: idx not in passed_neurons, incoming_indexes)))
				if num <= min:
					min = num
					min_idx = index

					if num == 0:
						activate_order.append(index)
						passed_neurons.add(index)
					else:
						break

			if min == len(requested_neurons):
				break

			if min != 0:
				activate_order.append(min_idx)
				passed_neurons.add(index)

		return activate_order

	@staticmethod
	def create_with_genome(self, genome):
		self.input_size = self.genome.input_size
		self.output_size = self.genome.output_size
		self.hidden_size = self.genome.hidden_size

		self.activate_order = []

		self.neurons = []

		for i in range(self.input_size + self.output_size + self.hidden_size + 1):
			self.neurons.append(Neuron())

		for gene in genome.genes:
			if gene.enable:
				self.neurons[gene.to_node].add_incoming(gene)


def main():
	neron_network = NeuronNetwork()
	neron_network.input_size = 2
	neron_network.output_size = 2
	neron_network.hidden_size = 1

	for i in range(neron_network.input_size + neron_network.output_size + neron_network.hidden_size + 1):
		neron_network.neurons.append(Neuron())

	neron_network.neurons[3].incoming_link[0] = 0.1
	neron_network.neurons[3].incoming_link[1] = 0.1
	neron_network.neurons[3].incoming_link[5] = 0.1

	neron_network.neurons[4].incoming_link[3] = 1

	neron_network.neurons[5].incoming_link[4] = 1

	print(neron_network.activate([1, 2]))
	print(neron_network.activate([1, 2]))


if __name__ == '__main__':
	main()
