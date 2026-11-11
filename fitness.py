import numpy as np
# from https://sentry.io/answers/print-colored-text-to-terminal-with-python/
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHT_GRAY = '\033[37m'
DARK_GRAY = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'

RESET = '\033[0m' # called to return to standard terminal text color

#input = [[#buildings], (-2)
#         [#roads]] (-1)
input = [[[2,2],[4,4],[4,5],[5,5],[5,4]],
         [[3,1],[3,2],[3,3],[3,4],[3,5],]]
input = [[0, 0, 0, -1, 0, 0],
         [0, 0, 0, -1, 0, 0],
         [0, 0, -2, -1, 0, 0],
         [0, 0, 0, -1, 0, 0],
         [0, 0, 0, -1, -2, -2],
         [0, 0, 0, -1, -2, -2],]

individial = [[1,2],[1,4],[4,3]]

def fitness(individual):  # maximization

    """Compute fitness of an individual for the 8-queen puzzle"""

    Max = 28
    violations = 0 # only diagonal conflicts need to be counted because
                   # the permutation representation prevents row/column conflicts
    l = len(individual)
    for i in range(0, l):
        for j in range(i + 1, l):
            # student code begin
            # detect a diagonal conflict
            # need to check if j is equal to i+distance ie if i is 1 and j is 2 away, then the number at j should not be 3
            rowDiff = j-i
            if(individual[j] == individual[i]+rowDiff):
                violations= violations+1
            # student code end
    return Max - violations


def get_pheno(individual):  
    repeat = True
    # create the list to store the pheno type
    pheno = input.copy()

    # place the -1 and 0 to None
    for i in range(len(pheno)):
        pheno[i] = [None if x > -1 else x for x in pheno[i]]

    # Placing trash cans
    for i in range(len(individual)):
        temp = individual[i] 
        pheno[temp[1]][temp[0]] = 0

    #while(repeat):
    
    return pheno

def pretty_print(list): 
    output = "" 
    for i in range(len(list)):
        for j in range(len(list[i])):
            val = list[i][j]
            if (val == None):
                output = output + BLACK + "■" + RESET

            elif (val == -2):
                output = output + CYAN + "█" + RESET

            elif (val == -1):
                output = output + WHITE + "■" + RESET

            elif (val == 0):
                output = output + GREEN + "0" + RESET

            elif (val == 1):
                output = output + CYAN + "1" + RESET

            elif (val == 2):
                output = output + YELLOW + "2" + RESET

            elif (val == 3):
                output = output + BRIGHT_YELLOW + "3" + RESET

            elif (val == 4):
                output = output + RED + "4" + RESET

            else:
                output = output + val +RESET
        output = output + "\n"

    print(output)

pretty_print(get_pheno(individial))