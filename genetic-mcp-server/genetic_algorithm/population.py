from typing import List, Optional
from chromosome import Chromosome

class Population:
    """
    A class to represent a population in a genetic algorithm.
    """

    def __init__(self, size: int, chromosomes: List[Chromosome]):
        """
        Initialize a population with a given size and chromosome size.
        
        :param size: The number of chromosomes in the population.
        :param chromosome_size: The size of each chromosome.
        :param fitness_function: An optional fitness function to guide the population initialization.
        """
        if size <= 0:
            raise ValueError("Population size must be greater than 0.")
        self.size = size
        self.chromosomes = chromosomes
        if not self.chromosomes or len(self.chromosomes) < 1:
            raise ValueError("Population must have at least one chromosome.")