"""
Unit test coverage for mutation operators. 
"""

import pytest
import copy

from mutation import (add_trashcan, remove_trashcan, modify_trashcan,
                      is_free_space, get_board_dimensions, 
                      update_sigma_x, update_sigma_y, creep_x_dimension, creep_y_dimension,
                      IllegalBoard)

# Problem information
board = [[0, 0, 0,-2,-2,-2,-2],
         [0, 0, 0,-2, 0, 0,-2],
         [0, 0, 0, 0, 0, 0,-2],
         [0,-2,-2,-2,-1,-1,-1],
         [0, 0, 0,-2,-2, 0, 0]]
rows = len(board)
columns = len(board[0])
max_trashcans = 4
sigma_bound = 1

@pytest.mark.parametrize('times', range(25))
def test_add_trashcan_to_none(times):
    """ Tests up to one gene is added and it is not out of bounds """
    candidate = [] # Although illegal, it simplifies finding the new pair 
    add_trashcan(candidate, board, max_trashcans)

    # Should always add exactly 1 or 0 trashcans (if on wall or road)
    size = len(candidate)
    assert size == 0 or size == 1

    if size == 1:
        # The trashcan should be within bounds
        new_trashcan = candidate[0]
        assert new_trashcan[0] >= 0 and new_trashcan[0] < rows
        assert new_trashcan[1] >= 0 and new_trashcan[1] < columns

        # The trashcan should not be on a road or wall
        tile = board[new_trashcan[0]][new_trashcan[1]]
        assert tile >= 0

@pytest.mark.parametrize('times', range(45))
def test_add_trashcan_to_some(times):
    """ Tests up to one gene is added and it is not a duplicate """
    candidate = [[0,0], [0,2]]
    prev_candidate = copy.deepcopy(candidate)
    add_trashcan(candidate, board, max_trashcans)

    # Should always add exactly 1 or 0 trashcans
    size = len(candidate)
    prev_size = len(prev_candidate)
    assert size == prev_size or size == prev_size + 1

    # If nothing was added
    if size == prev_size:
        # Existing trashcans should not be changed
        assert candidate == prev_candidate

    # If one was added
    else:
        # The new trash can should not be a duplicate
        already_seen = []
        for trashcan in candidate:
            assert trashcan not in already_seen
            already_seen.append(trashcan)

        # Existing trashcans should not be changed
        for trashcan in prev_candidate:
            assert trashcan in candidate

def test_add_trashcan_maxed_out():
    """ Tests no genes are added if it is of maximum size (max_trashcans) """
    candidate = [[0,0], [0,2], [2,3], [1,1]]
    prev_candidate = copy.deepcopy(candidate)
    add_trashcan(candidate, board, max_trashcans)
    # There should be no changes to the solution
    assert candidate == prev_candidate

def test_remove_trashcan_only_one():
    """ Tests no genes are removed if it is of minimum size (1) """
    candidate = [[0,0]]
    prev_candidate = copy.deepcopy(candidate)
    remove_trashcan(candidate)
    # There should be no changes to the solution
    assert candidate == prev_candidate

@pytest.mark.parametrize('times', range(10))
def test_remove_trashcan_more_than_one(times):
    """ Tests that only one gene is removed """
    candidate = [[0,0], [0,2], [2,3], [1,1]]
    prev_candidate = copy.deepcopy(candidate)
    remove_trashcan(candidate)

    # Exactly one trashcan should be removed
    assert len(candidate) == len(prev_candidate) - 1

    # None of the remaining transcans should be changed
    for trashcan in candidate:
        assert trashcan in prev_candidate

@pytest.mark.parametrize('times', range(25))
def test_modify_trashcan_from_one(times):
    """ Tests up to one gene is modified and it is not out of bounds """
    candidate = [[1,1]]
    prev_candidate = copy.deepcopy(candidate)
    modify_trashcan(candidate, board)

    # The size of the candidate should be the same
    assert len(candidate) == len(prev_candidate)

    # The trashcan should be within bounds
    new_trashcan = candidate[0]
    assert new_trashcan[0] >= 0 and new_trashcan[0] < rows
    assert new_trashcan[1] >= 0 and new_trashcan[1] < columns

    # The trashcan should not be on a road or wall
    tile = board[new_trashcan[0]][new_trashcan[1]]
    assert tile >= 0

@pytest.mark.parametrize('times', range(45))
def test_modify_trashcan_from_many(times):
    """ Tests up to one gene is modified and it is not a duplicate """
    candidate = [[0,0], [0,2], [2,3]]
    prev_candidate = copy.deepcopy(candidate)
    modify_trashcan(candidate, board)

    # The size of the candidate should be the same
    assert len(candidate) == len(prev_candidate)

    # The candidate should have no duplicates
    already_seen = []
    for trashcan in candidate:
        assert trashcan not in already_seen
        already_seen.append(trashcan)

    # The candidate should have exactly 1 or 0 changed genes
    numDifferentGenes = 0
    for trashcan in candidate:
        if trashcan not in prev_candidate:
            numDifferentGenes += 1
    assert numDifferentGenes == 0 or numDifferentGenes == 1

def test_is_free_space():
    """ Tests all possible tile values """
    assert is_free_space([0,0], board)      #  0 = free
    assert not is_free_space([0,4], board)  # -2 = building
    assert not is_free_space([3,4], board)  # -1 = road

def test_get_board_dimensions():
    """ Tests that dimensions are correct and exceptions are thrown """
    dimensions = get_board_dimensions(board)
    assert dimensions == (5,7)
    with pytest.raises(IllegalBoard):
        get_board_dimensions([])
    with pytest.raises(IllegalBoard):
        get_board_dimensions([[]])

@pytest.mark.parametrize('times', range(10))
def test_update_sigma_x(times):
    """ Sigma x should never be less than bound, and sigma y is unchanged """
    sigma = [1,1]
    prev_sigma = copy.deepcopy(sigma)
    learning_rate = 2
    update_sigma_x(sigma, learning_rate, sigma_bound)

    # Sigma x may change but never dip below the bound
    assert sigma[0] >= sigma_bound
    # Sigma y should never change
    assert sigma[1] == prev_sigma[1]

@pytest.mark.parametrize('times', range(10))
def test_update_sigma_y(times):
    """ Sigma y should never be less than bound, and sigma y is unchanged """
    sigma = [1,1]
    prev_sigma = copy.deepcopy(sigma)
    learning_rate = 2
    update_sigma_y(sigma, learning_rate, sigma_bound)

    # Sigma x may change but never dip below the bound
    assert sigma[0] == prev_sigma[0]
    # Sigma y should never change
    assert sigma[1] >= sigma_bound

@pytest.mark.parametrize('times', range(10))
def test_creep_x_dimension(times):
    """ Ensure the new x value is within the bounds """
    trashcan = [1,1]
    prev_trashcan = copy.deepcopy(trashcan)

    # Trashcan itself is unchaged for now, and new x is within bounds
    new_x = creep_x_dimension(trashcan, rows, sigma=[10,0])
    assert trashcan == prev_trashcan
    assert new_x >= 0 and new_x < rows

    # If step size is 0, it should be unchanged
    new_x = creep_x_dimension(trashcan, rows, sigma=[0,0])
    assert new_x == trashcan[0]

@pytest.mark.parametrize('times', range(10))
def test_creep_y_dimension(times):
    """ Ensure the new y value is within the bounds """
    trashcan = [1,1]
    prev_trashcan = copy.deepcopy(trashcan)
    new_y = creep_x_dimension(trashcan, columns, sigma=[0,10])

    # Trashcan itself is unchaged for now, and new y is within bounds
    assert trashcan == prev_trashcan
    assert new_y >= 0 and new_y < columns

    # If step size is 0, it should be unchanged
    new_y = creep_x_dimension(trashcan, columns, sigma=[0,0])
    assert new_y == trashcan[0]
