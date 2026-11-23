"""
Implementation of mutation operators and selectors
"""
import random
from enum import Enum

class MutationStrategy():
    """ A class to simplify selecting a mutation strategy """

    class Strategy(Enum):
        """ Enum designating the chosen mutation selection strategy """
        NONE = 0
        RANDOM = 1
        PROBABILISTIC = 2
        INFORMED = 3
        SELF_ADAPTIVE = 4

    def __init__(self):
        """ 
        Initializes paramters to default values. 
        Specific 'set' functions must be called before mutate().
        """
        # Board and initialization attributes
        self.board = None
        self.dimensions = None
        self.strategy = self.Strategy.NONE

        # Common default attributes
        self.sigma = [1,1]
        self.all = False

        # Probabilisitc mutation attributes
        self.probabilities = [0.33, 0.33, 0.33]

        # Informed mutation attributes
        self.bounds = [0,0.3]

        # Self-adaptive mutation attributes
        self.probability_sigma = 1

    def setBoardState(self, board):
        """ Saves informations about the input map 'board' """
        self.board = board
        self.dimensions = get_board_dimensions(board)

    def setStandardDeviation(self, sigma):
        """ Sets the 'sigma' of shape [x,y] for creep modify mutation """
        self.sigma = sigma

    def setModifyAll(self, all):
        """ Sets whether modify mutations change one or all trashcans """
        self.all = all

    def getStrategy(self):
        """ Returns the set mutation strategy """
        return self.strategy

    def printStrategy(self):
        """ Prints the mutations strategy parameters """
        print("Strategy:", self.strategy)
        print("Sigma:", self.sigma)
        print("Mutate All:", self.all)
        print("PM - Probabilities:", self.probabilities)
        print("IM - Bounds:", self.bounds)
        print("LM - Sigma:", self.probability_sigma)

    def initLearnedProbabilities(mu):
        """
        Returns a 2D list with a list of mutation probabilities for each 
        individual. Each inner list has structure: [p_add, p_remove, p_modify].
        Used for self-adaptive mutations. Every probability defaults to 33%.

        Parameters: 
            mu: size of the population
        Returns:
            list of lists representing mutation probabilities [[0.33, 0.33, 0.33], ...]
        """
        learned_probabilities = []
        for i in range(mu):
            learned_probabilities.append([0.33, 0.33, 0.33])
        return learned_probabilities

    def mutate(self, individual, fitness=1, penalty=0, learned_probabilities=[]):
        """ 
        Mutates the given individual in place using the set mutation selection
        strategy. A strategy must be set first with one of the setter methods.

        Parameters:
            individual: list of coordinates [row,col] (ex: [[0,0],[0,1]])
            fitness: integer, fitness of the individual, for informed mutation
            penalty: integer, canOverMax penalty for the individual, for informed mutation
            learned_probabilities: 2D list, learned mutation probabilities for self-adaptation
        """
        if self.strategy == self.Strategy.RANDOM:
            self.__random_mutate(individual)
        
        elif self.strategy == self.Strategy.PROBABILISTIC:
            self.__probabilistic_mutate(individual)
        
        elif self.strategy == self.Strategy.INFORMED:
            self.__informed_mutate(individual, fitness, penalty)
        
        elif self.strategy == self.Strategy.SELF_ADAPTIVE:
            self.__probabilistic_mutate(individual, learned_probabilities)

        else:
            print("No mutation strategy set!")

    def setRandomMutation(self):
        """ Selects the random mutation strategy """
        self.strategy = self.Strategy.RANDOM

    def setProbabilisiticMutation(self, probabilities):
        """ 
        Selects the probabilisitic mutation strategy with the given probabilities,
        which must each be 0 <= i <= 1.
        
        Parameters:
            probabilities: list, universal mutation probabilities [p_add, p_remove, p_modify] 
        """
        self.strategy = self.Strategy.PROBABILISTIC
        self.probabilities = probabilities

    def setInformedMutation(self, bounds):
        """
        Selects the informed mutation strategy using canOverMax proportions.
        Lower and upper bounds i given must be 0 <= i <= 1.
        
        Parameters:
            bounds: list, target bounds for canOverMax penalty [lower, upper]
        """
        self.strategy = self.Strategy.INFORMED
        self.bounds = bounds

    def setLearningMutation(self, probability_sigma):
        """
        Selects the self-adaptive mutation, with the given 
        standard deviation for learning mutation probabilities.

        Parameters:
            probability_sigma: real, standard deviation
        """
        self.strategy = self.Strategy.SELF_ADAPTIVE
        self.probability_sigma = probability_sigma

    # -----------------------------------------------------
    # Mutation Selection Operators
    # -----------------------------------------------------
    def __random_mutate(self, individual):
        """
        Performs one type of mutation on the individual at random
        from the following operators: add, remove, modify.

        Parameters:
            individual: list of coordinates [row,col] (ex: [[0,0],[0,1]])
        """
        operator = random.randint(0,2)

        if operator == 0:
            self.__add_trashcan(individual)

        elif operator == 1:
            self.__remove_trashcan(individual)

        else:
            self.__modify_trashcan(individual)

    def __probabilistic_mutate(self, individual, learned_probabilities=[]):
        """
        Performs each type of mutation with the set probability rate from the 
        following operators: add, remove, modify. For probabilistic mutation, 
        uses the globally set probabilities. For self-adaptive mutation, uses 
        and mutates in place the given learned_probabilities.

        Parameters:
            individual: list of coordinates [row,col] (ex: [[0,0],[0,1]])
            learned_probabilities: list of mutation probabilities learned for the individual [p_add, p_remove, p_modify]
        """
        add, remove, modify = random.random(), random.random(), random.random()

        actual_probabilities = self.probabilities

        # If using self-adaptive, mutate and use the leared probabilities
        if self.strategy == self.Strategy.SELF_ADAPTIVE:
            self.__mutate_probabilities(learned_probabilities, self.probability_sigma)
            actual_probabilities = learned_probabilities

        if add < actual_probabilities[0]:
            self.__add_trashcan(individual)
        
        if remove < actual_probabilities[1]:
            self.__remove_trashcan(individual)

        if modify < actual_probabilities[2]:
            self.__modify_trashcan(individual)

    def __informed_mutate(self, individual, fitness, penalty):
        """
        Performs a mutation strategy based on the ratio of extra can penalty 
        ('penalty') to total fitness ('fitness'). If it is on the high end of the
        desired proportional range, removes trashcans to reduce the penalty. If it 
        is on the low end, adds trashcans to try to reduce other penalties. If it 
        falls within the range, pick a random mutation.

        Parameters:
            individual: list of coordinates [row,col] (ex: [[0,0],[0,1]])
            fitness: integer, fitness of the individual
            penalty: integer, total canOver penalty part of the fitness
        """    
        ratio = penalty / fitness
        if ratio < self.bounds[0]:
            self.__add_trashcan(individual)
        elif ratio > self.bounds[1]:
            self.__remove_trashcan(individual)
        else:
            self.__random_mutate(individual)

    # -----------------------------------------------------
    # Basic Mutation Operators
    # -----------------------------------------------------
    def __add_trashcan(self, individual):
        """
        Adds a new random pair of coordinates at a random position in the 
        candidate solution, in place. 
        
        Leaves the individual unchanged if the new trashcan is a duplicate, 
        or the new trashcan is on a road or wall.

        - Global exploitation (keep good trashcans, but need another) 
        - Allows solutions to grow
        - Preserves candidate validity

        Parameters:
            individual: list of coordinates [row,col] (ex: [[0,0],[0,1]])
        Throws:
            IllegalBoard: if the problem board has no rows or columns
        """
        rows, cols = self.dimensions
        pos = random.randint(0,len(individual))
        new_trashcan = [random.randint(0,rows-1), random.randint(0,cols-1)]

        # Do not add if it is a duplicate or on a road or wall
        if new_trashcan not in individual and is_free_space(new_trashcan, self.board):
            individual.insert(pos, new_trashcan)

    def __remove_trashcan(self, individual):
        """ 
        Removes a random pair of coordinates from the candidate, in place.
        
        Leaves the individual unchanged if it has just one trashcan, to 
        ensure no empty individuals are created.

        - Allows solutions to shrink
        - Preserves candidate validity

        Parameters:
            individual: list of coordinates [row,col] (ex: [[0,0],[0,1]])
        Throws:
            IllegalSolution: if the input genome is empty
        """
        if (len(individual) == 0):
            raise IllegalSolution("remove_trashcan: individual to mutate is empty!")
        
        # Only remove if there are 2+ tashcans; do not create an empty individual
        if (len(individual) > 1):
            pos = random.randint(0,len(individual)-1)
            individual.pop(pos)

    def __modify_trashcan(self, individual):
        """ 
        Modifies both coordinates in trashcans in the candidate solution using 
        arithmetic creep, in place. If 'all' is set, creeps every allele. Otherwise, 
        chooses a random trashcan to creep. 
        
        Limits perturbations to the board size. Creep step sizes are uniform for all 
        coordinates in each direction. Leaves the individual unchanged if one of the 
        following is true: all perturbations are 0, the new trashcan is a duplicate, 
        or the new trashcan is on a road or wall.
    
        - Local exploitation (try to improve 'ok' trashcans)
        - Preserves candidate validity
        - Smaller change (up to one trashcan)

        Parameters:
            individual: list of coordinates [row,col] (ex: [[0,0],[0,1]])
            board: input map state as an n x n numpy array
            sigma: the step sizes to creep in each direction (default: [1,1])
        Throws:
            IllegalSolution: if the input genome is empty
            IllegalBoard: if the problem board has no rows or columns
        """
        if (len(individual) == 0):
            raise IllegalSolution("modify_trashcan: individual to mutate is empty!")

        num_traschans = len(individual)
        sigmas = [self.sigma] * num_traschans

        # Mutates every trashcan in the candidate
        if all:
            for pos in range(num_traschans):
                self.__modify_trashcan_at_pos(individual, sigmas, pos)
    
        # Pick a random trashcan to mutate
        else:
            pos = random.randint(0,len(individual)-1)
            self.__modify_trashcan_at_pos(individual, sigmas, pos)

    # -----------------------------------------------------
    # Mutation Helpers
    # -----------------------------------------------------
    def __creep_trashcan(self, trashcan, sigma):
        """
        Given a trashcan, returns both coordinates after applying an integer creep 
        mutation with the the given step size sigma. Keeps x and y within bounds.

        Parameters:
            trashcan: list, coordinates [row,col]
            sigma: list, standard deviations in each direction [s_row, s_col]
        Returns:
            tuple representing the modified coordinates (row', col')
        """
        new_x = trashcan[0] + (int) (sigma[0] * random.gauss(0,1))
        new_x = 0 if new_x < 0 else new_x
        new_x = self.dimensions[0]-1 if new_x >= self.dimensions[0] else new_x

        new_y = trashcan[1] + (int) (sigma[1] * random.gauss(0,1))
        new_y = 0 if new_y < 0 else new_y
        new_y = self.dimensions[1]-1 if new_y >= self.dimensions[1] else new_y

        return new_x, new_y

    def __mutate_probabilities(self, probabilities, sigma):
        """
        Given mutation probabiltiies, mutates each in place using real-number 
        arithemtic creep. Each value remains a valid probability between 0 and 1.

        Parameters:
            probabilities: list, mutation probabilites [p_add, p_remove, p_modify]
            sigma: int, standard deviation for probabilities
        """
        # Mutate the given probabilities
        for i in range(len(probabilities)):
            new_prob = probabilities[i] + sigma * random.gauss(0,1)
            probabilities[i] = max(0, min(1, new_prob))

    def __modify_trashcan_at_pos(self, individual, sigmas, pos):
        """
        Performs integer creep mutation in place on the traschan at position 'pos'
        in 'individual' using its corresponding standard deviations in 'sigma'.

        Parameters:
            individual: list of coordinates [row,col] (ex: [[0,0],[0,1]])
            sigmas: list, standard deviations for each trashcan [[s_row1, s_col1], [s_row2, s_col2]...]
        """
        # Creep both directions by a small integer, stopping at bounds
        new_x, new_y = self.__creep_trashcan(individual[pos], sigmas[pos])

        # Do not modify if it is a duplicate or on a road or wall
        new_trashcan = [new_x, new_y]
        if new_trashcan not in individual and is_free_space(new_trashcan, self.board):
            individual[pos] = new_trashcan

# -----------------------------------------------------
# Helper Functions
# -----------------------------------------------------
def is_free_space(position, board):
    """
    Returns true if it is not a road (-1) or wall (-2).
    Simply, if the board value is not negative.

    Parameters:
        position: list, coordinates in the board space [row, col]
        board: the numpy array presenting the input map state
    Returns:
        true if the 'position' is not a road or a wall in 'board'
    """
    value = board[position[0]][position[1]]
    return value >= 0

def get_board_dimensions(board):
    """
    Returns the dimensions of the board as a tuple (rows, columns).
    Throws IllegalBoard exceptions if there are no rows or columns.

    Parameters:
        board: the numpy array presenting the input map state
    Returns:
        tuple with the board dimensions (num_rows, num_cols)
    Throws:
        IllegalBoard: if the board is not a non-empty 2D array
    """
    dimensions = board.shape
    if len(dimensions) != 2:
        raise IllegalBoard("get_board_dimensions: there are fewer or more than 2 dimensions!")
    if 0 in dimensions:
        raise IllegalBoard("get_board_dimensions: rows or columns are empty!")
    return dimensions

# -----------------------------------------------------
# Exceptions
# -----------------------------------------------------
class IllegalSolution(Exception):
    """ Thrown when operating on an illegal candidate solution. """
    pass

class IllegalBoard(Exception):
    """ Thrown when operating on an illegal input problem. """
    pass
