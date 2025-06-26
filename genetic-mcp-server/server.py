from mcp.server.fastmcp import FastMCP
from typing import Any, List, Optional, Dict, Callable

import sys
sys.path.append("genetic_algorithm")
from genetic_algorithm.main import main as genetic_algorithm_main

# Create a server
mcp = FastMCP("genetic-mcp-server")

# ------- Adding tools -------
# Tool: vehicle routing problem
@mcp.tool("solve_vehicle_routing_problem")
def vehicle_routing_problem():
    """
    A tool to solve the vehicle routing problem using a genetic algorithm.
    """
    return

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