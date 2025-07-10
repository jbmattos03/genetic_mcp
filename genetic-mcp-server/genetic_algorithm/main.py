from typing import Dict, Any, Optional
import json
import sys
from math import factorial

from gen_alg import GeneticAlgorithm
from logger import logger_config

from fitness_functions.knapsack_function import KnapsackFitnessFunction
from fitness_functions.tsp_function import TravelingSalesmanFitnessFunction
from fitness_functions.vrp_function import VehicleRoutingFitnessFunction

logger = logger_config(process_name="genetic_algorithm_main", pretty=True)

def main(
        options: Optional[Dict[str, Any]] = None, 
        problem: Optional[str] = "knapsack",
        generations: Optional[int] = 100
) -> Dict[str, Any]:
    """
    Main function to run the genetic algorithm for a specified problem.

    :param options: A dictionary of options to configure the genetic algorithm.
    :param problem: The problem to solve. Default is "knapsack".
    """
    logger.info("Starting the genetic algorithm with options: %s", options)

    population_size = int(options.get("population_size", 1000))
    chromosome_size = int(options.get("chromosome_size", 10))
    generations = int(generations)

    ff_arg = options.get("fitness_function")  # Mandatory field for fitness function parameters
    if ff_arg is None:
        logger.error("Fitness function parameters must be provided.")
        raise ValueError("Fitness function parameters must be provided.")

    # Initialize the fitness function based on the problem type
    if problem == "knapsack":
        fitness_function = KnapsackFitnessFunction(ff_arg)
        logger.info("Using KnapsackFitnessFunction with parameters: %s", ff_arg)
    elif problem == "vehicle_routing":
        fitness_function = VehicleRoutingFitnessFunction(ff_arg)
        logger.info("Using VehicleRoutingFitnessFunction with parameters: %s", ff_arg)
    elif problem == "traveling_salesman":
        fitness_function = TravelingSalesmanFitnessFunction(ff_arg)
        logger.info("Using TravelingSalesmanFitnessFunction with parameters: %s", ff_arg)

        # Check if population size is leq (chromosome_size!), which is the max size of permutations of chromosome_size
        max_pop = factorial(chromosome_size)
        if population_size > (max_pop):
            raise ValueError(f"Population size must not exceed {chromosome_size}! ({max_pop}) for this problem.")
    else:
        logger.error(f"Unknown problem type: {problem}")
        raise ValueError(f"Unknown problem type: {problem}")

    # Initialize and run the genetic algorithm
    ga = GeneticAlgorithm(
        population_size=population_size,
        chromosome_size=chromosome_size,
        fitness_function=fitness_function,
        problem=problem,
    )

    result = ga.run(generations=generations)
    if problem == "knapsack":
        result.update({
            "max_weight": fitness_function.max_weight,
            "weight": result["best_chromosome"].weight,
        })
    elif problem == "traveling_salesman":
        result.update({
            "distance": result["best_chromosome"].distance,
        })

    # Log the result in a readable format
    log = ""
    for key in result:
        if key == "best_chromosome":
            result[key] = [g.value for g in result[key].genes]
        log += f"{key.capitalize().replace('_', ' ')}: {result[key]} "
    log += "\n"
    logger.info(f"{log}")

    return result
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        logger.info(f"Loading problem data from file: {file_name}")
        with open(file_name, "r") as file:
            tsp_data = json.load(file)
    else:
        logger.info("No file provided. Using default problem data.")
        tsp_data = {
            "options": {
                "population_size": 100,
                "chromosome_size": 4,
                "fitness_function": {
                    "cities": ["A", "B", "C", "D"],
                    "distance_matrix": [
                        [0, 10, 15, 20],
                        [10, 0, 35, 25],
                        [15, 35, 0, 30],
                        [20, 25, 30, 0]
                    ]
                }
            },
            "problem": "traveling_salesman",
            "generations": 50
        }
    
    options = tsp_data.get("options", {})
    problem = tsp_data.get("problem", "traveling_salesman")
    generations = tsp_data.get("generations", 100)
    
    main(options=options, problem=problem, generations=generations)