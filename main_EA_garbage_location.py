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
    pos = random.randint(0,len(individual)-1)
    individual.pop(pos)

def modify_trashcan(individual, rows, cols):
    """ 
    Modifies a single coordinate from the candidate solution using
    arithmetic creep, in place. 
    - Local exploitation (try to improve 'ok' trashcans)
    """
    pos = random.randint(0,len(individual)-1)
    coord = random.randint(0,1)

    # Modify one of coordinates of the trashcan at the position
    pass

# TODO: Make sure insert and modify cannot add duplicates
# TODO: Make sure insert and modify cannot add place on roads or walls
# TODO: Implement a random selection method
# TODO: Implement an adaptive or self-adaptive selection method
# TODO: Implement a self-adaptive method for creep mutation ?

