# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	Huang Quanyong (wo1fSea)
	quanyongh@foxmail.com
Date:
	2017/6/24
Description:
	environment
----------------------------------------------------------------------------"""


class Environment(object):
	def __init__(self, config):
		self.config = config

		self.species = {}
		self.generation = 0
		self.innovation = 0

		self.currentSpecies = 0
		self.currentGenome = 0

		self.best_genome = None

	def get_best(self):
		return self.best_genome

	def get_genomes(self):
		return [genome for species in self.species for genome in species.genomes]
