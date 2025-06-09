from mcp.server.fastmcp import FastMCP
from typing import Any, List, Optional, Dict, Callable
import random

# Create a server
mcp = FastMCP("genetic-mcp-server")

# ------- Adding tools -------
# Tool: maximize_fitness
@mcp.tool("maximize_fitness")
def maximize_fitness(population_size: Optional[int], chromosome_size: int, max_sum: int, fitness_function: Dict[str, Any]) -> Dict[str, float]:
    """
    A tool that maximizes the fitness of a genetic algorithm.
    """

    # ----- Validation -----
    # Check if population_size is provided, if not, set it to a default value
    if population_size is None:
        population_size = 1000

    # Validate chromosome_size and max_sum
    if chromosome_size <= 0 or max_sum <= 0:
        raise ValueError("chromosome_size and max_sum must be positive integers.")
    
    # Validate fitness_function
    if not Dict.isinstance(fitness_function):
        raise ValueError("fitness_function must be a dictionary") # TODO: check if keys "weights" and "values" are present
    
    # ----- Genetic Algorithm Logic -----

    return 

# Add a dynamic greeting resource
@mcp.resource("/greeting://{name}")
def greeting(name: str):
    """
    A simple greeting resource that returns a greeting message.
    """
    return f"Hello, {name}! Welcome to the Genetic MCP Server."