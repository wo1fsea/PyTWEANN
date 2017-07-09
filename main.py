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

XOR = [[1, 0, 1], [1, 1, -1], [0, 0, -1], [0, 1, 1]]
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
    old_fitness = 0
    while True:
        for genome in environment.get_genomes():
            fitness = 0
            right_sum = 0
            neuron_network = genome.get_neuron_network()
            for data in XOR_Sample:
                output = neuron_network.activate(data[:-1])[0]
                fitness += 1 - ((output - data[-1]) / 2) ** 2
                right_sum += 1 if output * data[-1] > 0 else 0
            genome.fitness = fitness
            if genome.fitness > old_fitness:
                old_fitness = genome.fitness
                if right_sum == len(XOR_Sample):
                    print("get!", genome.hidden_size)
                print(old_fitness, right_sum)
        environment.new_generation()


if __name__ == '__main__':
    main()
