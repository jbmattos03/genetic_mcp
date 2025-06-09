from typing import List, Optional
import random

from fitness_function import FitnessFunction
from chromosome import Chromosome
from population import Population
from gene import Gene

class GeneticAlgorithm:
    """
    A class to represent a genetic algorithm.
    """

    def __init__(self, population_size: int, chromosome_size: int, fitness_function: FitnessFunction = None, mutation_rate: Optional[float] = 0.05, crossover_rate: Optional[float] = 0.8):
        """
        Initialize the genetic algorithm with a population of chromosomes.

        :param population_size: The number of chromosomes in the population.
        :param chromosome_size: The size of each chromosome.
        :param fitness_function: An optional fitness function to guide the evolution process.
        """
        # Initialize the population with the specified size and chromosome size
        self.population = Population(population_size, chromosome_size, fitness_function)

        # Set the fitness function, mutation rate, and crossover rate
        if fitness_function is None:
            raise ValueError("A fitness function must be provided.")
        if not (0 <= mutation_rate <= 1):
            raise ValueError("Mutation rate must be between 0 and 1.")
        if not (0 <= crossover_rate <= 1):
            raise ValueError("Crossover rate must be between 0 and 1.")
        
        self.fitness_function = fitness_function
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        # Initialize generation count and best chromosome
        self.generation = 0
        self.best_chromosome = None
        self.best_fitness = float('-inf')

    def evaluate_fitness(self):
        """
        Evaluate the fitness of each chromosome in the population.
        """
        pass

    def select_parents(self) -> List[Chromosome]:
        """
        Select parents for crossover based on their fitness.
        
        :return: A list of selected parent chromosomes.
        """
        pass

    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        """
        Perform crossover between two parent chromosomes to create a new child chromosome.
        
        :param parent1: The first parent chromosome.
        :param parent2: The second parent chromosome.
        :return: A new child chromosome resulting from the crossover.
        """
        pass

    def mutate(self, chromosome: Chromosome):
        """
        Mutate a chromosome by randomly changing one of its genes.
        
        :param chromosome: The chromosome to mutate.
        """
        pass

    def run(self, generations: int):
        """
        Run the genetic algorithm for a specified number of generations.
        
        :param generations: The number of generations to run the algorithm.
        """
        pass