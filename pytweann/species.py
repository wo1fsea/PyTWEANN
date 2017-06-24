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

	def breedChild(self):
		config = self.environment.config
		if random.random() < config["crossover_chance"]:
			g1, g2 = random.sample(self.genomes, 2)
			child = g1.crossover(g2)
		else:
			child = random.choice(self.genomes).copy()

		return child

	def cull(self, remain_num=None):
		if remain_num is None:
			remain_num = len(self.genomes) / 2
		self.genomes.sort(key=lambda x: x.fitness, reverse=True)
		self.genomes = self.genomes[:remain_num]
