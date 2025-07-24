from typing import Dict, Optional, Any

import sys
sys.path.append("fitness_functions")
from fitness_functions.fitness_function import FitnessFunction
from chromosome import Chromosome
from gene import Gene
from population import Population

from logger import logger_config
logger = logger_config(process_name="fitness_function", pretty=True)

class VehicleRoutingFitnessFunction(FitnessFunction):
    """
    A fitness function for the vehicle routing problem.
    """
    def __init__(self, fields: Dict[str, Any]):
        """
        Initialize the vehicle routing fitness function.

        :param fields: A dictionary containing 'depot', 'client_demands', 'vehicle_capacity', 'distance_matrix' lists
        """
        super().__init__(fields)
        logger.debug(f"Initializing TravelingSalesmanFitnessFunction with fields: {fields}")

        # Validate required keys
        required_keys = ["vehicle_capacity", "client_demands", "distance_matrix"]
        if not all(key in fields for key in required_keys + ["depot"]) or not all(isinstance(fields[key], list) for key in required_keys):
            raise ValueError("Fields must contain 'cities' and 'distance_matrix' as lists.")
        
        if not isinstance(fields["depot"], (int, list)):
            raise ValueError("Depot must be an integer or a list representing the depot location(s).")
        
        # Ensure distance_matrix is a square matrix
        if not all(len(row) == len(fields["client_demands"]) for row in fields["distance_matrix"]):
            raise ValueError("Distance matrix must be a square matrix with the same number of rows and columns as the number of clients.")
        
        # Ensure distance_matrix has the same number of rows and columns as the number of cities
        if len(fields["distance_matrix"]) != len(fields["cities"]):
            raise ValueError("Distance matrix must have the same number of rows and columns as the number of cities.")
        
        self.client_demands = fields["client_demands"]
        self.vehicle_capacity = fields["vehicle_capacity"]
        self.depot = fields["depot"]
        self.distance_matrix = fields["distance_matrix"]
    
    def generate_gene(self, index: Optional[int] = None, value: Optional[float] = None) -> Gene:
        """
        Generate a gene for the vehicle routing problem.

        :param index: An optional index for the gene.
        :param value: An optional value for the gene.
        :return: A Gene object representing the generated gene.
        """
        pass

    def generate_chromosome(self, chromosome_size: int) -> Chromosome:
        """
        Generate a random chromosome for the vehicle routing problem.

        :param chromosome_size: The size of the chromosome to generate.
        :return: A Chromosome object representing the generated chromosome.
        """
        pass

    def generate_population(self, size: int, chromosome_size: int) -> Population:
        """
        Generate a population of chromosomes for the vehicle routing problem.

        :param size: The number of chromosomes in the population.
        :param chromosome_size: The size of each chromosome.
        :return: A Population object containing the generated chromosomes.
        """
        pass

    def calculate_fitness(self, chromosome: Chromosome) -> float:
        """
        Calculate the fitness of a vehicle routing chromosome.

        :param chromosome: The chromosome representing the vehicle routing solution.
        :return: The fitness value of the chromosome.
        """
        pass