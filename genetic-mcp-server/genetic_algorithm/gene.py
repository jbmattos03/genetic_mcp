from typing import List, Optional
import random

from fitness_function import FitnessFunction

class Gene:
    """
    A class to represent a gene in a genetic algorithm.
    """
    def __init__(self, value: Optional[int] = None):
        """
        Initialize a gene with a given value.
        
        :param value: The value of the gene.
        """
        if value is None:
            raise ValueError("Gene value cannot be None.")
        self.value = value