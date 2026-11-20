"""
CISC 455 - Main code for trash can placement evolutionary algorithm
"""

from input import generate_map, load_map_from_csv, load_map_from_npy, save_map_to_csv, save_map_to_npy
from population import initialize_population
from fitness import fitness, get_pheno, pretty_print
from selection import parent_selection, survior_selection
from recombination import n_point_crossover, arithmetic_crossover, uniform_crossover
from mutation import random_mutate, add_trashcan, remove_trashcan, modify_one_trashcan

def main():

    # consts
    N = 10
    M = 10
    default_file_location = "./saved_maps/"
    popsize = 20
    mating_pool_size = popsize # must be even for parent selection & recombination
    ideal_steps_from_trashcan = 3
    max_trashcans = N*M
    gen_limit = 20
    n_crossover = 2
    crossover_method = lambda parent1, parent2, n, map: n_point_crossover(parent1, parent2,n,map)
    mutation_method = lambda individual, board, max_cans: random_mutate(individual, board, max_cans)

    # generate map & save to file

    map = generate_map(N, M)
    # save_map_to_npy(map, "baseline_map.npy", default_file_location)
    # save_map_to_csv(map, "baseline_map.csv", default_file_location)

    # load map from csv file (uncomment both lines to use this option)
    # map = load_map_from_csv("map_test_easy.csv", "./saved_maps")
    # N, M = map.shape

    # load map from npy file
    # map = load_map_from_npy("baseline_map.npy", default_file_location)
    pretty_print(map)


    # initialize population
    population = initialize_population(popsize, map)

    # begin evolution
    gen = 0
    while gen < gen_limit:
        # fitness eval
        fitness_list = []
        for individual in population:
            fitness_list.append(fitness(individual, map, ideal_steps_from_trashcan))

        # print best fitness solutions
        k = 1
        for j in range(0, popsize):
            if fitness_list[j] == min(fitness_list):
                print("gen", gen, "best solution",k, "fitness:", fitness_list[j])
                print(population[j])
                pheno = get_pheno(population[j], map)
                pretty_print(pheno)
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

    # evolution ends

if __name__ == "__main__":
    main()
