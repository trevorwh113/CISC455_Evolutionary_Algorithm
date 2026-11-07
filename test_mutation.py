"""
Unit test coverage for mutation functionality. 
"""

import pytest
import copy

from main_EA_garbage_location import add_trashcan, remove_trashcan, modify_trashcan

# Problem information
board = [[0, 0, 0,-2,-2,-2,-2],
         [0, 0, 0,-2, 0, 0,-2],
         [0, 0, 0, 0, 0, 0,-2],
         [0,-2,-2,-2,-1,-1,-1],
         [0, 0, 0,-2,-2, 0, 0]]
rows = len(board)
columns = len(board[0])
max_trashcans = 4

@pytest.mark.parametrize('times', range(25))
def test_add_trashcan_to_none(times):
    candidate = []
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
    candidate = [[0,0], [0,2], [2,3], [1,1]]
    prev_candidate = copy.deepcopy(candidate)
    add_trashcan(candidate, board, max_trashcans)
    # There should be no changes to the solution
    assert candidate == prev_candidate