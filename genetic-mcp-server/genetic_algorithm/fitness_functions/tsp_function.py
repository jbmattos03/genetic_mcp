from typing import Dict, Optional, Any
import random

import sys
sys.path.append("fitness_functions")  # Adjust the path to import from the parent directory
from fitness_functions.fitness_function import FitnessFunction
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
        
        : param fields: A dictionary containing 'cities' and 'distance_matrix'.
        """
        super().__init__(fields)
        logger.debug(f"Initializing TravelingSalesmanFitnessFunction with fields: {fields}")

        # Validate required keys
        if not all(key in fields for key in ["cities", "distance_matrix"]) or not all(isinstance(fields[key], list) for key in ["cities", "distance_matrix"]):
            raise ValueError("Fields must contain 'cities' and 'distance_matrix' as lists.")
        
        # Ensure distance_matrix is a square matrix
        if not all(len(row) == len(fields["cities"]) for row in fields["distance_matrix"]):
            raise ValueError("Distance matrix must be a square matrix with the same number of rows and columns as the number of cities.")
        
        # Ensure distance_matrix has the same number of rows and columns as the number of cities
        if len(fields["distance_matrix"]) != len(fields["cities"]):
            raise ValueError("Distance matrix must have the same number of rows and columns as the number of cities.")
        
        self.cities = fields["cities"]
        self.distance_matrix = fields["distance_matrix"]

    def generate_gene(self, index: Optional[int] = None, value: Optional[int] = None) -> Gene:
        """
        Generate a gene.

        :param index (optional): An optional index for the gene.
        :param value (optional): An optional value for the gene.
        :return: A generated Gene object.
        """
        logger.debug("Generating gene")
        if value:
            logger.debug(f"Using provided value: {value}")
            return Gene(value)
        
        # If no value is provided, randomly select a city from the list of cities
        if not self.cities:
            logger.error("Cities list is empty. Cannot generate gene.")
            raise ValueError("Cities list is empty. Cannot generate gene.")
        
        gene = Gene(random.choice(self.cities))
        logger.debug(f"Generated gene with value: {gene.value}")

        return gene

    def generate_chromosome(self, chromosome_size: int) -> Chromosome:
        """
        Generate a chromosome.

        :param chromosome_size: The size of the chromosome to generate.
        :return: A generated Chromosome object.
        """
        logger.debug(f"Generating chromosome of size: {chromosome_size}")
        if not self.cities:
            raise ValueError("Cities list is empty. Cannot generate chromosome.")

        aux = []
        current_cities = self.cities[:]
        for _ in range(chromosome_size):
            city = random.choice(current_cities)
            current_cities.remove(city)
            aux.append(self.generate_gene(value=city))

        chromosome = Chromosome(
            size=chromosome_size,
            genes=aux
        )
        logger.debug(f"Generated chromosome: {[gene.value for gene in chromosome.genes]}")

        return chromosome

    def generate_population(self, size: int, chromosome_size: int) -> Population:
        """
        Generate a population.

        :param size: The population size.
        :param chromosome_size: The chromosome size.
        :return: A Population object containing the generated chromosomes.
        """
        logger.debug(f"Generating population with size: {size} with chromosome size: {chromosome_size}")
        aux = []
        valid_flag = False

        for _ in range(size):
            while not valid_flag:
                chromosome = self.generate_chromosome(chromosome_size)
                if chromosome in aux:
                    logger.debug(f"Chromosome already exists in population, generating a new one.")
                    continue
                # Ensure the chromosome has unique cities
                if len(set(gene.value for gene in chromosome.genes)) != len(chromosome.genes):
                    logger.debug(f"Chromosome has duplicate cities, generating a new one.")
                    continue

                # Add the chromosome to the population if it is valid
                valid_flag = True

            aux.append(chromosome)
            logger.debug(f"Generated chromosome: {[gene.value for gene in chromosome.genes]}")
        
        population = Population(
            size=size,
            chromosomes=aux
        )
        logger.debug(f"Generated population with {len(population.chromosomes)} chromosomes.")
        logger.debug(f"Population chromosomes: {[ [gene.value for gene in chromosome.genes] for chromosome in population.chromosomes]}")

        return population

    def calculate_fitness(self, chromosome: Chromosome) -> float:
        """
        Calculate the fitness of a given chromosome.

        :param chromosome: The chromosome for which to calculate fitness.
        :return: The fitness value of the chromosome.
        """
        logger.debug(f"Calculating fitness for chromosome: {chromosome}")
        if not chromosome.genes or len(chromosome.genes) != len(self.cities):
            raise ValueError("Chromosome genes must match the number of cities.")
        
        total_distance = 0
        for i in range(len(chromosome.genes)):
            city_from = chromosome.genes[i].value
            city_to = chromosome.genes[(i + 1) % len(chromosome.genes)].value
            logger.debug(f"Calculating distance from {city_from} to {city_to}")

            # Validate that the cities exist in the distance matrix
            if city_from not in self.cities or city_to not in self.cities:
                raise ValueError(f"City {city_from} or {city_to} not found in cities list.")
            
            distance = self.distance_matrix[self.cities.index(city_from)][self.cities.index(city_to)]
            total_distance += distance
            logger.debug(f"Current total distance: {total_distance}")
        logger.debug(f"Total distance for chromosome: {total_distance}")

        # The fitness is the inverse of the total distance (lower distance = higher fitness)
        fitness = 1 / total_distance if total_distance > 0 else float('inf')

        chromosome.fitness = fitness
        logger.debug(f"Calculated fitness: {fitness} for chromosome: {[gene.value for gene in chromosome.genes]}")

        return fitness