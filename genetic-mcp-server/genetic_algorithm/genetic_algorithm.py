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
        self.population = fitness_function.generate_population(population_size, chromosome_size)

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
        self.best_fitness = float("-inf") # Initialize best fitness to negative infinity

    def evaluate_fitness(self):
        """
        Evaluate the fitness of each chromosome in the population.
        """
        pass
    
    def select_best_chromosome(self) -> Chromosome:
        """
        Select the best chromosome from the population based on fitness.
        
        :return: The chromosome with the highest fitness.
        """
        self.best_chromosome = max(self.population.chromosomes, key=lambda c: c.fitness)
        
        if self.best_chromosome.fitness > self.best_fitness:
            self.best_fitness = self.best_chromosome.fitness

        return self.best_chromosome

    def select_parents(self, method: str = "roulette") -> List[Chromosome]:
        """
        Select parents for crossover based on their fitness.
        
        :param method: The selection method to use ('roulette', 'tournament', etc.).
        :return: A list of selected parent chromosomes.
        """
        if method == "roulette":
            return self.roulette_selection()
        elif method == "tournament":
            return self.tournament_selection()
        else:
            raise ValueError(f"Unknown selection method: {method}")
        
    def roulette_selection(self) -> List[Chromosome]:
        """
        Select parents using roulette wheel selection.
        
        :return: A list of selected parent chromosomes.
        """
        pass

    def tournament_selection(self, tournament_size: int = 3) -> List[Chromosome]:
        """
        Select parents using tournament selection.
        
        :param tournament_size: The number of chromosomes to include in each tournament.
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

    def mutate(self, chromosome: Chromosome, attempts: int = 5):
        """
        Mutate a chromosome by randomly changing one of its genes.
        
        :param chromosome: The chromosome to mutate.
        """
        for index, gene in enumerate(chromosome.genes):
            if random.random() < self.mutation_rate:
                # Replace the gene with a new random gene
                chromosome.genes[index] = Gene(fitness_function=self.fitness_function)

    def run(self, generations: int):
        """
        Run the genetic algorithm for a specified number of generations.
        
        :param generations: The number of generations to run the algorithm.
        """
        pass