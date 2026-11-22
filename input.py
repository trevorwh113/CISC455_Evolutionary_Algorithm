import math
import random 

import numpy as np


def generate_map_simple(n, m):
    """
    Builds a random map of the given dimensions, with equal probability for generation of roads, 
    buildings and empty space.

    returns nxm matrix with random locations of empty space (0), roads (-1), and buildings (-2)
    """

    rng = np.random.default_rng()
    matrix = rng.integers(low=-2, high=1, size=(n, m)).astype(object)

    return matrix


def generate_map(n, m, road_perc=0.2, buildings_perc=0.9):
    """
    Builds a random map of the given dimensions, with roads and buildings generated based on the given rates.
    Roads will only ever be horizonal or vertical, and span the full length/width of the map.
    Buildings will never be adjacent to a road (simulates sidewalks).

    n = width of matrix to generate
    m = height of matrix to generate
    road_perc = percentage of rows and columns to turn into roads 
                (default 20%, meaning 1 in 5 rows and columns will be roads)
    buildings_perc = percentage of valid empty spaces (once roads are generated) that should be buildings
                (default 90%, meaning 1 in 10 remaining empty spaces will be buildings)

    returns nxm matrix with empty space (0), roads (-1), and buildings (-2)
    """
    
    # start by generating matrix of all 0s
    matrix = np.full((n,m),0,dtype=object)

    # have some number of roads? generate horizontal then vertical 
    # roads cant be in adjacent rows/cols, 
    num_roads_n = math.floor(n*road_perc)
    num_roads_m = math.floor(m*road_perc)

    # generate roads - rows
    invalid_rows = set()
    for i in range(num_roads_n):
        # replace 0s in a ranom row with -1s
        valid_rows = [i for i in range(n) if i not in invalid_rows]
        loc_i = random.choice(valid_rows)
        matrix[loc_i] = np.array([-1] * m)

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

    return matrix


def building_generation_1(n, m, matrix, invalid_rows, invalid_cols, buildings_perc):
    """
    Randomly generates buildings (represented by -2) onto a given map
    
    n = width of matrix
    m = height of matrix
    matrix = int np matrix with -1s representing roads and 0s representing empty spaces. no buildings yet
    invalid_rows, invalid_cols: lists of row and column indices that are invalid bc roads
    buildings_perc = percentage of valid empty spaces that should be buildings
    """
    
    valid_rows = [i for i in range(n) if i not in invalid_rows]
    valid_cols = [i for i in range(m) if i not in invalid_cols]
    valid_coords = []
    for i in valid_rows:
        for j in valid_cols:
            valid_coords.append([i,j])

    num_buildings = math.floor(len(valid_rows)*len(valid_cols)*buildings_perc)
    for i in range(num_buildings+1):
        coords = random.choice(valid_coords)
        matrix[coords[0]][coords[1]] = -2
        valid_coords.remove(coords)


def get_empty_locations_from_map(map):
    """
    Returns list of coordinates signifying the empty locations from the given map.
    
    map = np matrix of empty space (0), roads (-1) and buildings (-2)
    
    returns list of possible coordinates for cans in [i,j] form
    """

    permissable_locs = []
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i,j] == 0:
                permissable_locs.append([i,j])
    
    return permissable_locs


def save_map_to_npy(map,fname="map.npy",location="."):
    """Saves a map to an npy file for reloading later"""
    np.save(location+"/"+fname, map)


def save_map_to_csv(map,fname="map.npy",location="."):
    """Saves a map to a csv file for reloading later"""
    np.savetxt(location+"/"+fname, map, delimiter=",", fmt="%d")


def load_map_from_npy(fname="map.npy",location="."):
    """Returns np matrix extracted from npy file"""
    matrix = np.load(location+"/"+fname, allow_pickle=True)
    return matrix

def load_map_from_csv(fname="map.csv",location="."):
    """Returns np matrix extracted from csv file"""
    matrix = np.loadtxt(location+"/"+fname, delimiter=",", dtype=int)
    return matrix.astype(object)
