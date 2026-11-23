"""
CISC 455 - Main code for trash can placement evolutionary algorithm
"""

import html

import numpy as np
import math

from input import generate_map, load_map_from_csv, load_map_from_npy, save_map_to_csv, save_map_to_npy
from population import initialize_population
from fitness import fitness, get_pheno, pretty_print, total_can_over_penalty
from selection import parent_selection, survior_selection
from recombination import n_point_crossover, arithmetic_crossover, uniform_crossover
from mutation import MutationStrategy


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
    """ The main EA algorithm for trashcan placement optimization """
    # ---------------------------------------------------------------
    # Execution parameters
    # ---------------------------------------------------------------
    # File saving and loading consts
    default_input_location = "./saved_maps/"
    default_output_location = "./saved_output/"
    
    # Execution info
    run_name = "run"            # Name of the output html file

    # ---------------------------------------------------------------
    # Input Problem Initialization
    # ---------------------------------------------------------------
    # Generate a random map       
    N = 25                      # Map width and height; NxN
    map = generate_map(N)       # Generate using N

    # Import from map (must be NxN); comment out the above to use
    # map = load_map_from_csv("map_test_easy.csv", default_input_location) 
    # N = map.shape[0]

    # Save the map to a file; uncomment to use
    # save_map_to_csv(map, "baseline_map.csv", default_input_location)

    # ---------------------------------------------------------------
    # Population and Control Parameters
    # ---------------------------------------------------------------
    popsize = 100                       # Population size
    gen_limit = 150                     # Number of iterations (termination condition)
    mating_pool_size = popsize          # do not edit; must be even for parent selection & recombination

    # ---------------------------------------------------------------
    # Mutation Strategy
    # ---------------------------------------------------------------
    mutation_method = MutationStrategy()
    mutation_method.setBoardState(map)
    mutation_method.setProbabilisiticMutation([0.33, 0.33, 0.33])   # [add, remove, modify] probabilities for mutation

    # ---------------------------------------------------------------
    # Recombination Strategy
    # ---------------------------------------------------------------
    n_crossover = 2
    crossover_method = lambda parent1, parent2, n, map: n_point_crossover(parent1, parent2, n, map)

    # ---------------------------------------------------------------
    # Fitness Parameters and Penalties
    # ---------------------------------------------------------------
    ideal_steps_from_trashcan = 4       # All spots should be within this many steps from a trashcan (4 because 3 is ideal)
    nonePenalty = 10                    # Penalty each tile that cannot reach a trashcan (should be high deal with courtyards)
    canOverPenalty = 20                 # Penalty each unecessary trashcans
    overStepPenalty = 5                 # Penalty for each tile further than ideal_steps_from_trashcan to a trashcan

    # ---------------------------------------------------------------
    # Algorithm
    # ---------------------------------------------------------------

    # initialize population
    population = initialize_population(popsize, map)
    learned_mutation_probs = MutationStrategy.initLearnedProbabilities(popsize)

    # open file for storing html output - make f None if only want to print to console
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
                print("gen", gen, "best solution",k, "fitness:", fitness_list[j], "num_trashcans:", len(population[j]))
                if f: f.write("<h3>Gen " + str(gen) + " - Best Solution no. " + str(k) + "</h3><p>Fitness: " + str(fitness_list[j]) + " - Num Trashcans: " + str(len(population[j])) + "</p>")
                
                pheno = get_pheno(population[j], map)
                pretty_print(pheno)
                if f: 
                    pretty_print_to_html(pheno, f)
                    f.write("\n")
                
                k = k + 1

        # parent selection
        parents, parent_mutation_probs = parent_selection(mating_pool_size, population, fitness_list, learned_mutation_probs)
        
        # reproduction
        children = []
        i = 0 # track parents
        while len(children) < mating_pool_size:

            # mutation: informed mutation on the parents because their fitness is already calculated
            if mutation_method.getStrategy() == MutationStrategy.Strategy.INFORMED:
                mutation_method.mutate(parents[i], fitness=fitness_list[i], penalty=total_can_over_penalty(parents[i], map, ideal_steps_from_trashcan, canOverPenalty))
                mutation_method.mutate(parents[i+1], fitness=fitness_list[i+1], penalty=total_can_over_penalty(parents[i+1], map, ideal_steps_from_trashcan, canOverPenalty))

            # recombination
            child1, child2 = crossover_method(parents[i], parents[i+1], n_crossover, map)

            # mutation: all other mutations happen after recombination
            if mutation_method.getStrategy() == MutationStrategy.Strategy.SELF_ADAPTIVE:
                mutation_method.mutate(child1, learned_probabilities=parent_mutation_probs[i])
                mutation_method.mutate(child2, learned_probabilities=parent_mutation_probs[i+1])
            elif mutation_method.getStrategy() != MutationStrategy.Strategy.INFORMED:
                mutation_method.mutate(child1)
                mutation_method.mutate(child2)

            children.append(child1)
            children.append(child2)

            i += 2

        # survivor selection
        population = survior_selection(parents, children)
        learned_mutation_probs = parent_mutation_probs

        gen += 1

    if f: close_html(f)

    # evolution ends

if __name__ == "__main__":
    main()