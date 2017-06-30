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
