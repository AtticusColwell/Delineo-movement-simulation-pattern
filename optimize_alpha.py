import numpy as np
from scipy.optimize import differential_evolution
from accuracy import calculate_metrics
from datetime import datetime
import os
from main import main

def objective_function(params, simulation_function):
    """
    Multi-objective function that combines different metrics.
    
    Args:
        params: [alpha, occupancy_weight, tendency_decay]
        simulation_function: Function that runs simulation with given parameters
    """
    alpha, occupancy_weight, tendency_decay = params
    
    # Run simulation
    metrics = simulation_function(alpha, occupancy_weight, tendency_decay)
    
    # Combine multiple metrics with weights
    combined_score = (
        0.4 * metrics['mean_squared_error'] +  # MSE weight
        0.3 * (1 - metrics['correlation']) +    # Correlation weight (1 - corr because we minimize)
        0.3 * metrics['peak_error']            # Peak timing error weight
    )
    
    return combined_score

def optimize_parameters(simulation_function):
    """
    Optimize parameters using differential evolution.
    """
    # Parameter bounds
    bounds = [
        (0.001, 1.0),     # alpha
        (0.1, 2.0),       # occupancy_weight
        (0.1, 0.9)        # tendency_decay
    ]
    
    # Run differential evolution
    result = differential_evolution(
        objective_function,
        bounds,
        args=(simulation_function,),
        maxiter=20,
        popsize=10,
        mutation=(0.5, 1.0),
        recombination=0.7
    )
    
    return result.x, result.fun

def run_simulation_with_params(alpha, occupancy_weight, tendency_decay):
    """
    Run simulation with specific parameters and return metrics.
    """
    # Clear previous output files
    if os.path.exists('output/capacity_occupancy.csv'):
        os.remove('output/capacity_occupancy.csv')
    
    # Read settings
    with open('setting.txt', 'r') as f:
        town_name = f.readline().strip()
        population = int(f.readline().strip())
        start_time = f.readline().strip()
        simulation_duration = int(f.readline().strip())
    
    # Run simulation
    main(
        f'./input/{town_name}.csv',
        population,
        datetime.fromisoformat(start_time),
        simulation_duration,
        alpha,
        occupancy_weight,
        tendency_decay
    )
    
    return calculate_metrics('output/capacity_occupancy.csv')

if __name__ == "__main__":
    # Find optimal parameters
    optimal_params, best_score = optimize_parameters(run_simulation_with_params)
    
    print(f"Optimization Results:")
    print(f"Optimal alpha: {optimal_params[0]:.6f}")
    print(f"Optimal occupancy_weight: {optimal_params[1]:.6f}")
    print(f"Optimal tendency_decay: {optimal_params[2]:.6f}")
    print(f"Best combined score: {best_score:.6f}") 