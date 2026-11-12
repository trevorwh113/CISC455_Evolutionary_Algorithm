import random 

from input import get_empty_locations_from_map

# map = matrix of roads & 
def initialize_individual(possible_locations, max_cans, min_cans):
    # possible locations = list of possible coordinates for cans in [i,j] form
    # max_cans = maximum number of trash cans we can have
    # min_cans = minimum number of trash cans we can have

    # returns individual: list of coordinatesin in form [i,j]

    individual = []

    num_cans = random.randint(min_cans, max_cans)
    
    # create copy of possible locations to avoid repeats by removing locations as they are added to individual  
    mutate_locs = possible_locations.copy()

    # randomly select from list of possible locations, removing them to avoid repeats
    for i in range(num_cans):
        loc_i = random.randint(0, len(mutate_locs)-1)
        individual.append(mutate_locs[loc_i])
        mutate_locs.pop(loc_i)

    return individual


def initialize_population(mu, map, max_cans=None, min_cans=None):
    # mu = population size
    # map = NxM matrix of roads & buildings
    # max_cans, min_cans = (optional) configure maximum or minimum number of cans

    # return population: list of lists of coordinates in in form [i,j]

    permissable_locs = get_empty_locations_from_map(map)
    population = []

    max = max_cans
    if not max or max > len(permissable_locs):
        max = len(permissable_locs)
    
    min = min_cans
    if not min or min < 0:
        min = 1

    for i in range(mu):
        population.append(initialize_individual(permissable_locs, max, min))

    return population

def print_population(population):
    print("POPULATION:")
    for i in range(len(population)):
        print(population[i])
