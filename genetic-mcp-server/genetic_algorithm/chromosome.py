from typing import List, Optional

from gene import Gene
from fitness_function import FitnessFunction

class Chromosome:
    """
    A class to represent a chromosome in a genetic algorithm.
    """

    def __init__(self, size: int, genes: List[Gene]):
        """
        Initialize a chromosome with a given size and optional genes.
        
        :param size: The size of the chromosome.
        :param genes: Optional list of genes to initialize the chromosome with.
        """
        if size <= 0:
            raise ValueError("Chromosome size must be greater than 0.")
        
        self.size = size
        self.genes = genes
        self.fitness = 0

    def __getitem__(self, index: int) -> Gene:
        """
        Get a gene at a specific index.
        
        :param index: The index of the gene to retrieve.
        :return: The gene at the specified index.
        """
        return self.genes[index]
    
    def __setitem__(self, index: int, value: Gene):
        """
        Set a gene at a specific index.
        
        :param index: The index of the gene to set.
        :param value: The gene to set at the specified index.
        """
        if not isinstance(value, Gene):
            raise TypeError("Value must be an instance of Gene.")
        self.genes[index] = value
    
