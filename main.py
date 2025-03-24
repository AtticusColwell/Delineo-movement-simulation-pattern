from datetime import datetime, timedelta
import random

from preprocess_data import preprocess_csv
from person import Person
from pois import POIs
from enter_poi import enter_poi
from leave_poi import leave_poi
from draw_plot import draw_plot

import pandas as pd
import matplotlib.pyplot as plt

def main(file_path, population, start_time, simulation_duration, alpha, occupancy_weight, tendency_decay):
    # Process CSV Data
    print("Parsing the CSV file...")
    pois_dict = preprocess_csv(file_path)

    # Create POIs with all parameters
    pois = POIs(pois_dict, alpha=alpha, occupancy_weight=occupancy_weight, tendency_decay=tendency_decay)
    print(f"Parsed {len(pois_dict)} POIs. Using alpha={alpha}, occupancy_weight={occupancy_weight}, tendency_decay={tendency_decay}")

    # Create Persons
    hagerstown_pop = population
    people = {person_id: Person() for person_id in range(hagerstown_pop)}
    print(f"Created {hagerstown_pop} Person instances.")

    # Create DataFrame for result showing
    df = pd.DataFrame(columns=pois.pois)

    '''
    for result
    '''
    person_1 = list(people.keys())[0]
    person_1_path = []

    # Run algorithm
    for hour in range(simulation_duration):
        print(f"Simulating hour {hour + 1}/{simulation_duration}...", start_time + timedelta(hours=hour))
        leave_poi(people, start_time + timedelta(hours=hour), pois)
        enter_poi(people, pois, start_time + timedelta(hours=hour), hagerstown_pop)

        '''
        for result
        '''
        
        capacities = pois.get_capacities_by_time(start_time + timedelta(hours=hour))
        occupancies = pois.occupancies

        # Write capacity vs occupancy data to file
        with open('output/capacity_occupancy.csv', 'a', encoding='utf-8') as f:
            f.write(f"\nHour {hour}:\n")
            for poi_id in pois.pois:
                poi_name = pois_dict[poi_id]['location_name']
                cap = capacities[poi_id]
                occ = occupancies[poi_id]
                diff = cap - occ
                f.write(f"{poi_name},{cap:.2f},{occ},{diff:.2f}\n")

        if people[person_1].curr_poi != "":
            person_1_path.append(pois_dict[people[person_1].curr_poi]['location_name'])
        else:
            person_1_path.append("None")
        df.loc[hour] = pois.occupancies
    
    # Print the path of person 1
    print(person_1_path)

    # Save the DataFrame to a CSV file
    output_file = "output/simulation_results.csv"
    df.to_csv(output_file, index=True)
    location_names = [pois_dict[list(pois_dict.keys())[i]]['location_name'] for i in range(len(df.columns))]
    df.columns = location_names
    
    # Save df and location names to files
    df.to_csv('output/occupancy_df.csv', index=True)
    with open('output/location_names.txt', 'w', encoding='utf-8') as f:
        for location in location_names:
            f.write(f"{location}\n")


if __name__ == "__main__":
    import time
    start_time_execution = time.time()

    # Run the main function
    with open('setting.txt', 'r') as f:
        town_name = f.readline().strip()
        population = int(f.readline().strip())
        start_time = f.readline().strip()
        simulation_duration = int(f.readline().strip())
        
        # Default values if not specified in settings
        alpha = 0.16557695315916893
        occupancy_weight = 1.5711109677337263
        tendency_decay = 0.3460627088857086
        
    main(f'./input/{town_name}.csv', 
         population, 
         datetime.fromisoformat(start_time), 
         simulation_duration, 
         alpha,
         occupancy_weight,
         tendency_decay)
         
    end_time_execution = time.time()
    print(f"Total execution time: {end_time_execution - start_time_execution:.2f} seconds")
