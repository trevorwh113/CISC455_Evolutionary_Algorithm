"""
Unit test coverage for mutation operators
"""

import pytest
import copy
import numpy as np

from mutation import *

# Problem information
board = np.array([[0, 0, 0,-2,-2,-2,-2],
                  [0, 0, 0,-2, 0, 0,-2],
                  [0, 0, 0, 0, 0, 0,-2],
                  [0,-2,-2,-2,-1,-1,-1],
                  [0, 0, 0,-2,-2, 0, 0]], dtype=object)
rows, columns = board.shape
max_trashcans = 4
learning_rate = 2
sigma_bound = 1

# -----------------------------------------------------
# Basic Mutation Operators
# -----------------------------------------------------
class TestAddTrashcan():
    """ Tests basic add traschan mutation """
    @pytest.mark.parametrize('times', range(25))
    def test_add_trashcan_to_none(self, times):
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

    @pytest.mark.parametrize('times', range(25))
    def test_add_trashcan_to_some(self, times):
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

    def test_add_trashcan_maxed_out(self):
        """ Tests no genes are added if it is of maximum size (max_trashcans) """
        candidate = [[0,0], [0,2], [2,3], [1,1]]
        prev_candidate = copy.deepcopy(candidate)
        add_trashcan(candidate, board, max_trashcans)
        # There should be no changes to the solution
        assert candidate == prev_candidate

class TestRemoveTraschcan:
    """ Test basic remove trashcan mutation """
    def test_remove_trashcan_only_one(self):
        """ Tests no genes are removed if it is of minimum size (1) """
        candidate = [[0,0]]
        prev_candidate = copy.deepcopy(candidate)
        remove_trashcan(candidate)
        # There should be no changes to the solution
        assert candidate == prev_candidate

    @pytest.mark.parametrize('times', range(10))
    def test_remove_trashcan_more_than_one(self, times):
        """ Tests that only one gene is removed """
        candidate = [[0,0], [0,2], [2,3], [1,1]]
        prev_candidate = copy.deepcopy(candidate)
        remove_trashcan(candidate)

        # Exactly one trashcan should be removed
        assert len(candidate) == len(prev_candidate) - 1

        # None of the remaining transcans should be changed
        for trashcan in candidate:
            assert trashcan in prev_candidate

class TestModifyOneTrashcan:
    """ Tests basic single trashcan modificaiton mutation """
    @pytest.mark.parametrize('times', range(25))
    def test_modify_one_trashcan_from_one(self, times):
        """ Tests up to one gene is modified and it is not out of bounds """
        candidate = [[1,1]]
        prev_candidate = copy.deepcopy(candidate)
        modify_one_trashcan(candidate, board)

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
    def test_modify_one_trashcan_from_many(self, times):
        """ Tests up to one gene is modified and it is not a duplicate """
        candidate = [[0,0], [0,2], [2,3]]
        prev_candidate = copy.deepcopy(candidate)
        modify_one_trashcan(candidate, board)

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

class TestModifyAllTrashcans:
    """ Tests basic all trashcan modificaiton mutation """
    @pytest.mark.parametrize('times', range(45))
    def test_modify_all_trashcans_from_many(self, times):
        """ Tests that up to all genes are modified and there are duplicate """
        candidate = [[0,0], [0,2], [2,3]]
        prev_candidate = copy.deepcopy(candidate)
        modify_all_trashcans(candidate, board)

        # The size of the candidate should be the same
        assert len(candidate) == len(prev_candidate)

        # The candidate should have no duplicates
        already_seen = []
        for trashcan in candidate:
            assert trashcan not in already_seen
            already_seen.append(trashcan)

        for i in range(len(candidate)):
            # All genes should remain in the bounds
            new_trashcan = candidate[i]
            assert new_trashcan[0] >= 0 and new_trashcan[0] < rows
            assert new_trashcan[1] >= 0 and new_trashcan[1] < columns

            # All genes should not be on roads or walls
            tile = board[new_trashcan[0]][new_trashcan[1]]
            assert tile >= 0

class TestSelfAdaptiveModifyOneTrashcan:
    """ Tests self-adaptive single trashcan modificaiton mutation """
    @pytest.mark.parametrize('times', range(25))
    def test_self_adaptive_modify_one_trashcan_from_one(self, times):
        """ Tests up to one gene and step size is modified and it is not out of bounds """
        candidate = [[1,1]]
        sigmas = [[1,1]]
        prev_candidate = copy.deepcopy(candidate)
        prev_sigmas = copy.deepcopy(sigmas)
        self_adaptive_modify_one_trashcan(candidate, board, sigmas, learning_rate, sigma_bound)

        # The size of the candidate and sigmas should be the same
        assert len(candidate) == len(prev_candidate)
        assert len(sigmas) == len(prev_sigmas)

        # The trashcan should be within bounds
        new_trashcan = candidate[0]
        assert new_trashcan[0] >= 0 and new_trashcan[0] < rows
        assert new_trashcan[1] >= 0 and new_trashcan[1] < columns

        # The trashcan should not be on a road or wall
        tile = board[new_trashcan[0]][new_trashcan[1]]
        assert tile >= 0

        # The value of sigma should remain above the bounds
        new_sigma = sigmas[0]
        assert new_sigma[0] >= sigma_bound
        assert new_sigma[1] >= sigma_bound

    @pytest.mark.parametrize('times', range(45))
    def test_self_adaptive_modify_one_trashcan_from_many(self, times):
        """ Tests up to one gene and step size is modified and it is not a duplicate """
        candidate = [[0,0], [0,2], [2,3]]
        sigmas = [[1,1], [1,1], [1,1]]
        prev_candidate = copy.deepcopy(candidate)
        prev_sigmas = copy.deepcopy(sigmas)
        self_adaptive_modify_one_trashcan(candidate, board, sigmas, learning_rate, sigma_bound)
    
        # The size of the candidate and sigmas should be the same
        assert len(candidate) == len(prev_candidate)
        assert len(sigmas) == len(prev_sigmas)

        # The candidate should have no duplicates
        already_seen = []
        for trashcan in candidate:
            assert trashcan not in already_seen
            already_seen.append(trashcan)

        # The candidate should have exactly 1 or 0 changed genes
        # Likewise, the candidate should have exactly 1 or 0 changed sigmas
        numDifferentGenes = 0
        numDifferentSigmas = 0
        for i in range(len(candidate)):
            if candidate[i] not in prev_candidate:
                numDifferentGenes += 1
            if sigmas[i] not in prev_sigmas:
                numDifferentSigmas += 1
        assert numDifferentGenes == 0 or numDifferentGenes == 1
        assert numDifferentSigmas == 0 or numDifferentSigmas == 1

class TestSelfAdaptiveModifyAllTrashcans:
    """ Tests self-adaptive all trashcan modificaiton mutation """
    @pytest.mark.parametrize('times', range(45))
    def test_self_adaptive_modify_all_trashcans_from_many(self, times):
        """ Tests that up to all genes and step sizes are modified and there are duplicate """
        candidate = [[0,0], [0,2], [2,3]]
        sigmas = [[1,1], [1,1], [1,1]]
        prev_candidate = copy.deepcopy(candidate)
        prev_sigmas = copy.deepcopy(sigmas)
        self_adaptive_modify_one_trashcan(candidate, board, sigmas, learning_rate, sigma_bound)

        # The size of the candidate should be the same
        assert len(candidate) == len(prev_candidate)
        assert len(sigmas) == len(prev_sigmas)

        # The candidate should have no duplicates
        already_seen = []
        for trashcan in candidate:
            assert trashcan not in already_seen
            already_seen.append(trashcan)

        for i in range(len(candidate)):
            # All genes should remain in the bounds
            new_trashcan = candidate[i]
            assert new_trashcan[0] >= 0 and new_trashcan[0] < rows
            assert new_trashcan[1] >= 0 and new_trashcan[1] < columns

            # All genes should not be on roads or walls
            tile = board[new_trashcan[0]][new_trashcan[1]]
            assert tile >= 0

            # All step sizes should be in bounds
            new_sigma = sigmas[i]
            assert new_sigma[0] >= sigma_bound
            assert new_sigma[1] >= sigma_bound

class TestInputBoard:
    """ Tests helpers for input board processing """
    def test_is_free_space(self):
        """ Tests all possible tile values """
        assert is_free_space([0,0], board)      #  0 = free
        assert not is_free_space([0,4], board)  # -2 = building
        assert not is_free_space([3,4], board)  # -1 = road

    def test_get_board_dimensions(self):
        """ Tests that dimensions are correct and exceptions are thrown """
        dimensions = get_board_dimensions(board)
        assert dimensions == (5,7)
        with pytest.raises(IllegalBoard):
            # 1 dimensional
            get_board_dimensions(np.array([]))
        with pytest.raises(IllegalBoard):
            # 2 dimensional but no elements
            get_board_dimensions(np.array([[]]))
        with pytest.raises(IllegalBoard):
            # 3 dimensional
            get_board_dimensions(np.array([[[0,0], [0,0]], [[0,0], [0,0]]]))

class TestSimpleModifyHelpers:
    """ Tests helpers for basic modification mutations """
    @pytest.mark.parametrize('times', range(10))
    def test_creep_trashcan(self, times):
        """ Both new coordinate values should be within bounds """
        trashcan = [1,1]
        prev_trashcan = copy.deepcopy(trashcan)

        # New x is within bounds and y does not change if sigma_y = 1
        new_x, new_y = creep_trashcan(trashcan, (rows, columns), sigma=[10,0])
        assert new_x >= 0 and new_x < rows
        assert new_y == trashcan[1]
        # The trashcan is not modified in place yet
        assert trashcan == prev_trashcan

        # New y is within bounds and x does not change if sigma_x = 1
        new_x, new_y = creep_trashcan(trashcan, (rows, columns), sigma=[0,10])
        assert new_x == trashcan[0]
        assert new_y >= 0 and new_y < columns
        # The trashcan is not modified in place yet
        assert trashcan == prev_trashcan

    @pytest.mark.parametrize('times', range(10))
    def test_modify_trashcan(self, times):
        candidate = [[0,0], [0,2], [2,3]]
        sigmas = [[1,1], [1,1], [1,1]]
        prev_candidate = copy.deepcopy(candidate)

        pos = 0
        modify_trashcan(candidate, sigmas, board, pos, (rows, columns))

        # The size of the candidate should be the same
        assert len(candidate) == len(prev_candidate)

        # The candidate should have no duplicates
        already_seen = []
        for trashcan in candidate:
            assert trashcan not in already_seen
            already_seen.append(trashcan)

        # Only the trashcan at the specified value should change
        for i in range(len(candidate)):
            if i != pos:
                assert candidate[i] == prev_candidate[i]

class TestAdaptiveModifyHelpers:
    """ Tests helpers for self-adaptive modification mutations """
    @pytest.mark.parametrize('times', range(10))
    def test_update_sigma(self, times):
        """ Both new step sizes should not be less than the bound """
        sigma = [1,1]
        update_sigma(sigma, learning_rate, sigma_bound)

        # Sigmas may change but never dip below the bound
        assert sigma[0] >= sigma_bound
        assert sigma[1] >= sigma_bound

    @pytest.mark.parametrize('times', range(10))
    def test_self_adaptive_modify_trashcan(self, times):
        candidate = [[0,0], [0,2], [2,3]]
        sigmas = [[1,1], [1,1], [1,1]]
        prev_candidate = copy.deepcopy(candidate)
        prev_sigmas = copy.deepcopy(sigmas)

        pos = 0
        self_adaptive_modify_trashcan(candidate, sigmas, board, pos, (rows, columns), learning_rate, sigma_bound)

        # The size of the candidate should be the same
        assert len(candidate) == len(prev_candidate)

        # The candidate should have no duplicates
        already_seen = []
        for trashcan in candidate:
            assert trashcan not in already_seen
            already_seen.append(trashcan)

        # Only the trashcan at the specified value should change
        # Likewise, only the step size of the specified value should change
        for i in range(len(candidate)):
            if i != pos:
                assert candidate[i] == prev_candidate[i]
                assert sigmas[i] == prev_sigmas[i]
