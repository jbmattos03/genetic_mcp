from typing import List, Optional
import random

from fitness_functions.fitness_function import FitnessFunction
from chromosome import Chromosome
from gene import Gene
from logger import logger_config

logger = logger_config(process_name="genetic_algorithm", pretty=True)

class GeneticAlgorithm:
    """
    A class to represent a genetic algorithm.
    """

    def __init__(
            self, 
            population_size: int, 
            chromosome_size: int, 
            fitness_function: FitnessFunction = None, 
            mutation_rate: Optional[float] = 0.05, 
            crossover_rate: Optional[float] = 0.8,
            method: Optional[str] = "roulette",
            problem: Optional[str] = "knapsack"
    ):
        """
        Initialize the genetic algorithm with a population of chromosomes.

        :param population_size: The number of chromosomes in the population.
        :param chromosome_size: The size of each chromosome.
        :param fitness_function: An optional fitness function to guide the evolution process.
        :param mutation_rate (optional): The mutation rate for the algorithm.
        :param crossover_rate (optional): The crossover rate for the algorithm.
        :param method (optional): Parent selection method. Can be either "roulette" or "tournament". Default is "roulette".
        :param problem (optional): Type of problem to be solved. Can be either "traveling_salesman", "knapsack" or "vehicle_routing".
        """
        # Initialize the population with the specified size and chromosome size
        self.population = fitness_function.generate_population(population_size, chromosome_size)

        # Set the fitness function, mutation rate, and crossover rate
        if fitness_function == None:
            raise ValueError("A fitness function must be provided.")
        if not (0 <= mutation_rate <= 1):
            raise ValueError("Mutation rate must be between 0 and 1.")
        if not (0 <= crossover_rate <= 1):
            raise ValueError("Crossover rate must be between 0 and 1.")
        
        # Initialize the genetic algorithm parameters
        self.problem = problem
        self.method = method.lower() if method else "roulette"
        self.fitness_function = fitness_function
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        # Initialize generation count and best chromosome
        self.generation = 0
        self.best_chromosome = None
        self.best_fitness = float("-inf") # Initialize best fitness to negative infinity

    def evaluate_fitness(self):
        """
        Evaluate the fitness of all chromosomes in the population.
        """
        for chromosome in self.population.chromosomes:
            chromosome.fitness = self.fitness_function.calculate_fitness(chromosome)
            gene_genes = [gene.value for gene in chromosome.genes]  # Extract gene genes
            logger.debug(f"Chromosome {gene_genes} fitness: {chromosome.fitness}")
    
    def select_best_chromosome(self) -> Chromosome:
        """
        Select the best chromosome from the population based on fitness.

        :return: The best chromosome in the population.
        """
        if not self.population.chromosomes:
            logger.error("Population is empty. Cannot select the best chromosome.")
            return None

        self.best_chromosome = max(self.population.chromosomes, key=lambda c: c.fitness, default=None)
        if self.best_chromosome:
            gene_genes = [gene.value for gene in self.best_chromosome.genes]  # Extract gene genes
            logger.debug(f"Best chromosome: {gene_genes} with fitness: {self.best_chromosome.fitness}")
            
            if self.best_chromosome.fitness > self.best_fitness:
                self.best_fitness = self.best_chromosome.fitness
                logger.info(f"New best fitness found: {self.best_fitness} in generation {self.generation}")
        else:
            logger.warning("No valid chromosome found in the population.")
            return

        return self.best_chromosome

    def select_parents(self, method: Optional[str] = "roulette", parent_proportion: Optional[float] = 0.8) -> List[Chromosome]:
        """
        Select parents for crossover based on their fitness.
        
        :param method (optional): The selection method to use ('roulette', 'tournament', etc.). Default is 'roulette'.
        :param parent_proportion (optional): The ratio between parents and population. Default is 0.8.
        :return: A list of selected parent chromosomes.
        """
        if method == "roulette":
            logger.info("Using roulette wheel selection for parent selection.")
            selected = self.roulette_selection(parents=int(len(self.population.chromosomes) * parent_proportion))
        elif method == "tournament":
            logger.info("Using tournament selection for parent selection.")
            selected = self.tournament_selection(parents=int(len(self.population.chromosomes) * parent_proportion))
        else:
            logger.error(f"Unknown selection method: {method}")
            raise ValueError(f"Unknown selection method: {method}")
        
        # Verifying if all pairs contain 2 elements
        if any(len(pair) != 2 for pair in selected):
            logger.warn("Some selected pairs do not contain exactly 2 chromosomes. Dropping those pairs.")
        selected = [pair for pair in selected if len(pair) == 2]
        
        return selected

        
    def roulette_selection(self, parents: int) -> List[Chromosome]:
        """
        Select parents using roulette wheel selection.
        
        :param parents: The number of parents to select.
        :return: A list of selected parent chromosomes.
        """
        logger.info("Starting roulette wheel selection for parent selection.")

        selected = []
        current_pop = [chromosome for chromosome in self.population.chromosomes]
        logger.debug(f"Current population: {[ [g.value for g in chromosome.genes] for chromosome in current_pop ]}")
        
        total_fitness = sum([chromosome.fitness for chromosome in self.population.chromosomes])
        logger.debug(f"Total fitness of population: {total_fitness}")
        current_sum = 0

        while len(selected) < parents:
            logger.debug(f"Selecting {parents} parents, currently selected: {len(selected)}")
            random_number = random.uniform(0, total_fitness)
            
            for chromosome in current_pop:
                current_sum += chromosome.fitness

                if random_number < current_sum:
                    selected.append(chromosome)
                    current_pop.remove(chromosome) # Remove parents
                    break # Break out of for loop
                
            current_sum = 0

        # Group selected parents into pairs
        selected = [selected[i:i + 2] for i in range(0, len(selected), 2)]
        logger.debug(f"Selected parents: {[g.value for pair in selected for chromosome in pair for g in chromosome.genes]}")
    
        return selected

    def tournament_selection(self, parents: int, tournament_size: Optional[int] = 3) -> List[Chromosome]:
        """
        Select parents using tournament selection.
        
        :param parents: The number of parents to select.
        :param tournament_size (optional): The number of chromosomes to include in each tournament.
        :return: A list of selected parent chromosomes.
        """
        logger.info("Starting tournament selection for parent selection.")
        selected = []
        current_pop = [chromosome for chromosome in self.population.chromosomes]
        logger.debug(f"Current population: {[g.value for chromosome in current_pop for g in chromosome.genes]}")

        while len(selected) < parents:
            logger.debug(f"Selecting {parents} parents, currently selected: {len(selected)}")
            tournament = random.sample(current_pop, tournament_size)
            winner = max(tournament, key=lambda c: c.fitness)
            logger.debug(f"Tournament participants: {[g.value for chromosome in tournament for g in chromosome.genes]}, winner: {winner.genes} with fitness: {winner.fitness}")
            
            selected.append(winner)
            current_pop.remove(winner)

        selected = [selected[i:i + 2] for i in range(0, len(selected), 2)]
        logger.debug(f"Selected parents: {[g.value for pair in selected for chromosome in pair for g in chromosome.genes]}")

        return selected

    def crossover(self, parent1: Chromosome, parent2: Chromosome, chromosome_length: int, attempts: Optional[int] = 5) -> Chromosome:
        """
        Perform crossover between two parent chromosomes to create a new child chromosome.
        
        :param parent1: The first parent chromosome.
        :param parent2: The second parent chromosome.
        :param chromosome_length: The length of the chromosome.
        :param attempts (optional): The number of attempts to create valid offspring.
        """
        logger.info(f"Performing crossover between parents: {[g.value for g in parent1.genes]} and {[g.value for g in parent2.genes]}")
        valid_flag = False
        attempts_counter = attempts

        while valid_flag is False and attempts_counter > 0:
            attempts_counter -= 1
            logger.debug(f"Attempts remaining: {attempts_counter}")

            # Randomly select crossover points
            i = random.randint(0, parent1.size - 1)
            j = random.randint(0, parent2.size - 1)
            logger.debug(f"Selected crossover points: {i}, {j}")

            if i != j:
                max_index = max(i, j)
                min_index = min(i, j)

                offspring1 = Chromosome(genes=parent1.genes[:], size=chromosome_length)
                offspring1.genes[min_index:max_index] = parent2.genes[min_index:max_index][:]
                logger.debug(f"Offspring1 genes after crossover: {[g.value for g in offspring1.genes]}")

                offspring2 = Chromosome(genes=parent2.genes[:], size=chromosome_length)
                offspring2.genes[min_index:max_index] = parent1.genes[min_index:max_index][:]
                logger.debug(f"Offspring2 genes after crossover: {[g.value for g in offspring2.genes]}")
            else:
                offspring1 = Chromosome(genes=parent2.genes[:i]+parent1.genes[i:], size=chromosome_length)
                logger.debug(f"Offspring1 genes after crossover: {[g.value for g in offspring1.genes]}")

                offspring2 = Chromosome(genes=parent1.genes[:i]+parent2.genes[i:], size=chromosome_length)
                logger.debug(f"Offspring2 genes after crossover: {[g.value for g in offspring2.genes]}")


            # Check if the offspring are valid (i.e., their weight does not exceed the max sum)
            # and if they are not already in the population
            if self.problem == "knapsack":
                if offspring1 not in self.population.chromosomes and offspring2 not in self.population.chromosomes and \
                sum([offspring1.genes[k].value * self.fitness_function.weight[k] for k in range(chromosome_length)]) <= self.fitness_function.max_weight and \
                sum([offspring2.genes[k].value * self.fitness_function.weight[k] for k in range(chromosome_length)]) <= self.fitness_function.max_weight:
                    valid_flag = True
            # For TSP, check if the offspring are valid (i.e., they do not contain duplicate genes)
            elif self.problem == "traveling_salesman":
                if (
                    offspring1 not in self.population.chromosomes and
                    offspring2 not in self.population.chromosomes and
                    len([g.value for g in offspring1.genes]) == len(set(g.value for g in offspring1.genes)) and
                    len([g.value for g in offspring2.genes]) == len(set(g.value for g in offspring2.genes))
                ):
                    valid_flag = True
        
        if valid_flag is True:
            # Replace the parents with the offspring
            parent1.genes = offspring1.genes
            parent2.genes = offspring2.genes
        else:
            logger.warning(f"Failed to create valid offspring after {attempts} attempts. Retaining original parents: {[g.value for g in parent1.genes]} and {[g.value for g in parent2.genes]}")

    def mutate(self, chromosome: Chromosome):
        """
        Mutate a chromosome by randomly changing one of its genes.
        
        :param chromosome: The chromosome to mutate.
        """
        logger.info(f"Mutating chromosome: {[g.value for g in chromosome.genes]} in generation {self.generation}")
        for index, gene in enumerate(chromosome.genes):
            if random.random() <= self.mutation_rate:
                # Replace the gene with a new random gene
                original_value = gene.value
                logger.debug(f"Mutating gene at index {index} with original value {original_value}")

                new_gene = self.fitness_function.generate_gene(index=index)
                logger.debug(f"New gene generated with value {new_gene.value}")

                if new_gene != gene:
                    gene.value = new_gene.value

                    if self.problem == "knapsack":
                        if any(chromosome.genes == pop_chromosome.genes for pop_chromosome in self.population.chromosomes) or \
                        sum([chromosome.genes[k].value * self.fitness_function.weight[k] for k in range(chromosome.length)]) > self.fitness_function.max_weight:
                            logger.warning(f"Mutation resulted in an invalid chromosome: {[g.value for g in chromosome.genes]}. Reverting to original value.")
                            gene.value = original_value
                    elif self.problem == "traveling_salesman":
                        if any(chromosome.genes == pop_chromosome.genes for pop_chromosome in self.population.chromosomes) or \
                            len([g.value for g in chromosome.genes]) != len(set([g.value for g in chromosome.genes])): 
                                logger.warning(f"Mutation resulted in an invalid chromosome: {[g.value for g in chromosome.genes]}. Reverting to original value.")
                                gene.value = original_value

    def run(self, generations: int):
        """
        Run the genetic algorithm for a specified number of generations.
        
        :param generations: The number of generations to run the algorithm.
        :return: The best solution found after running the algorithm (dictionary with 'best_chromosome, 
        'best_fitness' and 'generation').
        """
        logger.info(f"Starting genetic algorithm for {generations} generations with method: {self.method}")
        for _ in range(generations):
            self.generation += 1
            logger.info(f"Generation {self.generation} started.")
            
            # Evaluate the fitness of the population
            self.evaluate_fitness()
            logger.debug(f"Population fitness after evaluation: {[chromosome.fitness for chromosome in self.population.chromosomes]}")

            # Select parents for crossover
            parents = self.select_parents(method=self.method)
            logger.info(f"Selected parents for crossover: {[g.value for pair in parents for chromosome in pair for g in chromosome.genes]}")

            # Perform crossover to create new chromosomes
            for parent1, parent2 in parents:
                if random.random() < self.crossover_rate:
                    logger.info(f"Performing crossover between parents: {[g.value for g in parent1.genes]} and {[g.value for g in parent2.genes]}")
                    self.crossover(parent1, parent2, chromosome_length=parent1.size)

            # Mutate the chromosomes in the population
            for chromosome in self.population.chromosomes:
                self.mutate(chromosome)

            # Select the best chromosome
            best_chromosome = self.select_best_chromosome()
            if best_chromosome:
                logger.info(f"Best chromosome in generation {self.generation}: {[g.value for g in best_chromosome.genes]} with fitness: {best_chromosome.fitness}")
            else:
                logger.warning(f"No valid chromosome found in generation {self.generation}. Continuing to next generation.")
                continue

        best = self.select_best_chromosome()
        if not best:
            logger.error("No valid solution found after running the genetic algorithm.")
            return None
        else:
            logger.info(f"Best solution found: {[g.value for g in best.genes]} with fitness: {best.fitness} after {self.generation} generations.")
            return {
                "best_chromosome": [g.value for g in best.genes],
                "best_fitness": best.fitness,
                "generation": self.generation
            }