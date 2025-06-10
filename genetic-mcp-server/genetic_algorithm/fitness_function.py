from typing import List, Any, Dict
from abc import ABC, abstractmethod
import random

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
    def generate_population(self, size: int, chromosome_size: int) -> List[Chromosome]:
        """
        Generate a population of chromosomes based on the fitness function's requirements.
        
        :param size: The number of chromosomes in the population.
        :param chromosome_size: The size of each chromosome.
        :return: A list of chromosomes.
        """
        pass

class KnapsackFitnessFunction(FitnessFunction):
    """
    A fitness function for the knapsack problem.
    """
    def __init__(self, fields: Dict[str, Any]):
        if not fields:
            raise ValueError("Knapsack fitness function must have at least one field.")
        elif not all("weight" in field and "value" in field for field in fields):
            raise ValueError("Each field must contain 'weight' and 'value' keys.")
        
        super().__init__(fields)

    def generate_chromosome(self, chromosome_size: int) -> Chromosome:
        """
        Generate a random chromosome for the knapsack problem.

        :param chromosome_size: The size of the chromosome to generate.
        :return: A Chromosome object representing the generated chromosome.
        """
        chromosome = Chromosome(size=chromosome_size, genes=[])

        for i in range(chromosome_size):
            if self.fields["capacity"] is not None and isinstance(self.fields["capacity"], (int, float)):
                chromosome.__setitem__(index=i, value=Gene(random.randint(0, self.fields["capacity"])))
            elif self.fields["capacity"] is not None and isinstance(self.fields["capacity"], list):
                chromosome.__setitem__(index=i, value=Gene(random.randint(0, self.fields["capacity"][i])))
            else:
                chromosome.__setitem__(Gene(random.randint(0, 1))) # Default to binary gene

        return chromosome
    
    def generate_population(self, size: int, chromosome_size: int) -> List[Chromosome]:
        """
        Generate a population of chromosomes for the knapsack problem.

        :param size: The number of chromosomes in the population.
        :param chromosome_size: The size of each chromosome.
        :return: A Population object containing the generated chromosomes.
        """
        population = Population(size=size, chromosomes=[])

        for i in range(size):
            success_flag = False 

            while success_flag is False:
                chromosome = self.generate_chromosome(chromosome_size)
                
                total_weight = sum(chromosome.genes.value[i] * self.fields["weight"][i] for i in range(len(chromosome.genes)))
                if total_weight <= self.fields["max_weight"]:
                    population.__setitem__(index=i, value=chromosome)
                    success_flag = True

        return population

    def calculate_fitness(self, chromosome: Any) -> float:
        """
        Calculate the fitness of a knapsack chromosome.
        
        :param chromosome: The chromosome representing the knapsack solution.
        """
        chromosome.fitness = sum(chromosome.genes.value[i] * self.fields["value"][i] for i in range(len(chromosome.genes)))  # Assuming genes are binary (0 or 1)
    
class VehicleRoutingFitnessFunction:
    """
    A fitness function for the vehicle routing problem.
    """

    
