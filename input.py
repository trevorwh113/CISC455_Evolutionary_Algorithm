import numpy as np

def generate_map_simple(n, m, save_to_file=False):
    # returns nxm matrix with random locations of empty space (0), roads (-1) and buildings (-2)
    # equal prob for each location

    rng = np.random.default_rng()
    matrix = rng.integers(low=-2, high=1, size=(n, m))
    print(matrix, type(matrix))

    return matrix

def get_empty_locations_from_map(map):
    # map = matrix of empty space (0), roads (-1) and buildings (-2)
    # returns list of possible coordinates for cans in [i,j] form

    permissable_locs = []
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i,j] == 0:
                permissable_locs.append([i,j])
    
    return permissable_locs

# def save_map_to_file(n,m,map,f_location):
