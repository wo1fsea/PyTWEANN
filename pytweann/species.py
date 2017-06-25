# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/6/20
Description:
    species.py
----------------------------------------------------------------------------"""

import random


class Species(object):
    def __init__(self, environment, genome):
        self.environment = environment
        self.genomes = [genome]

        self.staleness = 0
        self.best_fitness = 0
        self.average_fitness = 0

    def breed_child(self):
        config = self.environment.config
        if random.random() < config["crossover_chance"] and len(self.genomes) > 1:
            g1, g2 = random.sample(self.genomes, 2)
            child = g1.crossover(g2)
        else:
            child = random.choice(self.genomes).copy()

        child.mutate()

        return child

    def cull(self, remain_num=None):
        if remain_num is None:
            remain_num = int(max(len(self.genomes) / 2, 1))
        self.genomes.sort(key=lambda x: x.fitness, reverse=True)
        self.genomes = self.genomes[:remain_num]

    def try_add(self, genome):
        can_add = self.genomes[0].distance(genome) < self.environment.config["delta_threshold"]
        if can_add:
            self.genomes.append(genome)
        return can_add

    def renew_best_fitness(self):
        last_best_fitness = self.best_fitness
        self.best_fitness = max(self.genomes, key=lambda x: x.fitness).fitness
        return self.best_fitness > last_best_fitness
