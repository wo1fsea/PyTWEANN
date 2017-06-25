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

import pytweann.pytweann

XOR = [[1, -1, 1], [1, 1, -1], [-1, -1, 1], [-1, 1, -1]]
AND = [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, -1]]


def main():
    environment = pytweann.pytweann.create_environment(input_size=2, output_size=1)
    while True:
        for genome in environment.get_genomes():
            fitness = 0
            neuron_network = genome.get_neuron_network()
            for data in AND:
                fitness += 1 if neuron_network.evaluate(data[:-1])[0] > 0 and data[-1] > 0 else 0
            if fitness == 4:
                print("get!")

            genome.fitness = fitness
        environment.new_generation()


if __name__ == '__main__':
    main()
