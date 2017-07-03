# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/6/29
Description:
    test_neuron_network.py
----------------------------------------------------------------------------"""

import unittest
from pyenat.neuron_network import NeuronNetwork, Neuron


class TestNeuronNetwork(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_neuron_network(self):
        """
        test neuron_network
        test case
        input: n0 = 1, n1 = 1, n2 = 2
        output: n3 = activation_function(1. * n5), n4 = activation_function(2. * n5)
        hidden: n5 = activation_function(0.1 * n0 + 1. * n1 + 10. * n2 + 100. * n3 + 1000. * n4)

        :return:
        """

        neron_network = NeuronNetwork()
        neron_network.input_size = 2
        neron_network.output_size = 2
        neron_network.hidden_size = 1

        for i in range(neron_network.input_size + neron_network.output_size + neron_network.hidden_size + 1):
            neron_network.neurons.append(Neuron())

        neron_network.neurons[5].incoming_link[0] = 0.1
        neron_network.neurons[5].incoming_link[1] = 1.
        neron_network.neurons[5].incoming_link[2] = 10.
        neron_network.neurons[5].incoming_link[3] = 100.
        neron_network.neurons[5].incoming_link[4] = 1000.

        neron_network.neurons[3].incoming_link[5] = 1.
        neron_network.neurons[4].incoming_link[5] = 2.

        def activation_function(x): return x ** 2

        neron_network.activation_function = activation_function

        input_data = [1, 1, 2]
        n3 = 0
        n4 = 0
        n5 = activation_function(
            0.1 * input_data[0] + 1. * input_data[1] + 10. * input_data[2] + 100. * n3 + 1000. * n4)
        n3 = activation_function(1. * n5)
        n4 = activation_function(2. * n5)
        self.assertSequenceEqual(neron_network.activate(input_data[1:]), [n3, n4])
        n5 = activation_function(
            0.1 * input_data[0] + 1. * input_data[1] + 10. * input_data[2] + 100. * n3 + 1000. * n4)
        n3 = activation_function(1. * n5)
        n4 = activation_function(2. * n5)
        self.assertSequenceEqual(neron_network.activate(input_data[1:]), [n3, n4])

    def test_neuron_network_with_genome(self):
        """
        test neuron_network
        test case
        input: n0 = 1, n1 = 1, n2 = 2
        output: n3 = activation_function(1. * n5), n4 = activation_function(2. * n5)
        hidden: n5 = activation_function(0.1 * n0 + 1. * n1 + 10. * n2 + 100. * n3 + 1000. * n4)

        :return:
        """
        from pyenat.config import new_config
        from pyenat.environment import Environment
        from pyenat.genome import Genome, Gene

        config = new_config()
        config["input_size"] = 2
        config["output_size"] = 2

        environment = Environment(config)
        genome = Genome(environment)
        genome.hidden_size = 1

        l53 = Gene()
        l53.from_node = 5
        l53.to_node = 3
        l53.weight = 1.
        l53.enable = True
        genome.genes.append(l53)

        l54 = Gene()
        l54.from_node = 5
        l54.to_node = 4
        l54.weight = 2.
        l54.enable = True
        genome.genes.append(l54)

        l05 = Gene()
        l05.from_node = 0
        l05.to_node = 5
        l05.weight = 0.1
        l05.enable = True
        genome.genes.append(l05)

        l15 = Gene()
        l15.from_node = 1
        l15.to_node = 5
        l15.weight = 1.
        l15.enable = True
        genome.genes.append(l15)

        l25 = Gene()
        l25.from_node = 2
        l25.to_node = 5
        l25.weight = 10.
        l25.enable = True
        genome.genes.append(l25)

        l35 = Gene()
        l35.from_node = 3
        l35.to_node = 5
        l35.weight = 100.
        l35.enable = True
        genome.genes.append(l35)

        l45 = Gene()
        l45.from_node = 4
        l45.to_node = 5
        l45.weight = 1000.
        l45.enable = True
        genome.genes.append(l45)

        def activation_function(x): return x ** 2

        neron_network = genome.get_neuron_network()
        neron_network.activation_function = activation_function

        input_data = [1, 1, 2]
        n3 = 0
        n4 = 0
        n5 = activation_function(
            0.1 * input_data[0] + 1. * input_data[1] + 10. * input_data[2] + 100. * n3 + 1000. * n4)
        n3 = activation_function(1. * n5)
        n4 = activation_function(2. * n5)
        self.assertSequenceEqual(neron_network.activate(input_data[1:]), [n3, n4])
        n5 = activation_function(
            0.1 * input_data[0] + 1. * input_data[1] + 10. * input_data[2] + 100. * n3 + 1000. * n4)
        n3 = activation_function(1. * n5)
        n4 = activation_function(2. * n5)
        self.assertSequenceEqual(neron_network.activate(input_data[1:]), [n3, n4])
