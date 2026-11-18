import random

"""
This file performs recombination for trash can placement evolutionary algorithm.
We use three different recombination methods: n-point crossover, arithmetic crossover, and uniform crossover 
"""

def fix_child(child, grid):
    """
    Ensures no duplicates
    Fixes a child solution to ensure that all trash can coordinates are valid (i.e., not on roads or buildings).

    - Valid coordinates are those that are not on roads (-1) or buildings (-2).
    - Replaces invalid coordinates with random valid coordinates from the grid.

    Returns a fixed child solution with valid coordinates.
    """

    valid_locations = []

    #find all valid locations
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] != -1 and grid[x][y] != -2:
                valid_locations.append([x, y])

    fixed_child = []

    for coordinate in child:
        x, y = coordinate
        #check if the coordinate is valid
        if (0 <= x < len(grid) and
            0 <= y < len(grid[x]) and
            grid[x][y] != -1 and
            grid[x][y] != -2 and
            coordinate not in fixed_child):

            fixed_child.append(coordinate)

        else:
            #find valid locations that are not already occupied
            available_locations = []

            for location in valid_locations:
                if location not in fixed_child:
                    available_locations.append(location)

            #replace invalid or duplicate coordinate
            if len(available_locations) > 0:
                new_location = random.choice(available_locations)
                fixed_child.append(new_location)

    return fixed_child


def n_point_crossover(parent1, parent2, n, grid):
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
        return fix_child(child1, grid), fix_child(child2, grid)

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

    return fix_child(child1, grid), fix_child(child2, grid)


def arithmetic_crossover(parent1, parent2, grid):
    """
    n-point arithmetic crossover

    - create new trash can coordinates between the corresponding coordinates of the two parents.
    - continue until the shorter parent ends 
    - keep the remaining tail of the longer parent 
    """

    child1 = []
    child2 = []

    min_length = min(len(parent1), len(parent2))

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

    return fix_child(child1, grid), fix_child(child2, grid)


# --------------------------------------------------
# 3. UNIFORM CROSSOVER
# --------------------------------------------------
# Randomly swap x and y coordinates between parents.
# Continue until the shorter parent ends.
# Keep the extra tail from each original parent.


def uniform_crossover(parent1, parent2, grid):

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
    return fix_child(child1, grid), fix_child(child2, grid)
