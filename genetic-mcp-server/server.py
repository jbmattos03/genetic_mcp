from mcp.server.fastmcp import FastMCP
from typing import Any, Dict

import sys
sys.path.append("genetic_algorithm")
from genetic_algorithm.main import main as genetic_algorithm_main

# Create a server
mcp = FastMCP("genetic-mcp-server")

# ------- Adding tools -------
# Tool: knapsack problem
@mcp.tool(description="Solve a knapsack problem using a genetic algorithm.")
async def knapsack_problem(
    population_size: int = 1000,
    chromosome_size: int = 10,
    generations: int = 100,
    fitness_function: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    A tool to solve the knapsack problem using a genetic algorithm.

    Parameters:
        population_size (int): Number of individuals in the population.
      chromosome_size (int): Number of genes in each chromosome.
        generations (int): Number of generations to run.
        fitness_function (dict): Knapsack problem parameters:
            - cities (list of strings): Name of each city.
            - distance_matrix (list of lists (matrix) of numbers): Distance between all the cities.

    Example:
        knapsack_problem(
            population_size=100,
            chromosome_size=5,
            generations=75,
            fitness_function={
                "capacity": [5, 4, 3, 2, 1],
                "weight": [2, 3, 4, 5, 7],
                "value": [40, 50, 60, 80, 100],
                "max_weight": 50
            }
        )

    """
    if not isinstance(population_size, int) or population_size <= 0:
        raise ValueError("Population size must be a positive integer.")
    if not isinstance(chromosome_size, int) or chromosome_size <= 0:
        raise ValueError("Chromosome size must be a positive integer.")
    if not fitness_function or not isinstance(fitness_function, dict):
        raise ValueError("Fitness function parameters must be provided.")
    
    options = {
        "population_size": population_size,
        "chromosome_size": chromosome_size,
        "fitness_function": fitness_function,  # Mandatory field for fitness function parameters
    }
    
    # Run the genetic algorithm for the knapsack problem
    result = genetic_algorithm_main(options=options, problem="knapsack", generations=generations)
    return result

# Tool: traveling salesman problem
@mcp.tool(description="Solve a traveling salesman problem using a genetic algorithm.")
async def traveling_salesman_problem(
    population_size: int = 1000,
    chromosome_size: int = 10,
    generations: int = 100,
    fitness_function: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Solves the traveling salesman problem using a genetic algorithm.

    Parameters:
        population_size (int): Number of individuals in the population.
        chromosome_size (int): Number of genes in each chromosome.
        generations (int): Number of generations to run.
        fitness_function (dict): Knapsack problem parameters:
            - capacity (list of numbers): Capacity of each item.
            - weight (list of numbers): Weight of each item.
            - value (list of numbers): Value of each item.
            - max_weight (number): Maximum total weight allowed.

    Example:
        knapsack_problem(
            population_size=100,
            chromosome_size=5,
            generations=75,
            fitness_function={
                "cities": ["A", "B", "C", "D", "E"],
                "distance_matrix": [
                    [0, 10, 20, 30, 40],
                    [10, 0, 20, 30, 40],
                    [10, 20, 0, 30, 40],
                    [10, 20, 30, 0, 40]
                    [10, 20, 30, 40, 0]
                ]
            }
        )
    """
    if not isinstance(population_size, int) or population_size <= 0:
        raise ValueError("Population size must be a positive integer.")
    if not isinstance(chromosome_size, int) or chromosome_size <= 0:
        raise ValueError("Chromosome size must be a positive integer.")
    if not fitness_function or not isinstance(fitness_function, dict):
        raise ValueError("Fitness function parameters must be provided.")
    
    options = {
        "population_size": population_size,
        "chromosome_size": chromosome_size,
        "fitness_function": fitness_function,  # Mandatory field for fitness function parameters
    }
    
    # Run the genetic algorithm for the traveling salesman problem
    result = genetic_algorithm_main(options=options, problem="traveling_salesman", generations=generations)
    return result

# Add a dynamic greeting resource
@mcp.resource("/greeting://{name}")
def greeting(name: str):
    """
    A simple greeting resource that returns a greeting message.
    """
    return f"Hello, {name}! Welcome to the Genetic MCP Server."

if __name__ == "__main__":
    # Start the server
    mcp.run()