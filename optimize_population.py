from datetime import datetime, timedelta
import os
from main import main
from accuracy import calculate_metrics

def optimize_population(file_path, start_population, start_time, simulation_duration, 
                       population_range=(1000, 10000), step_size=500,
                       alpha = 0.16557695315916893,
                       occupancy_weight=1.5711109677337263,
                       tendency_decay=0.3460627088857086):
    """
    Find optimal population size by running simulations and measuring accuracy.
    
    Args:
        file_path: Path to the input CSV file
        start_population: Initial population to start optimization from
        start_time: Start time for simulation
        simulation_duration: Duration of simulation in hours
        population_range: Tuple of (min_population, max_population)
        step_size: Step size for population adjustment
        alpha, occupancy_weight, tendency_decay: Simulation parameters
    
    Returns:
        dict: Contains optimal population and its corresponding metrics
    """
    best_metrics = None
    best_population = start_population
    min_pop, max_pop = population_range
    
    # Try different population sizes
    for population in range(min_pop, max_pop + 1, step_size):
        print(f"\nTesting population size: {population}")
        
        # Clear previous results
        if os.path.exists('output/capacity_occupancy.csv'):
            os.remove('output/capacity_occupancy.csv')
            
        # Run simulation with current population
        main(file_path, population, start_time, simulation_duration,
             alpha, occupancy_weight, tendency_decay)
        
        # Calculate metrics
        metrics = calculate_metrics('output/capacity_occupancy.csv')
        
        # Update best if this population gives better accuracy
        if best_metrics is None or metrics['accuracy'] > best_metrics['accuracy']:
            best_metrics = metrics
            best_population = population
            print(f"New best population found: {population} (Accuracy: {metrics['accuracy']:.2f}%)")
    
    return {
        'optimal_population': best_population,
        'metrics': best_metrics
    }

if __name__ == "__main__":
    # Read settings from file
    with open('setting.txt', 'r') as f:
        town_name = f.readline().strip()
        initial_population = int(f.readline().strip())
        start_time_str = f.readline().strip()
        simulation_duration = int(f.readline().strip())
    
    # Run optimization
    result = optimize_population(
        f'./input/{town_name}.csv',
        initial_population,
        datetime.fromisoformat(start_time_str),
        simulation_duration,
        population_range=(initial_population - 1000, initial_population + 1000),
        step_size=200
    )
    
    print("\nOptimization Results:")
    print(f"Optimal Population: {result['optimal_population']}")
    print(f"Best Accuracy: {result['metrics']['accuracy']:.2f}%")
    print(f"Mean Absolute Error: {result['metrics']['mean_absolute_error']:.4f}")
    print(f"Root Mean Squared Error: {result['metrics']['root_mean_squared_error']:.4f}") 