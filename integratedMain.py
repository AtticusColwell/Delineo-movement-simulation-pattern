from datetime import datetime, timedelta
import random
import json

from preprocess_data import preprocess_csv
from person import Person
from pois import POIs
from enter_poi import enter_poi
from leave_poi import leave_poi
from draw_plot import draw_plot

import pandas as pd
import matplotlib.pyplot as plt

def main(file_path, start_time, simulation_duration, alpha, occupancy_weight, tendency_decay):
    # Process CSV Data
    print("Parsing the CSV file...")
    pois_dict = preprocess_csv(file_path)

    # Create POIs with all parameters
    pois = POIs(pois_dict, alpha=alpha, occupancy_weight=occupancy_weight, tendency_decay=tendency_decay)
    print(f"Parsed {len(pois_dict)} POIs. Using alpha={alpha}, occupancy_weight={occupancy_weight}, tendency_decay={tendency_decay}")

    # Load persons from papdata.json instead of generating them
    with open('./input/papdata.json', 'r', encoding='utf-8') as f:
        papdata = json.load(f)

    people = {}
    for person_id, person_info in papdata["people"].items():
        person = Person()
        # Set attributes based on papdata.json structure
        person.sex = person_info.get("sex")
        person.age = person_info.get("age")
        person.home = person_info.get("home")
        # Convert person_id to int (if needed) or keep as string based on your Person class implementation
        people[int(person_id)] = person

    print(f"Created {len(people)} Person instances from papdata.json.")

    # Create DataFrame for result showing
    df = pd.DataFrame(columns=pois.pois)

    '''
    For result tracking:
    '''
    person_1 = list(people.keys())[0]
    person_1_path = []

    # Run algorithm
    for hour in range(simulation_duration):
        current_time = start_time + timedelta(hours=hour)
        print(f"Simulating hour {hour + 1}/{simulation_duration} at {current_time}...")
        leave_poi(people, current_time, pois)
        # Use the actual number of persons from papdata.json
        enter_poi(people, pois, current_time, len(people))

        '''
        For result logging:
        '''
        capacities = pois.get_capacities_by_time(current_time)
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
    print("Person 1 path:", person_1_path)

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

    # Run the main function using settings from setting.txt
    with open('setting.txt', 'r') as f:
        town_name = f.readline().strip()
        # population is no longer used as we load persons from papdata.json
        _ = f.readline().strip()  # skip population line
        start_time_str = f.readline().strip()
        simulation_duration = int(f.readline().strip())
        
        # Default values if not specified in settings
        alpha = 0.16557695315916893
        occupancy_weight = 1.5711109677337263
        tendency_decay = 0.3460627088857086
        
    main(f'./input/{town_name}.csv', 
         datetime.fromisoformat(start_time_str), 
         simulation_duration, 
         alpha,
         occupancy_weight,
         tendency_decay)
         
    end_time_execution = time.time()
    print(f"Total execution time: {end_time_execution - start_time_execution:.2f} seconds")
