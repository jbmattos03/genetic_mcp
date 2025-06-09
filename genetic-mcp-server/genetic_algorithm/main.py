from typing import Dict, Any, Optional

from genetic_algorithm import GeneticAlgorithm

def main(options: Optional[Dict[str, Any]] = None):
    population_size = options.get("population_size", 1000)
    chromosome_size = options.get("chromosome_size", 10)
    max_sum = options.get("max_sum", 100)
    fitness_function = options.get("fitness_function", 
                                   {
                                       "weights": [1.0], 
                                       "values": [1, 2, 3]
                                   })
    
    # Initialize the genetic algorithm
    ga = GeneticAlgorithm(population_size, chromosome_size, max_sum, fitness_function)
    ga.run()
        
if __name__ == "__main__":
    main()