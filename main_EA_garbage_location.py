"""
CISC 455 - Main code for trash can placement evolutionary algorithm
"""

import random

#   list of coordinates
individial = [[1,2],[4,4],[7,5]]

population = [individial, individial, [[2,3],[5,3]]]

# -----------------------------------------------------
# Mutation
# -----------------------------------------------------
def mutate(individual):
    pass
    # Perform one of the operations at random


def add_trashcan(individual, board, max_trashcans):
    """
    Adds a new random pair of coordinates at a random position in the 
    candidate solution, in place. 
    
    Leaves the individual unchanged if one of the following is true: 
    it already has the max number of trashcans, the new trashcan is a 
    duplicate, or the new trashcan is on a road or wall.

    Throws an IllegalBoard exception if the problem board has no rows
    or no columns.

    Properties:
    - Global exploitation (keep good trashcans, but need another) 
    - Allows solutions to grow
    - Preserves candidate validity
    """
    # Do not add anything if the candidate is already the max size
    if (len(individual) >= max_trashcans):
        return

    rows, cols = getBoardDimensions(board)
    pos = random.randint(0,len(individual))
    new_trashcan = [random.randint(0,rows-1), random.randint(0,cols-1)]

    # Do not add if it is a duplicate or on a road or wall
    if new_trashcan not in individual and isFreeSpace(new_trashcan, board):
        individual.insert(pos, new_trashcan)

def remove_trashcan(individual):
    """ 
    Removes a random pair of coordinates from the candidate, in place.

    Leaves the individual unchanged if it has just one trashcan, to 
    ensure no empty individuals are created.

    Throws an IllegalSolution exception if the input genome is empty.

    Properties:
    - Allows solutions to shrink
    - Preserves candidate validity
    """
    if (len(individual) == 0):
        raise IllegalSolution("remove_trashcan: individual to mutate is empty!")
    
    # Only remove if there are 2+ tashcans; do not create an empty individual
    if (len(individual) > 1):
        pos = random.randint(0,len(individual)-1)
        individual.pop(pos)

def modify_trashcan(individual, board):
    """ 
    Modifies a single coordinate from the candidate solution using
    arithmetic creep, in place. Limits perturbations to the board 
    size.

    Leaves the individual unchanged if one of the following is true: 
    all perturbations are 0, the new trashcan is a duplicate, or the 
    new trashcan is on a road or wall.

    Throws an IllegalSolution exception if the input genome is empty.
    Throws an IllegalBoard exception if the problem board has no rows 
    or no columns.

    Properties:
    - Local exploitation (try to improve 'ok' trashcans)
    - Preserves candidate validity
    """
    if (len(individual) == 0):
        raise IllegalSolution("modify_trashcan: individual to mutate is empty!")

    rows, cols = getBoardDimensions(board)
    pos = random.randint(0,len(individual)-1)

    # Creep x direction by a small integer, stopping at bounds
    new_x = individual[pos][0] + (int) (random.gauss(0,1))
    new_x = 0 if new_x < 0 else new_x
    new_x = rows-1 if new_x >= rows else new_x

    # Creep y direction by a small integer, stopping at bounds
    new_y = individual[pos][1] + (int) (random.gauss(0,1))
    new_y = 0 if new_y < 0 else new_y
    new_y = cols-1 if new_y >= cols else new_y

    # Do not modify if it is a duplicate or on a road or wall
    new_trashcan = [new_x, new_y]
    if new_trashcan not in individual and isFreeSpace(new_trashcan, board):
        individual[pos] = new_trashcan

# TODO: Implement a random mutation selection method
# TODO: Implement an adaptive or self-adaptive selection method
# TODO: Implement a self-adaptive parameter for creep mutation ?

# -----------------------------------------------------
# Helper functions
# -----------------------------------------------------
def isFreeSpace(position, board):
    """
    Returns true if it is not a road (-1) or wall (-2).
    Simply, if the board value is not negative.
    """
    value = board[position[0]][position[1]]
    return value >= 0

def getBoardDimensions(board):
    """
    Returns the dimensions of the board as a tuple (rows, columns).
    Throws IllegalBoard exceptions if there are no rows or columns.
    """
    if len(board) == 0:
        raise IllegalBoard("getBoardDimensions: there are no rows!")
    if len(board[0]) == 0:
        raise IllegalBoard("getBoardDimensions: there are no columns!")
    return len(board), len(board[0])

# -----------------------------------------------------
# Exceptions
# -----------------------------------------------------
class IllegalSolution(Exception):
    """ Indicates an illegal candidate solution. """
    pass

class IllegalBoard(Exception):
    """ Indicates an illegal input problem. """
    pass