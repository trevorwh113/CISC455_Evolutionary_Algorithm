"""
Implementation of mutation operators
"""
import random
import numpy as np
import math

# -----------------------------------------------------
# Mutation Selection Operators
# -----------------------------------------------------
# TODO: Implement an adaptive or self-adaptive selection method
# TODO: Test the self-adaptive creep mutation

def random_mutate(individual, board, max_trashcans):
    """
    Performs one type of mutation on the individual at random
    from the following operators: add, remove, modify.
    """
    operator = random.randint(0,2)
    if operator == 0:
        add_trashcan(individual, board, max_trashcans)
    elif operator == 1:
        remove_trashcan(individual)
    else:
        modify_trashcan(individual, board)

def informed_mutate(individual, board, max_trashcans):
    pass

# -----------------------------------------------------
# Basic Mutation Operators
# -----------------------------------------------------
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

    rows, cols = get_board_dimensions(board)
    pos = random.randint(0,len(individual))
    new_trashcan = [random.randint(0,rows-1), random.randint(0,cols-1)]

    # Do not add if it is a duplicate or on a road or wall
    if new_trashcan not in individual and is_free_space(new_trashcan, board):
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

# TODO: Should this operate on all the existing ones or just pick one to change
def modify_trashcan(individual, board, sigma=[1,1]):
    """ 
    Modifies a single coordinate from the candidate solution using
    arithmetic creep, in place. Limits perturbations to the board 
    size. Creep step uses standard deviation 1 by default (sigma)
    for both coordinates.

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

    # Pick a random trashcan to mutate
    rows, cols = get_board_dimensions(board)
    pos = random.randint(0,len(individual)-1)

    # Creep both directions by a small integer, stopping at bounds
    new_x = creep_x_dimension(individual[pos], rows, sigma)
    new_y = creep_y_dimension(individual[pos], cols, sigma)

    # Do not modify if it is a duplicate or on a road or wall
    new_trashcan = [new_x, new_y]
    if new_trashcan not in individual and is_free_space(new_trashcan, board):
        individual[pos] = new_trashcan

# -----------------------------------------------------
# Self-Adaptive Mutation Operators
# -----------------------------------------------------
# TODO: Should this operate on all the existing ones or just pick one to change
def self_adaptive_modify_trashcan(individual, sigmas, board, learning_rate, bound):
    """ 
    Modifies a single coordinate from the candidate solution using
    arithmetic creep, in place. Limits perturbations to the board 
    size. Creep step uses standard deviations sigmas, containing a
    pair of x and y step sizes for each chromosome (trashcan). Step
    sizes adapt based on the global learning rate, and cannot
    drop below bound.

    - individual: [[x,y],              [x2,y2],                ...]
    - sigmas:     [[sigma_x, sigma_y], [sigma_x_2, sigma_y_2], ...]
    - board: [[0,0,-1], [-2,-2,-2], ...]
    - learning rate: int
    - bound: int

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

    ## indvidual [[1,1], [1,2], ...] - the traschans in the individual
    ## sigmas - [[1,1], [3,0], ... ] the step sizes for each direction for each individual

    if (len(individual) == 0):
        raise IllegalSolution("modify_trashcan: individual to mutate is empty!")

    # Pick a random trashcan to mutate
    rows, cols = get_board_dimensions(board)
    pos = random.randint(0,len(individual)-1)

    # Mutate the step size
    update_sigma_x(sigmas[pos], learning_rate, bound)
    update_sigma_y(sigmas[pos], learning_rate, bound)

    # Creep both directions by a small integer, stopping at bounds
    new_x = creep_x_dimension(individual[pos], rows, sigmas[pos])
    new_y = creep_y_dimension(individual[pos], cols, sigmas[pos])

    # Do not modify if it is a duplicate or on a road or wall
    new_trashcan = [new_x, new_y]
    if new_trashcan not in individual and is_free_space(new_trashcan, board):
        individual[pos] = new_trashcan

# -----------------------------------------------------
# Helper functions
# -----------------------------------------------------
def is_free_space(position, board):
    """
    Returns true if it is not a road (-1) or wall (-2).
    Simply, if the board value is not negative.
    """
    value = board[position[0]][position[1]]
    return value >= 0

def get_board_dimensions(board):
    """
    Returns the dimensions of the board as a tuple (rows, columns).
    Throws IllegalBoard exceptions if there are no rows or columns.
    """
    if len(board) == 0:
        raise IllegalBoard("get_board_dimensions: there are no rows!")
    if len(board[0]) == 0:
        raise IllegalBoard("get_board_dimensions: there are no columns!")
    return len(board), len(board[0])

def update_sigma_x(sigma, learning_rate, bound):
    """
    Given a pair of step sizes (sigma), updates the sigma in 
    the x direction in place by sampling using the learning rate.
    The sigma cannot drop below bound.
    """
    new_sigma_x = sigma[0] * math.exp(learning_rate * random.gauss(0,1))
    new_sigma_x = bound if new_sigma_x < bound else new_sigma_x
    sigma[0] = new_sigma_x

def update_sigma_y(sigma, learning_rate, bound):
    """
    Given a pair of step sizes (sigma), updates the sigma in 
    the y direction in place by sampling using the learning rate.
    The sigma cannot drop below bound.
    """
    new_sigma_y = sigma[1] * math.exp(learning_rate * random.gauss(0,1))
    new_sigma_y = bound if new_sigma_y < bound else new_sigma_y
    sigma[1] = new_sigma_y

def creep_x_dimension(trashcan, rows, sigma):
    """
    Given a trashcan, returns the x coordinate after applying
    an integer creep mutation with the x value of the given
    step size sigma. Keeps x within bounds.
    """
    new_x = trashcan[0] + (int) (sigma[0] * random.gauss(0,1))
    new_x = 0 if new_x < 0 else new_x
    new_x = rows-1 if new_x >= rows else new_x
    return new_x

def creep_y_dimension(trashcan, cols, sigma):
    """
    Given a trashcan, returns the y coordinate after applying
    an integer creep mutation with the y value of the given
    step size sigma. Keeps y within bounds.
    """
    new_y = trashcan[1] + (int) (sigma[1] * random.gauss(0,1))
    new_y = 0 if new_y < 0 else new_y
    new_y = cols-1 if new_y >= cols else new_y
    return new_y

# -----------------------------------------------------
# Exceptions
# -----------------------------------------------------
class IllegalSolution(Exception):
    """ Indicates an illegal candidate solution. """
    pass

class IllegalBoard(Exception):
    """ Indicates an illegal input problem. """
    pass