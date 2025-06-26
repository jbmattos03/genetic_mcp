from typing import Dict, Optional, Any
import random

from fitness_function import FitnessFunction
from chromosome import Chromosome
from gene import Gene
from population import Population

from logger import logger_config
logger = logger_config(process_name="fitness_function", pretty=True)

class TravelingSalesmanFitnessFunction(FitnessFunction):
    """
    A fitness function for the traveling salesman problem.
    """
    def __init__(self, fields: Dict[str, Any]):
        """
        Initialize the Traveling Salesman fitness function.

        : param fields: A dictionary containing 'cities'.
        """
        if not fields:
            raise ValueError("Traveling salesman function requires at least one field.")
        
        required_keys = ["cities"]
        for key in fields:
            if key not in required_keys:
                raise ValueError(f"Missing required key '{key}' in fields.")

    def generate_gene(self, index: Optional[int] = None, value: Optional[int] = None) -> Gene:
        """
        Generate a gene.

        :param index:
        :param value:
        :return: A generated Gene object.
        """
        pass

    def generate_chromosome(self, chromsosome_size: int) -> Chromosome:
        """
        Generate a chromosome.

        :param chromosome_size: 
        """
        pass

    def generate_population(self, size: int, chromosome_size: int) -> Population:
        """
        Generate a population.

        :param size: The population size.
        :param chromosome_size: The chromosome size.
        """
        pass

    def calculate_fitness(self, chromosome: Chromosome) -> float:
        """
        """
        pass