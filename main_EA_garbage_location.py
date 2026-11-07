"""
CISC 455 - Main code for trash can placement evolutionary algorithm
"""

import random

# Input problem parameters
N = 10
M = 20

#   list of coordinates
individial = [[1,2],[4,4],[7,5]]

population = [individial, individial, [[2,3],[5,3]]]

# -----------------------------------------------------
# Mutation
# -----------------------------------------------------
def mutate(individual):
    pass
    # Perform one of the operations at random


def add_trashcan(individual, rows, cols):
    """
    Adds a new random pair of coordinates at a random position in the 
    candidate solution, in place. 
    - Global exploitation (keep good trashcans, but need another) 
    - Allows solutions to grow.
    """
    pos = random.randint(0,len(individual))
    new_trashcan = [random.randint(0,rows-1), random.randint(0,cols-1)]
    individual.insert(pos, new_trashcan)

def remove_trashcan(individual):
    """ 
    Removes a random pair of coordinates from the candidate solution,
    in place. 
    - Allows solutions to shrink.
    """
    # TODO: Throws an error if there isn't at least 1 individual 
    pos = random.randint(0,len(individual)-1)
    individual.pop(pos)

def modify_trashcan(individual, rows, cols):
    """ 
    Modifies a single coordinate from the candidate solution using
    arithmetic creep, in place. 
    - Local exploitation (try to improve 'ok' trashcans)
    """
    # TODO: Throws an error if there isn't at least 1 individual 
    pos = random.randint(0,len(individual)-1)

    # Creep x direction by a small integer, stopping at bounds
    new_x = individual[pos][0] + (int) (2 * random.gauss(0,1))
    new_x = 0 if new_x < 0 else new_x
    new_x = rows-1 if new_x >= rows else new_x

    # Creep y direction by a small integer, stopping at bounds
    new_y = individual[pos][1] + (int) (2 * random.gauss(0,1))
    new_y = 0 if new_y < 0 else new_y
    new_y = cols-1 if new_y >= cols else new_y

    individual[pos] = [new_x, new_y]

# TODO: Make sure insert and modify cannot add duplicates
# TODO: Make sure insert and modify cannot add place on roads or walls
# TODO: Make sure insert, modify cannot exceed the allowed number of trash cans
# TODO: Make sure delete cannot create an empty solution
# TODO: Implement a random mutation selection method
# TODO: Implement an adaptive or self-adaptive selection method
# TODO: Implement a self-adaptive parameter for creep mutation ?

