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

import math
import random

from .species import Species
from .genome import Genome


class Environment(object):
    def __init__(self, config):
        self.config = config

        self.species = []
        self.generation = 0
        self.innovation = 0

        self.currentSpecies = 0
        self.currentGenome = 0

        self.best_genome = None

        self.population = self.config["population"]

        self._init_genomes()

    def _init_genomes(self):
        for i in range(self.population):
            genome = Genome(self)
            genome.mutate()
            self.add_to_species(genome)

    def get_best(self):
        return self.best_genome

    def get_genomes(self):
        return [genome for species in self.species for genome in species.genomes]

    def renew_global_rank(self):
        genomes = self.get_genomes()
        genomes.sort(key=lambda x: x.fitness)

        for i, genome in enumerate(genomes):
            genome.global_rank = i

    def renew_average_fitness(self):
        for i, species in enumerate(self.species):
            total = sum(map(lambda genome: genome.global_rank, species.genomes))
            species.average_fitness = total / len(species.genomes)

    def remove_stale_species(self):
        staleness_threshold = self.config["staleness_threshold"]
        best_fitness = self.best_genome.fitness if self.best_genome else 0

        for species in self.species:
            if species.renew_best_fitness():
                species.staleness = 0
            else:
                species.staleness += 1

        self.species = list(
            filter(lambda x: x.staleness < staleness_threshold or x.best_fitness >= best_fitness, self.species))

    def remove_weak_species(self):
        total_average_fitness = sum(map(lambda x: x.average_fitness, self.species))
        self.species = list(
            filter(lambda x: math.floor(x.average_fitness / total_average_fitness * self.population) >= 1,
                   self.species))

    def cull_species(self, cut_to_one):
        for species in self.species:
            species.cull(None if not cut_to_one else 1)

    def new_generation(self):
        self.cull_species(False)
        self.renew_global_rank()
        self.remove_stale_species()
        self.renew_global_rank()
        self.renew_average_fitness()
        self.remove_weak_species()

        new_genomes = []

        total_average_fitness = sum(map(lambda x: x.average_fitness, self.species))
        for species in self.species:
            breed = int(math.floor(species.average_fitness / total_average_fitness * self.population) - 1)
            for i in range(breed):
                new_genomes.append(species.breed_child())

        self.cull_species(True)

        genome_num = len(self.species) + len(new_genomes)
        assert genome_num <= self.population, "wrong population."
        for i in range(self.population - genome_num):
            species = random.choice(self.species)
            new_genomes.append(species.breed_child())

        for genome in new_genomes:
            self.add_to_species(genome)

        self.generation += 1

    def add_to_species(self, genome):
        for species in self.species:
            if species.try_add(genome):
                return

        self.species.append(Species(self, genome))
