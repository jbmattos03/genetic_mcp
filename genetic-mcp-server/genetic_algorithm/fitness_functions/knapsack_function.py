from typing import Dict, Optional, Any
import random

from fitness_function import FitnessFunction
from chromosome import Chromosome
from gene import Gene
from population import Population

from logger import logger_config
logger = logger_config(process_name="fitness_function", pretty=True)

class KnapsackFitnessFunction(FitnessFunction):
    """
    A fitness function for the knapsack problem.
    """
    def __init__(self, fields: Dict[str, Any]):
        """
        Initialize the knapsack fitness function.

        :param fields: A dictionary containing 'capacity', 'weight', and 'value' lists.
        """
        if not fields:
            raise ValueError("Knapsack fitness function must have at least one field.")
        
        # Validate required keys
        required_keys = ["capacity", "weight", "value", "max_weight"]
        for key in required_keys:
            if key not in fields:
                raise ValueError(f"Missing required key '{key}' in fields.")

        # Ensure all lists are of the same length
        if not (len(fields["capacity"]) == len(fields["weight"]) == len(fields["value"])):
            raise ValueError("All lists in fields ('capacity', 'weight', 'value') must have the same length.")

        self.capacity = fields["capacity"]
        self.weight = fields["weight"]
        self.value = fields["value"]
        self.max_weight = fields.get("max_weight", sum(self.capacity))  # Default max weight if not provided

        super().__init__(fields)

    def generate_gene(self, index: Optional[int] = None, value: Optional[float] = None) -> Gene:
        """
        Generate a gene for the knapsack problem.

        :param index: An optional index for the gene.
        :param value: An optional value for the gene.
        :return: A Gene object representing the generated gene.
        """
        logger.debug(f"Generating gene with index: {index}, value: {value}")
        if value:
            logger.debug(f"Using provided value: {value}")
            return Gene(value)
        elif self.capacity is not None and isinstance(self.capacity, (int, float)):
            logger.debug(f"Using capacity value: {self.fields['capacity']}")
            return Gene(random.randint(0, self.capacity))
        elif self.fields["capacity"] is not None and isinstance(self.capacity, list):
            if index is None or index >= len(self.fields["capacity"]):
                logger.error(f"Index {index} is out of range for capacity list: {self.fields['capacity']}")
                raise IndexError("Index out of range for capacity list.")
            
            logger.debug(f"Using capacity value at index {index}: {self.capacity[index]}")
            return Gene(random.randint(0, self.capacity[index]))
        else:
            logger.warning("No specific capacity or value provided, defaulting to binary gene.")
            return Gene(random.randint(0, 1)) # Default to binary gene

    def generate_chromosome(self, chromosome_size: int) -> Chromosome:
        """
        Generate a random chromosome for the knapsack problem.

        :param chromosome_size: The size of the chromosome to generate.
        :return: A Chromosome object representing the generated chromosome.
        """
        logger.debug(f"Generating chromosome of size: {chromosome_size}")
        chromosome = Chromosome(size=chromosome_size, genes=[])

        success_flag = False
        while not success_flag:
            logger.debug("Generating genes for the chromosome.")
            genes = [self.generate_gene(index=i) for i in range(chromosome_size)]
            
            total_weight = sum(genes[i].value * self.weight[i] for i in range(len(genes)))
            if total_weight <= self.max_weight:
                logger.debug(f"Generated genes: {[gene.value for gene in genes]}, Total weight: {total_weight}")
                success_flag = True
                chromosome.genes = genes
            
        return chromosome
    
    def generate_population(self, size: int, chromosome_size: int) -> Population:
        """
        Generate a population of chromosomes for the knapsack problem.

        :param size: The number of chromosomes in the population.
        :param chromosome_size: The size of each chromosome.
        :return: A Population object containing the generated chromosomes.
        """
        logger.debug(f"Generating population of size: {size} with chromosome size: {chromosome_size}")
        chromosomes = []

        for _ in range(size):
            genes = [self.generate_gene(index=i) for i in range(chromosome_size)]
            chromosome = Chromosome(size=chromosome_size, genes=genes)

            # Validate chromosome weight against max_weight
            total_weight = sum(gene.value * self.weight[i] for i, gene in enumerate(chromosome.genes))
            if total_weight <= self.max_weight:
                chromosomes.append(chromosome)
            else:
                logger.debug(f"Chromosome exceeds max weight: {total_weight}. Skipping.")

        if not chromosomes:
            raise ValueError("Population must have at least one chromosome.")

        return Population(size=size, chromosomes=chromosomes)

    def calculate_fitness(self, chromosome: Chromosome) -> float:
        """
        Calculate the fitness of a knapsack chromosome.

        :param chromosome: The chromosome representing the knapsack solution.
        :return: The fitness value of the chromosome.
        """
        logger.debug(f"Calculating fitness for chromosome: {[g.value for g in chromosome.genes]}")
        fitness = sum(gene.value * self.value[i] for i, gene in enumerate(chromosome.genes))  # Access gene.value
        logger.debug(f"Calculated fitness: {fitness} for chromosome: {[g.value for g in chromosome.genes]}")

        return fitness