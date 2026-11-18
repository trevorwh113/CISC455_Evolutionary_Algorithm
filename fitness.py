import math
import numpy as np

# Colour constants from https://sentry.io/answers/print-colored-text-to-terminal-with-python/
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[97m'
RESET = '\033[0m' # called to return to standard terminal text color

def get_pheno(individual, input):
    """
    Computes how far each cell is from a trash can.

        EX it turns 
        [[0, 0, 0, -1, 0, 0],
         [0, 0, 0, -2, 0, 0],
         [0, 0, -2, -2, -2, 0],
         [0, 0, -2, -1, -2, 0],
         [0, 0, -2, -2, -2, -2],
         [0, 0, 0, -1, -2, -2],]
         to 
        5 5 5 5 6 7
        4 4 4-2 6 7
        3 3-2-2-2 7
        2 2-2-1-2 8
        1 1-2-2-2-2
        0 1 2 3-2-2

    Parameters:
       individual (list of coordinates): Where the trash can are.
       input (2D list): map of all of the roads and buildings

    Returns:
        pheno (np.array): The map with all the cell populated with how far it is from a trash can.
    """  
    # create the list to store the pheno type
    pheno = input.copy()

    # place the -1 and 0 to None
    pheno[pheno >= -1] = np.nan

    # inisalize the explore queue and other var needed for the search
    q = individual.copy()
    explored = q.copy()
    end = q[-1]
    counter = 0

    # do breadth first search on the grid to see how min distance that cell is from a trash can
    while (len(q)>0):
        # dequeue
        cell = q.pop(0)

        # check if the cell has a value already
        if(type(pheno[cell[0], cell[1]]) == type(np.nan) or pheno[cell[0], cell[1]] != -2):
            pheno[cell[0], cell[1]] = counter

        # add the non explored and non building adjacent cells to the queue
        newcells = adj_cells(cell, pheno.shape[0], pheno.shape[1])
        for elem in newcells:
            # check if the cell has been explored or not a building
              if(not(elem in explored) and pheno[elem[0], elem[1]] != -2):
                # add to queue
                q.append(elem)
                explored.append(elem)

        # check if counter needs to be updated
        if (end == cell and len(q)>0):
            end = q[-1]
            counter+=1  
    return pheno

def adj_cells(index, col, row): 
    """
    Computes all valid cells around an np.array index

    Parameters:
        index (np.array): Input vector of shape (n,).
        col (int): How many cols the array has
        row (int): How many rows the array has.

    Returns:
        cells (list): list of the coordinates of valid adjacent cells around indez
    """ 
    xMax = row-1
    yMax = col-1
    cells = []

    # check all 8 cells around the index (the cell same as the index will be skipped) 
    for i in range(3,6):
        for j in range(3,6):
            # i%3-1 gets -1, 0, 1 then add it to the x index
            x = index[0]+(i%3-1)

            # j%3-1 gets -1, 0, 1 then add it to the y index
            y = index[1]+(j%3-1)
            # check if valid index
            if (0 <= x and x <= xMax):
                if (0 <= y and y <= yMax):
                    if(not(x == index[0] and y == index[1])):
                        # add index to output
                        cells.append([x,y])
    return cells

def pretty_print(list): 
    """
    Prints to the consol what the city looks like with colours and shapes
        Building: represend by -2, printed as a cyan █
        Road: represend by -1, printed as a light grey ■
        Null: represend by np.nan, printed as a black ■
        Trash Can: represend by 0, printed as a white 0

        EX:
        555567
        444█67
        33███7
        22█■█8
        11████
        0123██

    Parameters:
   list (np.array): Map of the city.
    """  

    """"
    # Placing trash cans
    for i in range(len(individual)):
        temp = individual[i] 
        pheno[temp[1], temp[0]] = 0
    """
    output = "" 
    for i in range(len(list)):
        for j in range(len(list[i])):
            val = list[i, j]

            if (type(val) == type(np.nan) or val == None):
                output = output + BLACK + "■" + RESET

            elif (val == -2):
                output = output + CYAN + "█" + RESET

            elif (val == -1):
                output = output + RESET + "■" 

            elif (val == 0):
                output = output + WHITE+ "0" + RESET

            elif (val == 1):
                output = output + GREEN + "1" + RESET

            elif (val == 2):
                output = output + BLUE+ "2" + RESET

            elif (val == 3):
                output = output + YELLOW + "3" + RESET

            elif (val == 4):
                output = output + MAGENTA  + "4" + RESET

            else:
                output = output + RED +str(val) +RESET
        output = output + "\n"
    print(output)

def fitness(individual, input, maxStep): 
    """
    Compute fitness of an individual for the trash can alocation problem. 
    
    Parameters:
       individual (list of coordinates): Where the trash can are.
       input (2D list): map of all of the roads and buildings

    Returns:
        score ():The score of an individual. Lower score is better.
    """
    # Lower score is better
    score = 0

    # penalty scores so easy to change
    nonePenalty = 5
    canOverPenalty = 5
    overStepPenalty = 5

    # get how far each cell is from a trash can
    map = get_pheno(individual, input)

    # find out how many of item there is 
    unique, counts = np.unique(map, return_counts=True)
    map = dict(zip(unique, counts))

    for elem in unique:
        # there is a none
        if (elem == np.nan):
            score = score + map[elem]*nonePenalty

        # between 1 and max step
        elif (1 <= elem and elem <= maxStep):
            score = score + map[elem]*elem

        # bigger than maxstep
        elif (elem > maxStep):
            score = score + map[elem]*elem*overStepPenalty
        
    # 1 trash can can easily cover a 7x7 space so a 49 area (if we want 3 steps between cans)
    trashCanCap = math.ceil(input.shape[0]*input.shape[1]/(maxStep*2+1)**2)

    #  minimization: penalty for each trash can (how much relative to distance penalty?)
    score = score + (len(individual)-trashCanCap)*canOverPenalty

    return score