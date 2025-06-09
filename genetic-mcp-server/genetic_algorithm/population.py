from typing import List, Optional

from chromosome import Chromosome
from fitness_function import FitnessFunction

class Population:
    """
    A class to represent a population in a genetic algorithm.
    """

    def __init__(self, size: int, chromosome_size: int, fitness_function: Optional[FitnessFunction] = None):
        """
        Initialize a population with a given size and chromosome size.
        
        :param size: The number of chromosomes in the population.
        :param chromosome_size: The size of each chromosome.
        :param fitness_function: An optional fitness function to guide the population initialization.
        """
        if size <= 0:
            raise ValueError("Population size must be greater than 0.")

        self.chromosomes = [Chromosome(chromosome_size, fitness_function=fitness_function) for _ in range(size)]
        self.fitness_function = fitness_function
        self.size = size

    def __getitem__(self, index: int) -> Chromosome:
        """
        Get a chromosome at a specific index.
        :param index: The index of the chromosome to retrieve.
        :return: The chromosome at the specified index.
        """
        return self.chromosomes[index]
    
    def __setitem__(self, index: int, value: Chromosome):
        """
        Set a chromosome at a specific index.
        :param index: The index of the chromosome to set.
        :param value: The chromosome to set at the specified index.
        """
        if not isinstance(value, Chromosome):
            raise TypeError("Value must be an instance of Chromosome.")
        self.chromosomes[index] = value