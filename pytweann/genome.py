# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/6/19
Description:
    genome.py
----------------------------------------------------------------------------"""

import random


class Gene(object):
	"""
	Connect Gene
	"""

	def __init__(self):
		self.from_node = 0
		self.to_node = 0
		self.weight = 0
		self.enable = True

		self.innovation = 0

	def copy(self):
		new_gene = Gene()
		new_gene.from_node = self.from_node
		new_gene.to_node = self.to_node
		new_gene.weight = self.weight
		new_gene.enable = self.enable

		new_gene.innovation = self.innovation

		return new_gene


class Genome(object):
	def __init__(self, environment):
		self.environment = environment

		self.genes = []

		self.fitness = 0
		self.adjusted_fitness = 0

		self.neuron_networks = None
		self.max_neuron = 0

		config = self.environment.config
		self.mutation_rates = {
			"weight": config["weight_mutation_chance"],
			"bias": config["bias_mutation_chance"],
			"link": config["link_mutation_chance"],
			"node": config["node_mutation_chance"],
			"enable": config["enable_mutation_chance"],
			"disable": config["disable_mutation_chance"],
			"step_size": config["step_size"],
		}

	def disjoint(self, genome):
		innovation1 = set([gene.innovation for gene in self.genes])
		innovation2 = set([gene.innovation for gene in genome.genes])
		disjoint = innovation1.symmetric_difference(innovation2)
		return len(disjoint) / max(len(self.genes), len(genome.genes))

	def weight_difference(self, genome):
		# innovation1 = dict([(gene.innovation, gene) for gene in self.genes])
		innovation2 = dict([(gene.innovation, gene) for gene in genome.genes])

		weight_sum = 0
		matching = 0

		for gene in self.genes:
			gene2 = innovation2.get(gene.innovation)
			if gene2:
				weight_sum += abs(gene.weight - gene2.weight)
				matching += 1

		return weight_sum / matching

	def distance(self, genome):
		config = self.environment.config
		return config["delta_disjoint"] * self.distance(genome) + config["delta_weights"] * self.weight_difference(
			genome) < config["delta_threshold"]

	def weight_mutate(self):
		step_size = self.mutation_rates["step_size"]
		perturb_chance = self.environment.config["perturb_chance"]
		for gene in self.genes:
			if random.random() < perturb_chance:
				gene.weight = gene.weight + random.random() * 2 * step_size - step_size
			else:
				gene.weight = random.random() * 4 - 2

	def link_mutate(self, is_bias):
		pass

	def node_mutate(self):
		pass

	def enable_disable_mutate(self, enable):
		candidates = filter(lambda x: x.enable==enable, self.genes)

		if not candidates:
			return

		gene = random.choice(candidates)
		gene.enable = not gene.enable

	def mutate(self):
		pass

	def crossover(self, genome):
		if self.fitness < genome.fitness:
			return genome.crossover(self)

		innovation1 = dict([(gene.innovation, gene) for gene in self.genes])
		innovation2 = dict([(gene.innovation, gene) for gene in genome.genes])

		self.genes = []
		for innovation, gene1 in innovation1.items():
			gene2 = innovation2.get(innovation)
			if gene2 and gene2.enable and random.randint(0, 1):
				self.genes.append(gene1)
			else:
				self.genes.append(gene2)

		child = Genome(self.environment)

		child.max_neuron = max(self.max_neuron, genome.max_neuron)
		child.mutation_rates = dict(self.mutation_rates)

		return child

	def copy(self):
		new_genome = Genome(self.environment)

		new_genome.genes = [gene.copy() for gene in self.genes]

		new_genome.fitness = self.fitness
		new_genome.adjusted_fitness = self.adjusted_fitness

		new_genome.neuron_networks = None
		new_genome.max_neuron = self.max_neuron

		new_genome.mutation_rates = dict(self.mutation_rates)
		return new_genome
