# CISC455_Evolutionary_Algorithm
Group 2 - Evolutionary Ops
Claire Whelan, Nicole Hernandez, Trevor White, Emma Leitch-Blais, Maria Kobilaski

## Description
This EA is designed to evolve trash can placement for a generated 2D city map. Fitness of solutions are calculated by assigning a score to each coordinate on the map, this score indicates how far that coordinate is from a trash can. The lower the fitness score of a solution, the more optimal. Each additional trashcan placed negatively impacts the fitness. 

## Purpose
The purpose of this algorithm is to minimize the walking distance from a trash can to any point on the map while minimizing the amount of trash cans used. 

## Running the EA

### Dependencies
To run the program, make sure to have the following programs and libraries installed:

- python3
- NumPy

Additionally, the unit tests require the `pytest`, but they are all deprecated. They have been moved to `outdated_tests/` to avoid confusion.

### Run the Program
To run the EA, update the `run_name` parameter in `main()`. This should be a unique name that will be given to the output file.
```
run_name = "run"            # Name of the output html file
```

Then, simply execute the main file: 
```
python3 main.py
```

## Input Problem Initialization
### About Input Maps
All generated input maps are square. The generated starting map uses the following values to designate obstacles:
- `0`: free space
- `-1`: road
- `-2`: building

### Generating Random Input Maps
You can generate an random input map of size `NxN`. This is the default setting. The following lines should be uncommented in `main()`:
```
# Generate a random map       
N = 25                      # Map width and height; NxN
map = generate_map(N)       # Generate using N
```
### Reading Input Maps from Files
You can also read an input map in from a `.csv` file. To do so, uncomment the following lines, and comment the lines above for random input:
```
# Import from map (must be NxN); comment out the above to use
# map = load_map_from_csv("map_test_easy.csv", default_input_location) 
# N = map.shape[0]
```
The input maps are taken from `saved_maps/` by default. The maps used for validation of the algorithm there for your reference.

### Saving a Randomly Generated Map
You can save a randomly generated input map by uncommenting the following:
```
# Save the map to a file; uncomment to use
# save_map_to_csv(map, "baseline_map.csv", default_input_location)
```

## Algorithm Paramters
These paramters have been set according to the problem scope and algorithm tuning performed. They are defined under the corresponding headers in the `main()` function.

### Population and Control Parameters
The algorithm maitains a population with `popsize` individuals. Its termination condition is `gen_limit`, the number of generations before termination condition is reached.
For recombination, `mating_pool_size` is defined. It must be the same as the popsize to maintain a constant population size. The selected values are the following:
```
popsize = 100                       # Population size
gen_limit = 150                     # Number of iterations (termination condition)
mating_pool_size = popsize          # do not edit; must be even for parent selection & recombination
```
### Mutation Strategy
The chosen mutation strategy for the EA is a probabilistic selection for each type of basic mutation: add, remove, and modify. The tuned values
are 33% for each basic operator, as shown below. 
```
mutation_method = MutationStrategy()
mutation_method.setBoardState(map)
mutation_method.setProbabilisiticMutation([0.33, 0.33, 0.33])   # [add, remove, modify] probabilities for mutation
```

Various other mutation strategies where implemented and evaluated against this one. To simplify testing and swapping of mutation strategies,
a helper class in `mutation.py` was used. Briefly, here is how you can select different mutation strategies, although we do not expect them to be used:
```
# Random:           mutation_method.setRandomMutation()
# Probabilistic:    mutation_method.setProbabilisiticMutation([p_add, p_remove, p_modify])
# Informed:         mutation_method.setInformedMutation([lower, upper])
# Learning:         mutation_method.setLearningMutation(sigma)
```
where `p_xxx` is the probability of the corresponding basic mutation operator, `lower` and `upper` and boundary percentages for the proportion of `canOverMax` to fitness,
and `sigma` is a standard deviation for mutating learned operator probabilities. Informed mutation uses a heuristic and learning mutation is derived from probabilistic.

### Recombination Strategy
The chosen recombination strategy is n point crossover with `n = 2`, again based on experiemental results. In the `main()` function, you can find
it as a lamba wrapping the corresponding function:
```
n_crossover = 2
crossover_method = lambda parent1, parent2, n, map: n_point_crossover(parent1, parent2, n, map)
```

Much like mutation, two other types of recombination were evaluated and discarded since they under performed. These are `arithmetic_crossover` and `uniform_crossover`,
found in `recombination.py`. We don't expect them to be used as they were not selected in the design, but if desired, you can update the lamba above as well as this line:
```
# recombination
child1, child2 = crossover_method(parents[i], parents[i+1], n_crossover, map)
```

### Fitness Parameters and Penalties
Fitness is evaluated by summing the steps for all spots to a trash can. One of the required parameters is the ideal distance from any point to a trash can, which is part of the
problem definition. Since there are competing constraints, 3 penalties are also used: `nonePenalty` discourages unreachable tiles such as courtyards, `canOverPenalty` worsens fitness for excessive trash cans, and `overStepPenalty` inflates the scores of trash cans that oare outside of the ideal steps. For example, `canOverPenalty` prevents solutions with trash cans on every tile. 
```
ideal_steps_from_trashcan = 4       # All spots should be within this many steps from a trashcan (4 because 3 is ideal)
nonePenalty = 10                    # Penalty each tile that cannot reach a trashcan (should be high deal with courtyards)
canOverPenalty = 50                 # Penalty each unnecessary trashcans
overStepPenalty = 10                # Penalty for each tile further than ideal_steps_from_trashcan to a trashcan
```
The values above for the penalties were decided through tuning, generally observing that high `canOverPenalty` is most important to minimize trash cans.

## Output
Every 10 generations, the best solution is printed to the console. The final solution is also printed to the console at the end of the run. The HTML output is by default saved in the `saved_outputs/` folder.
