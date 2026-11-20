"""
CISC 455 - Main code for trash can placement evolutionary algorithm
"""

import html

import numpy as np

from input import generate_map, load_map_from_csv, load_map_from_npy, save_map_to_csv, save_map_to_npy
from population import initialize_population
from fitness import fitness, get_pheno, pretty_print, calculate_can_cap
from selection import parent_selection, survior_selection
from recombination import n_point_crossover, arithmetic_crossover, uniform_crossover
from mutation import random_mutate, add_trashcan, remove_trashcan, modify_one_trashcan


def pretty_print_to_txt(list, f):
    """
    Writes to the given file with what the city looks like with numbers and shapes
    designed for a txt file, so black and white 
    """

    output = "" 
    for i in range(len(list)):
        for j in range(len(list[i])):
            val = list[i, j]

            if (type(val) == type(np.nan) or val == None):
                output = output + "■"

            elif (val == -2):
                output = output  + "█"

            elif (val == -1):
                output = output + "■" 

            elif (val == 0):
                output = output + "0"

            elif (val == 1):
                output = output + "1"

            elif (val == 2):
                output = output + "2"

            elif (val == 3):
                output = output + "3"

            elif (val == 4):
                output = output + "4"

            else:
                output = output + str(val)
        output = output + "\n"

    f.write(output)


def initialize_html(f):
    """
    To the given file, writes html header, style, and opens body. 
    """
    f.write(
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        "<style>"
        "table{border-collapse:collapse}"
        "td{border: 1px solid gray;;width:1em;height:1em;"
        "text-align:center;font-family:sans-serif}"
        "</style>\n</head>\n<body>\n")


def close_html(f):
    """
    For the given file, writes closing tag for html body and file. 
    """
    f.write("</body>\n</html>\n")


def pretty_print_to_html(grid, f, just_map=False):
    """
    Writes the city grid to the given file as a coloured HTML table.
    Pass True to just_map for printing the map, when 0s in the grid signify empty spaces rather than trash cans 
    """

    zero_display = "0"
    # don't print zeros if we're just printing map, not solution phen
    if just_map: zero_display = ""

    colors = {
        -1: ("#7f7f7f", "#000000", ""),
        -2: ("#000000", "#000000", ""),
        0: ("#ffffff", "#000000", zero_display),
        1: ("#48CF48", "#000000", "1"),
        2: ("#4b96f9", "#000000", "2"),
        3: ("#eded5a", "#000000", "3"),
        4: ("#e865e8", "#000000", "4"),
    }

    rows = []
    for row in grid:
        cells = []
        for val in row:
            if val is None or (
                isinstance(val, (float, np.floating)) and np.isnan(val)
            ):
                background, foreground, text = "#FFFFFF", "#ffffff", ""
            else:
                background, foreground, text = colors.get(
                    val, ("#f84e4e", "#000000", str(val))
                )

            cells.append(
                f'<td style="background-color:{background};color:{foreground}">'
                f"{text}</td>"
            )
        rows.append("<tr>" + "".join(cells) + "</tr>")

    f.write(
        "<table>\n"
        + "\n".join(rows)
        + "\n</table>\n"
    )       


def main():

    # consts
    N = 25
    popsize = 100
    mating_pool_size = popsize # must be even for parent selection & recombination
    ideal_steps_from_trashcan = 4 # (bc ideal is 3)
    gen_limit = 150
    n_crossover = 2
    crossover_method = lambda parent1, parent2, n, map: n_point_crossover(parent1, parent2, n, map)
    mutation_method = lambda individual, board, max_cans: random_mutate(individual, board, max_cans)
    # fitness penalties
    nonePenalty = 10 # should be high (handle gaps in building)
    canOverPenalty = 20
    overStepPenalty = 5

    # file saving and loading consts
    default_input_location = "./saved_maps/"
    default_output_location = "./saved_output/"
    run_name = "test" # modify for each new run so that contents don't overwrite 

    # generate map & save to file

    map = generate_map(N, N)
    # save_map_to_npy(map, "baseline_map.npy", default_input_location)
    # save_map_to_csv(map, "baseline_map.csv", default_input_location)

    # load map from csv file (uncomment both lines to use this option)
    # map = load_map_from_csv("map_test_easy.csv", "./saved_maps")
    # N, M = map.shape
    
    max_trashcans = calculate_can_cap(map,ideal_steps_from_trashcan)


    # load map from npy file
    # map = load_map_from_npy("baseline_map.npy", default_input_location)

    # initialize population
    population = initialize_population(popsize, map)

    # open file for storing output - make f None if only want to print to console
    f = open(default_output_location + run_name + ".html", "x", encoding="utf-8")
    # f = None

    # begin evolution    
    pretty_print(map)
    if f:
        initialize_html(f)
        f.write("<h1>Test Run - " + run_name + "</h1>")
        f.write("<h3>Input Map" + "</h3>")
        pretty_print_to_html(map, f, just_map=True)
        f.write("\n")

    gen = 1
    while gen <= gen_limit:
        # fitness eval
        fitness_list = []
        for individual in population:
            fitness_list.append(fitness(individual, map, ideal_steps_from_trashcan, nonePenalty, canOverPenalty, overStepPenalty))

        # print best fitness solutions & save to file
        k = 1
        for j in range(0, popsize):
            if fitness_list[j] == min(fitness_list) and gen % 10 == 0:
                print("gen", gen, "best solution",k, "fitness:", fitness_list[j])
                if f: f.write("<h3>Gen " + str(gen) + " - Best Solution no. " + str(k) + "</h3><p>Fitness: " + str(fitness_list[j]) + "</p>")
                
                pheno = get_pheno(population[j], map)
                pretty_print(pheno)
                if f: 
                    pretty_print_to_html(pheno, f)
                    f.write("\n")
                
                k = k + 1

        # parent selection
        parents = parent_selection(mating_pool_size, population, fitness_list)
        
        # reproduction
        children = []
        i = 0 # track parents
        while len(children) < mating_pool_size:
            
            # recombination (or maybe choose randomly?)
            child1, child2 = crossover_method(parents[i], parents[i+1], n_crossover, map) #parents[i], parents[i+1] 

            # mutation
            mutation_method(child1, map, max_trashcans)
            mutation_method(child2, map, max_trashcans)

            children.append(child1)
            children.append(child2)

            i += 2

        # survivor selection
        population = survior_selection(parents, children)

        gen += 1

    if f: close_html(f)

    # evolution ends

if __name__ == "__main__":
    main()
