from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

from chromosome import Chromosome
from gene import Gene
from population import Population

# Implement an interface for fitness functions
class FitnessFunction(ABC):
    """
    A class to represent a fitness function for a genetic algorithm.
    """
    def __init__(self, fields: Dict[str, Any]):
        """
        Initialize the fitness function with the required fields.
        
        :param fields: A list of dictionaries representing the fields required by the fitness function.
        """
        self.fields = fields
        if not self.fields:
            raise ValueError("Fitness function must have at least one field.")

    @abstractmethod
    def generate_gene(self, index: Optional[int] = None, value: Optional[float] = None) -> Gene:
        """
        Generate a gene based on the fitness function's requirements.

        :param Optional[float] value: An optional value for the gene.
        :return: A Gene object representing the generated gene.
        """
        pass

    @abstractmethod
    def generate_chromosome(self) -> Chromosome:
        """
        Generate a chromosome based on the fitness function's requirements.
        
        :return: A Chromosome object representing the generated chromosome.
        """
        pass
        
    @abstractmethod
    def calculate_fitness(self, chromosome: Any) -> float:
        """
        Calculate the fitness of a given chromosome.
        
        :param chromosome: The chromosome for which to calculate fitness.
        :return: The fitness value of the chromosome.
        """
        pass

    @abstractmethod
    def generate_population(self, size: int, chromosome_size: int) -> Population:
        """
        Generate a population of chromosomes based on the fitness function's requirements.
        
        :param size: The number of chromosomes in the population.
        :param chromosome_size: The size of each chromosome.
        :return: A list of chromosomes.
        """
        pass
    



