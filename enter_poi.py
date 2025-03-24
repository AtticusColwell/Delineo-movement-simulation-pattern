import random

def enter_poi(people, pois, current_time, hagerstown_pop):
    move_probability, distribution = pois.generate_distribution(current_time, hagerstown_pop)
    move_probability_with_tendency, distributions_with_tendency = pois.generate_distributions_with_tendency(current_time, hagerstown_pop)
    for person_id, person in people.items():
        if person.curr_poi == "":
            next_poi_id = pois.get_next_poi(move_probability, distribution)
        else:
            curr_poi_index = pois.poi_id_to_index[person.curr_poi]
            next_poi_id = pois.get_next_poi(move_probability_with_tendency[curr_poi_index], distributions_with_tendency[curr_poi_index])
        if next_poi_id is not None:
            pois.enter(next_poi_id)
            person.visit(next_poi_id)