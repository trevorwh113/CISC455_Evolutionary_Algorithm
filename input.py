import math
import random 

import numpy as np

def generate_map_simple(n, m, save_to_file=False):
    # returns nxm matrix with random locations of empty space (0), roads (-1) and buildings (-2)
    # equal prob for each location

    rng = np.random.default_rng()
    matrix = rng.integers(low=-2, high=1, size=(n, m)).astype(object)

    return matrix

def generate_map(n, m, road_perc=0.2, buildings_perc=0.9, save_to_file=False):
    # returns nxm matrix with random locations of empty space (0), roads (-1) and buildings (-2)
    
    # start by generating matrix of all 0s
    matrix = np.full((n,m),0,dtype=object)
    print(matrix, type(matrix), n, m)

    # have some number of roads? generate horizontal then vertical 
    # roads cant be in adjacent rows/cols, 
    num_roads_n = math.floor(n*road_perc)
    num_roads_m = math.floor(m*road_perc)
    print(num_roads_n,num_roads_m)

    # generate roads - rows
    invalid_rows = set()
    for i in range(num_roads_n):
        # replace 0s in a ranom row with -1s
        valid_rows = [i for i in range(n) if i not in invalid_rows]
        loc_i = random.choice(valid_rows)
        matrix[loc_i] = np.array([-1] * m)

        print(loc_i, invalid_rows)

        # ensure this & neighbouring rows will not be selected on next loop
        invalid_rows.add(loc_i)
        if loc_i > 0:
            invalid_rows.add(loc_i-1)
        if loc_i < n - 1:
            invalid_rows.add(loc_i+1)
    
    # generate roads - cols
    invalid_cols = set()
    for i in range(num_roads_m):
        valid_cols = [i for i in range(m) if i not in invalid_cols]
        loc_i = random.choice(valid_cols)

        # loop through matrix to replace values in col
        for j in range(n):
            matrix[j][loc_i] = -1

        # ensure this & neighbouring cols will not be selected on next loop
        invalid_cols.add(loc_i)
        if loc_i > 0:
            invalid_cols.add(loc_i-1)
        if loc_i < m - 1:
            invalid_cols.add(loc_i+1)

    building_generation_1(n,m, matrix, invalid_rows, invalid_cols, buildings_perc)

    return generate_map_simple(n, m)

def building_generation_1(n, m, matrix, invalid_rows, invalid_cols, buildings_perc):
    # n, m = dimensions of matrix
    # matrix = map with existing roads but no buildings
    # invalid_rows, invalid_cols: lists of row and column indices that are invalid bc roads
    # adds buildings to given matrix in random spots not containing roads 

    valid_rows = [i for i in range(n) if i not in invalid_rows]
    invalid_rows = [i for i in range(m) if i not in invalid_cols]

    num_buildings = math.floor(len(valid_rows)*len(invalid_rows)*buildings_perc)
    print(num_buildings)
    for i in range(num_buildings+1):
        r = random.choice(valid_rows)
        c = random.choice(invalid_rows)
        matrix[r][c] = -2

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
