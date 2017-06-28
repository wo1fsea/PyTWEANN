# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/6/25
Description:
    main.py
----------------------------------------------------------------------------"""

import pyenat.pyenat
import random

XOR = [[1, 0, 1], [1, 1, 0], [0, 0, 0], [0, 1, 1]]
AND = [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, -1]]

XOR_Sample = []
for i in range(4):
    XOR_Sample.extend(XOR)

random.shuffle(XOR_Sample)

XOR_test = []
XOR_test.extend(XOR)

random.shuffle(XOR_test)


def main():
    environment = pyenat.pyenat.create_environment(input_size=2, output_size=1)
    while True:
        for genome in environment.get_genomes():
            fitness = 0
            neuron_network = genome.get_neuron_network()
            for data in XOR_Sample:
                output = neuron_network.evaluate(data[:-1])[0]
                fitness += 1 - (output - data[-1]) ** 2
            genome.fitness = fitness
            c = 0
            if genome.fitness > 15.5:
                print("get")
        environment.new_generation()


if __name__ == '__main__':
    main()
