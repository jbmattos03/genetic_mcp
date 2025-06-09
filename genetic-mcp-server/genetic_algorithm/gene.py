from typing import List, Optional
import random

from fitness_function import FitnessFunction

class Gene:
    """
    A class to represent a gene in a genetic algorithm.
    """
    def __init__(self, value: Optional[int] = None, fitness_function: Optional[FitnessFunction] = None):
        """
        Initialize a gene with a given value.
        
        :param value: The value of the gene. If None, a random value will be assigned.
        """
        if value is None:
            self.value = self.random_value(fitness_function)
        else:
            self.value = value
    
    def random_value(self, fitness_function: Optional[FitnessFunction] = None) -> float:
        """
        Generate a random value for the gene based on the fitness function.
        
        :param fitness_function: An optional fitness function to guide the random value generation.
        :return: A random integer value.
        """
        if fitness_function and fitness_function.fields:
            # If a fitness function is provided, use its values to generate a random value
            return random.choice(fitness_function.values)
        else:
            # Default random value generation if no fitness function is provided
            return float(random.randint(0, 1))