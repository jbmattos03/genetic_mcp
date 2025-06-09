from typing import List, Optional, Any, Dict
from dataclasses import dataclass

@dataclass
class FitnessFunction:
    """
    A class to represent a fitness function for a genetic algorithm.
    """
    fields: Optional[Dict[str, Any]] = None # Optional fields for additional parameters
    weights: List[float]
    values: List[Any]
