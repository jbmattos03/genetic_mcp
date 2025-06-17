from typing import Dict, Any, Optional

from gen_alg import GeneticAlgorithm
from logger import logger_config

from fitness_function import KnapsackFitnessFunction, VehicleRoutingFitnessFunction

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
    ff_arg = options.get("fitness_function")  # Mandatory field for fitness function parameters
    if ff_arg is None:
        logger.error("Fitness function parameters must be provided.")
        raise ValueError("Fitness function parameters must be provided.")

    # Initialize the fitness function based on the problem type
    if problem == "knapsack":
        fitness_function = KnapsackFitnessFunction(ff_arg)
        logger.info("Using KnapsackFitnessFunction with parameters: %s", ff_arg)
    elif problem == "vehicle_routing":
        from fitness_function import VehicleRoutingFitnessFunction
        fitness_function = VehicleRoutingFitnessFunction(ff_arg)
        logger.info("Using VehicleRoutingFitnessFunction with parameters: %s", ff_arg)
    else:
        logger.error(f"Unknown problem type: {problem}")
        raise ValueError(f"Unknown problem type: {problem}")

    # Initialize and run the genetic algorithm
    ga = GeneticAlgorithm(
        population_size=population_size,
        chromosome_size=chromosome_size,
        fitness_function=fitness_function,
    )

    generations = int(generations)
    result = ga.run(generations=generations)
    logger.info("Genetic algorithm completed. Best solution: %s", result)

    return result
        
if __name__ == "__main__":
    main(
        {
            "population_size": 1000,
            "chromosome_size": 10,
            "fitness_function": {
                    "capacity": [5, 4, 3, 2, 1, 6, 2, 3, 4, 5],
                    "weight": [2, 3, 4, 5, 7, 1, 6, 4.5, 3.5, 2.5],
                    "value": [40, 50, 65, 80, 110, 15, 90, 70, 60, 55],
                    "max_weight": 50
            }
        }
    )