import random

"""
This file performs recombination for trash can placement evolutionary algorithm.
We use three different recombination methods: n-point crossover, arithmetic crossover, and uniform crossover 
"""

def n_point_crossover(parent1, parent2, n):
    """
    n-point crossover

    - Take trash can coordinates directly from the parents.
    - Swap sections between the parents.
    - If parents have different lengths, keep the extra tail.
    """

    # make copies so we don't change the original parents
    child1 = parent1.copy()
    child2 = parent2.copy()

    # find the length of the smaller parent
    min_length = min(len(parent1), len(parent2))

    # choose crossover points
    if min_length < 2:
        return child1, child2

    points = sorted(random.sample(range(1, min_length), min(n, min_length - 1)))

    # add bounds
    points = [0] + points + [min_length]

    # swap sections between parents
    for i in range(len(points) - 1):

        start = points[i]
        end = points[i + 1]

        if i % 2 == 1:
            child1[start:end] = parent2[start:end]
            child2[start:end] = parent1[start:end]

    return child1, child2


def arithmetic_crossover(parent1, parent2, n):
    """
    n-point arithmetic crossover

    - create new trash can coordinates between the corresponding coordinates of the two parents.
    - continue until the shorter parent ends 
    - keep the remaining tail of the longer parent 
    """

    child1 = []
    child2 = []

    min_length = min(len(parent1), len(parent2))

    # choose crossover points
    if min_length < 2:
        points = [0, min_length]
    else:
        points = random.sample(range(1, min_length), min(n, min_length - 1))
        points.sort()
        points = [0] + points + [min_length]

    # create coordinates between the parents
    for i in range(min_length):

        x1, y1 = parent1[i]
        x2, y2 = parent2[i]

        # Find a random point between the two coordinates
        alpha = random.random()

        new_x1 = int(alpha * x1 + (1 - alpha) * x2)
        new_y1 = int(alpha * y1 + (1 - alpha) * y2)

        new_x2 = int((1 - alpha) * x1 + alpha * x2)
        new_y2 = int((1 - alpha) * y1 + alpha * y2)

        child1.append([new_x1, new_y1])
        child2.append([new_x2, new_y2])

    # keep the extra coordinates from the longer parent
    if len(parent1) > min_length:
        child1.extend(parent1[min_length:])
        child2.extend(parent1[min_length:])

    elif len(parent2) > min_length:
        child1.extend(parent2[min_length:])
        child2.extend(parent2[min_length:])

    return child1, child2


# --------------------------------------------------
# 3. UNIFORM CROSSOVER
# --------------------------------------------------
# Randomly swap x and y coordinates between parents.
# Continue until the shorter parent ends.
# Keep the extra tail from each original parent.


def uniform_crossover(parent1, parent2):

    """
    uniform crossover 

    - Randomly swap x and y coordinates between parents 
    - Continue until end of the smaller parent's length
    - Keep the extra tail from each original parent
    """

    child1 = []
    child2 = []

    min_length = min(len(parent1), len(parent2))

    for i in range(min_length):

        x1, y1 = parent1[i]
        x2, y2 = parent2[i]

        # randomly decide whether to swap each coordinate
        if random.random() < 0.5:
            child1.append([x1, y2])
            child2.append([x2, y1])

        else:
            child1.append([x2, y1])
            child2.append([x1, y2])

    #keep the remaining coordinates
    child1.extend(parent1[min_length:])
    child2.extend(parent2[min_length:]) 
    return child1, child2
