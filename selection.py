import random

def parent_selection(lambda_pointers, population, fitness):

    """
    Stochastic Universal Sampling to select parents for the next generation based on their fitness.

    parameters:
        lambda_pointers: int
        The number of parents to select.
        population: list
        The current population of individuals.
        fitness: list
        The fitness values corresponding to each individual in the population.
    
    returns:
        selected_individuals: list
        A list of selected individuals based on their fitness.
    """
    total_fitness = sum(fitness)

    #assign probabilities to each individual based on their fitness
    probabilities = []

    for i in range(len(population)):
        probabilities.append(fitness[i] / total_fitness)
    
    #generate random pointers
    spacing = 1 / lambda_pointers
    first_pointer = random.uniform(0, spacing)
    #place pointers
    pointers = []
    for i in range(lambda_pointers):
        pointers.append(first_pointer + i * spacing)
    
    #select individuals based on pointers
    selected_individuals = []
    for pointer in pointers:
        cumulative_probability = 0
        for i in range(len(population)):
            cumulative_probability += probabilities[i]
            if cumulative_probability >= pointer:
                selected_individuals.append(population[i])
                break
    
    return selected_individuals

def survior_selection(population, offspring):
    """
    Generational Replacement to select the next generation of individuals from the current population and offspring.
    parameters:
        population: list
        The current population of individuals.
        offspring: list
        The newly generated offspring individuals.
        
    returns:
        offspring: list
        A list of all individuals from the next generation.
    """
    return offspring
