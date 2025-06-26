from typing import List
from gene import Gene

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
    
