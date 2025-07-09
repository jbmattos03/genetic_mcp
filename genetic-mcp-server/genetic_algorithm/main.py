from typing import Dict, Any, Optional
import json

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
    logger.info("Genetic algorithm completed. Best solution: %s", result)

    if problem == "knapsack":
        result.append({
            "max_weight": fitness_function.max_weight,
            "weight": sum([gene.value * fitness_function.weight[i] for i, gene in enumerate(result[0].genes)]),
        })

    return result
        
if __name__ == "__main__":
    with open("tsp.json", "r") as file:
        tsp_data = json.load(file)
    
    options = tsp_data.get("options", {})
    problem = tsp_data.get("problem", "traveling_salesman")
    generations = tsp_data.get("generations", 100)
    #print(options, problem, generations)
    
    main(options=options, problem=problem, generations=generations)