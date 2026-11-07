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

@pytest.mark.parametrize('times', range(10))
def test_add_trashcan_to_none(times):
    candidate = []
    add_trashcan(candidate, rows, columns)

    # One trash can should have been added
    assert len(candidate) == 1

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
    add_trashcan(candidate, rows, columns)

    # Should always add exactly 1 or 0 trashcans
    size = len(candidate)
    prev_size = len(prev_candidate)
    assert size == prev_size or size == prev_size + 1

    # If no trashcan was added
    if (size == prev_size):
        # The list should remain the exact same
        assert candidate == prev_candidate

    # If one trashcan was added
    else:
        # It should not be a duplicate
        already_seen = []
        for trashcan in candidate:
            assert trashcan not in already_seen
            already_seen.append(trashcan)

        # No other elements should be changed
        for trashcan in prev_candidate:
            assert trashcan in candidate
