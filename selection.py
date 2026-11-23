import random

def parent_selection(lambda_pointers, population, fitness, mutation_probs):

    """
    Stochastic Universal Sampling to select parents for the next generation based on their fitness.

    parameters:
        lambda_pointers: int
        The number of parents to select.
        population: list
        The current population of individuals.
        fitness: list
        The fitness values corresponding to each individual in the population.
        mutation_probs: list of lists
        The associated learned mutation probabilities with each individual in the population
        (for self-adaptive mutation)
    
    returns:
        selected_individuals: list
        A list of selected individuals based on their fitness.
        selected_mutation_probs: list
        The list of mutation probabilities associated with the selected individuals
    """
    inverse_fitness = []

    for i in range(len(population)):
        #inverse fitness for minimization problems
        inverse_fitness.append(1 / (fitness[i] + 1))

    total_fitness = sum(inverse_fitness)

    #assign probabilities to each individual based on their fitness
    probabilities = []

    for i in range(len(population)):
        probabilities.append(inverse_fitness[i]/total_fitness)
    
    #generate random pointers
    spacing = 1 / lambda_pointers
    first_pointer = random.uniform(0, spacing)
    #place pointers
    pointers = []
    for i in range(lambda_pointers):
        pointers.append(first_pointer + i * spacing)
    
    #select individuals based on pointers
    selected_individuals = []
    selected_mutation_probs = []
    for pointer in pointers:
        cumulative_probability = 0
        for i in range(len(population)):
            cumulative_probability += probabilities[i]
            if cumulative_probability >= pointer:
                selected_individuals.append(population[i])
                selected_mutation_probs.append(mutation_probs[i])
                break
    
    return selected_individuals, selected_mutation_probs

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
